import unittest
from mockito        import mock
from mockito        import verify
from mockito        import when
from mockito        import never
from entreprise     import DevisInvalide
from entreprise     import ServiceCommande
from entreprise     import DateInterventionInvalide
from entreprise     import UtilisateurNonAutorise
from entreprise     import Devis
from entreprise     import PrestationInconnue
from entreprise     import DevisFinalise

class TestJaneCreeUneCommandePourUnDevisValideEtUneDateDInterventionCorrecte(unittest.TestCase):

    def setUp(self):
        self.commandes = mock()
        self.fabrique = mock()
        self.service = ServiceCommande(self.commandes, self.fabrique)
        self.devis = mock()
        self.date = mock()
        self.createur = mock()
        self.commande = mock()
        
        when(self.fabrique).nouvelle_commande(self.createur, self.date, self.devis).thenReturn(self.commande)
        
        when(self.commande).devis().thenReturn(self.devis)
        when(self.commande).date().thenReturn(self.date)
        when(self.commande).createur().thenReturn(self.createur)
        
    def test_Jane_cree_une_commande_pour_un_devis_valide_et_une_date_d_intervention_correcte_ajoute_la_commande(self):
        """Test l'ajout d'une commande valide par Jane"""

        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(True)
        self.service.ajouter_commande(self.createur, self.date, self.devis)
        verify(self.commandes).append(self.commande)
        
    def test_Jane_cree_une_commande_pour_un_devis_invalide_et_une_date_d_intervention_correcte_leve_une_exception(self):
        """Test l'ajout d'une commande avec un devis invalide. Une exception est alors levee"""
        
        when(self.devis).expire().thenReturn(True)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(True)
        self.assertRaises(DevisInvalide, self.service.ajouter_commande, self.createur, self.date, self.devis)
        
    def test_Jane_cree_une_commande_pour_un_devis_invalide_et_une_date_d_intervention_correcte_n_ajoute_pas(self):
        """Test l'ajout d'une commande avec un devis invalide. L'ajout n'a alors pas lieu"""        
        
        when(self.devis).expire().thenReturn(True)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(True)
        try:
            self.service.ajouter_commande(self.createur, self.date, self.devis)
        except(DevisInvalide):
            pass
        verify(self.commandes, never).append(self.commande)
        
    def test_Jane_cree_une_commande_pour_un_devis_valide_et_une_date_d_intervention_incorrecte_leve_une_exception(self):
        """Test l'ajout d'une commande avec une date invalide. Une exception est levee"""
        
        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(True)
        when(self.createur).peut_creer_commandes().thenReturn(True)        
        self.assertRaises(DateInterventionInvalide, self.service.ajouter_commande, self.createur, self.date, self.devis)
        
    def test_Jane_cree_une_commande_pour_un_devis_valide_et_une_date_d_intervention_incorrecte_n_ajoute_pas(self):
        """Test l'ajout d'une commande avec une date invalide. L'ajout n'a alors pas lieu"""
        
        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(True) 
        when(self.createur).peut_creer_commandes().thenReturn(True) 
        try:
            self.service.ajouter_commande(self.createur, self.date, self.devis)      
        except(DateInterventionInvalide):
            pass    
        verify(self.commandes, never).append(self.commande)
        
    def test_Jane_cree_une_commande_mais_n_a_pas_le_droit_leve_une_exception(self):
        """Test Jane ajoute une commande, mais n'a pas le droit. Une exception est levee"""
        
        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(False)
        self.assertRaises(UtilisateurNonAutorise, self.service.ajouter_commande, self.createur, self.date, self.devis)
        
    def test_Jane_cree_une_commande_mais_n_a_pas_le_droit_n_ajoute_pas(self):
        """Test Jane ajoute une commande, mais n'a pas le droit. L'ajout n'a alors pas lieu"""
        
        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(False)
        try:
            self.service.ajouter_commande(self.createur, self.date, self.devis)
        except(UtilisateurNonAutorise):
            pass
        verify(self.commandes, never).append(self.commande)
        
