import unittest

from bank import Account
from bank import Transfert

from mockito import mock
from mockito import verify
from mockito import when
from mockito import never
from mockito import times

    
class TestJohnCrediteSonCompte(unittest.TestCase):
        
    def setUp(self):
        self.storage = mock()
        self.account = Account(self.storage)

            
    
    def test_credit_du_compte_positivement(self):
        """Test l'accreditement d'un compte"""

        amount = 100
        self.account.credit(amount)
        verify(self.storage).insert(amount)
        
    def test_historique(self):
        when(self.storage).select().thenReturn([])
        history = self.account.historique()
        self.assertEquals(history, self.account.operations)
        
    def test_can_accept_credit_valeur_positive(self):
        """Test si un compte accepte un credit sur valeur positive"""
        amount = 1
        self.assertTrue(self.account.can_accept_credit(amount))
        
    def test_can_accept_credit_valeur_negative(self):
        """Test si un compte accepte un credit sur valeur negative"""
        amount = -1
        self.assertFalse(self.account.can_accept_credit(amount))
    
    def test_credit_du_compte_negativement(self):
        """Test l'accreditement d'un compte negativement"""
        
        amount = -10
        self.assertRaises(ValueError, self.account.credit, amount)

class TestJohnDebiteSonCompte(unittest.TestCase):
        
    def test_debit_du_compte_positivement(self):
        """Test le debit d'un compte avec une valeur positive"""
        
        storage = mock()
        when(storage).select().thenReturn([105])
        account = Account(storage)
        amount = 100
        account.debit(amount)
        verify(storage).insert(-amount)
        
    def test_debit_sur_solde_insuffisant(self): 
        """Test le debit quand le solde est insuffisant""" 
        storage = mock()
        when(storage).select().thenReturn([])
        account = Account(storage)
        amount = 11
        self.assertRaises(ValueError, account.debit, amount)
        
    def test_debit_du_compte_negativement(self):
        """Test le debit d'un compte negativement"""
        
        storage = mock()
        account = Account(storage)
        amount = -10
        self.assertRaises(ValueError, account.debit, amount)
        
    def test_debit_d_une_valeur_trop_importante(self):
        """Test le debit par une valeur trop importante aka plus grande que le solde courant"""
        storage = mock()
        when(storage).select().thenReturn([5])
        account = Account(storage)
        amount = 10
        
class TestJohnOuvreUnCompte(unittest.TestCase):
    """
    Cette classe test l'ouverture d'un compte ainsi que les deux operations elementaires que sont
    les credits et les debits
    """
    def setUp(self):
        self.storage = mock()
        self.account = Account(self.storage)
    
    def test_ouverture_de_compte_solde_a_zero(self):
        """Test l'ouverture d'une compte et son solde"""
        
        when(self.storage).select().thenReturn([])
        self.assertEquals(self.account.balance(), 0)
        
    def test_balance(self):
        """Test la balance d'un compte"""
        when(self.storage).select().thenReturn([10, -5])
        balance = self.account.balance()
        self.assertEquals(balance, 5)    
        
class TestJohnTrasnfertDeLArgentASaFemme(unittest.TestCase):
    
    def setUp(self):
        self.accountSrc = mock()
        self.accountDest = mock()
        self.transfer = Transfert(self.accountSrc, self.accountDest)
    
    def test_transfert_debite_le_bon_compte(self):
        """Test si lors du transfert la valeur est bien debitee de la source"""

        amount = 100
        when(self.accountDest).can_accept_credit(amount).thenReturn(True)
        self.transfer.transfer(amount)
        verify(self.accountSrc, times=1).debit(amount)
        
    def test_transfert_credite_le_bon_compte(self):
        """Test si lors du transfert la valeur est bien creditee a la destination"""
      
        amount = 100
        when(self.accountDest).can_accept_credit(amount).thenReturn(True)
        self.transfer.transfer(amount)
        verify(self.accountDest, times=1).credit(amount)
        
    def test_transfert_credite_et_debite_de_la_meme_valeur(self):  
        """Test que lors d'un transfert la valeur debitee et creditee est la meme"""  
        amount = 100
        when(self.accountDest).can_accept_credit(amount).thenReturn(True)
        self.transfer.transfer(amount)
        verify(self.accountDest, times=1).credit(amount)
        verify(self.accountSrc, times=1).debit(amount)

    def test_debit_errone_ne_credite_pas(self):
        """Test si en cas d'erreur lors du debit, il n'y a pas de credit"""
        
        amount = 100
        when(self.accountDest).can_accept_credit(amount).thenReturn(True)
        when(self.accountSrc).debit(amount).thenRaise(ValueError)
        
        self.assertRaises(ValueError, self.transfer.transfer, amount)
        verify(self.accountDest, never).credit(amount)
        
    def test_credit_errone_ne_debite_pas(self):
        """Test si quand le credit n'est pas possible, il n'y a pas de debit"""
        
        amount = 100
        when(self.accountDest).can_accept_credit(amount).thenReturn(False)
        self.assertRaises(ValueError, self.transfer.transfer, amount)
        verify(self.accountSrc, never).debit(amount)    