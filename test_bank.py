import unittest
import doctest

from bank import Account

class TestJohnOuvreUnCompte(unittest.TestCase):
    """
    Cette classe test l'ouverture d'un compte ainsi que les deux operations elementaires que sont
    les credits et les debits
    """
    
    def test_ouverture_de_compte_solde_a_zero(self):
        """Test l'ouverture d'une compte et son solde"""

        account = Account()
        self.assertEquals(account.balance(), 0)
        
    def test_credit_du_compte_positivement(self):
        """Test l'accreditement d'un compte"""
        
        account = Account()
        amount = 100
        old_balance = account.balance()
        account.credit(amount)
        new_balance = account.balance()
        self.assertEquals(old_balance+amount, new_balance)
        
    def test_credit_du_compte_negativement(self):
        """Test l'accreditement d'un compte negativement"""
        
        account = Account()
        amount = -10
        self.assertRaises(ValueError, account.credit, amount)
        
    def test_debit_du_compte_positivement(self):
        """Test le debit d'un compte avec une valeur positive"""
        
        account = Account()
        amount = 100
        old_balance = account.balance()
        account.debit(amount)
        new_balance = account.balance()
        self.assertEquals(old_balance-amount, new_balance)
        
    def test_debit_sur_solde_negatif(self): 
        """Test le debit quand le solde est deja negatif""" 
        account = Account()
        amount = -100
        self.assertRaises(ValueError, account.debit, amount)
        
    def test_debit_du_compte_negativement(self):
        """Test le debit d'un compte negativement"""
        
        account = Account()
        amount = -10
        self.assertRaises(ValueError, account.debit, amount)
        
        