class TestJaneCreeUnDevis(unittest.TestCase):
    
    def setUp(self):
        self.prestations = mock()
        self.storage = mock()
        self.devis = Devis(self.prestations, self.storage)
    
    def test_Jane_ajoute_une_prestation_existante_a_un_devis_prestation_ajoutee(self):
        """Test quand Jane ajoute une prestation existante a un devis, la prestation est bien ajoutee"""
        
        new_prestation = mock()
        when(new_prestation).exists().thenReturn(True)
        self.devis.addPrestation(new_prestation)
        verify(self.prestations).append(new_prestation)
    
    def test_Jane_ajoute_une_prestation_inexistante_a_un_devis_leve_une_exception(self):
        """Test quand Jane ajoute une prestation inexistante a un devis, une excpetion est levee"""
        
        new_prestation = mock()
        when(new_prestation).exists().thenReturn(False)
        self.assertRaises(PrestationInconnue, self.devis.addPrestation, new_prestation)    
    
    def test_Jane_ajoute_une_prestation_inexistante_a_un_devis_n_ajoute_rien_au_devis(self):
        """Test quand Jane ajoute une prestation inexistante a un devis, n ajoute rien au devis"""
        
        new_prestation = mock()
        when(new_prestation).exists().thenReturn(False)
        try:
            self.devis.addPrestation(new_prestation)
        except(PrestationInconnue):
            pass
        verify(self.prestations, never).append(new_prestation)
    
    def test_Jane_edite_son_devis_en_pdf(self):
        """Test l'edition d'un devis en pdf"""
        
        prestation = mock()
        when(self.prestations).select().thenReturn([prestation])
        when(prestation).description().thenReturn("My Description")
        when(prestation).cout_unitaire().thenReturn(90)
        pdf = self.devis.buildPDF()
        expected_output = "Devis\nMy Description - CU: 90euros"
        
        self.assertEqual(pdf, expected_output)
        
    def test_total_HT(self):
        """Test le calcul du total HT du devis"""
        
        prestation = mock()
        when(prestation).coutHT().thenReturn(45)
        
        prestation2 = mock()
        when(prestation2).coutHT().thenReturn(35)
        
        when(self.prestations).select().thenReturn([prestation, prestation2])
        totalHT = self.devis.computeTotalHT()
        expectedTotal = 80
        self.assertEqual(totalHT, expectedTotal)
        
    def test_total_TTC(self):
        """Test le calcul du total TTC du devis"""
        
        prestation = mock()
        when(prestation).coutHT().thenReturn(45)
        
        prestation2 = mock()
        when(prestation2).coutHT().thenReturn(35)
        
        when(self.prestations).select().thenReturn([prestation, prestation2])
        totalHT = self.devis.computeTotalTTC()
        expectedTotal = 96 
        self.assertEqual(totalHT, expectedTotal)
        
    def test_TauxTTC(self):
        """Test taux TTC"""
        
        taux = self.devis._tauxTTC()
        expected_taux = 1.2
        self.assertEqual(taux, expected_taux)
            
    def test_Jane_ajoute_un_devis_au_storage(self):
        """Test quand Jane ajoute une prestation existante a un devis, le devis est sauve dans la base"""
        
        self.devis.store()
        verify(self.storage).insert(self.devis)
        
            
    def test_Jane_ajoute_dans_un_devis_sauve_leve_exception(self):
        """Test quand Jane essaye d'ajouter dans un devis deja sauve, leve une exception"""
        
        new_prestation = mock()
        when(new_prestation).exists().thenReturn(True)
        when(self.storage).includes(self.devis).thenReturn(True)
        self.assertRaises(DevisFinalise, self.devis.addPrestation, new_prestation) 
        
    def test_Jane_ajoute_dans_un_devis_sauve_ajoute_pas(self):
        """Test quand Jane essaye de modifer un devis deja sauve, n'ajoute rien"""
        
        new_prestation = mock()
        when(new_prestation).exists().thenReturn(True)
        when(self.storage).includes(self.devis).thenReturn(True)
        try:
            self.devis.addPrestation(new_prestation)
        except(DevisFinalise):
            pass
        verify(self.prestations, never).append(new_prestation)