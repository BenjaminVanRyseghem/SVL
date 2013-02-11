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
        
        """
        given   : un devis valide, une date d'intervention valide, un utilisateur autorise
        when    : ajoute le devis avec la date d'intervention dans une commande
        then    : la commande est cree et ajoutee a la liste des commandes
        """

        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(True)
        self.service.ajouter_commande(self.createur, self.date, self.devis)
        verify(self.commandes).append(self.commande)
        
    def test_Jane_cree_une_commande_pour_un_devis_invalide_et_une_date_d_intervention_correcte_leve_une_exception(self):
        """Test l'ajout d'une commande avec un devis invalide. Une exception est alors levee"""
        
        """
        given   : un devis invalide, une date d'intervention valide, un utilisateur autorise
        when    : ajoute le devis avec la date d'intervention dans une commande
        then    : une exception est leve car le devis est invalide (DevisInvalide)
        """
        
        when(self.devis).expire().thenReturn(True)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(True)
        self.assertRaises(DevisInvalide, self.service.ajouter_commande, self.createur, self.date, self.devis)
        
    def test_Jane_cree_une_commande_pour_un_devis_invalide_et_une_date_d_intervention_correcte_n_ajoute_pas(self):
        """Test l'ajout d'une commande avec un devis invalide. L'ajout n'a alors pas lieu"""        
        
        """
        given   : un devis invalide, une date d'intervention valide, un utilisateur autorise
        when    : ajoute le devis avec la date d'intervention dans une commande
        then    : la commande n'est pas ajoutee a la liste des commandes
        """
        
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
        
        """
        given   : un devis valide, une date d'intervention invalide, un utilisateur autorise
        when    : ajoute le devis avec la date d'intervention dans une commande
        then    : une exception est levee car la date est invalide (DateInterventionInvalide)
        """
        
        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(True)
        when(self.createur).peut_creer_commandes().thenReturn(True)        
        self.assertRaises(DateInterventionInvalide, self.service.ajouter_commande, self.createur, self.date, self.devis)
        
    def test_Jane_cree_une_commande_pour_un_devis_valide_et_une_date_d_intervention_incorrecte_n_ajoute_pas(self):
        """Test l'ajout d'une commande avec une date invalide. L'ajout n'a alors pas lieu"""
        
        """
        given   : un devis valide, une date d'intervention invalide, un utilisateur autorise
        when    : ajoute le devis avec la date d'intervention dans une commande
        then    : la commande n'est pas ajoutee a la liste des commandes
        """
        
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
        
        """
        given   : un devis valide, une date d'intervention valide, un utilisateur non autorise
        when    : ajoute le devis avec la date d'intervention dans une commande
        then    : une exception est levee car l'utilisateur n'a pas les droits de creation de commandes (UtilisateurNonAutorise)
        """
        
        when(self.devis).expire().thenReturn(False)
        when(self.date).expire().thenReturn(False)
        when(self.createur).peut_creer_commandes().thenReturn(False)
        self.assertRaises(UtilisateurNonAutorise, self.service.ajouter_commande, self.createur, self.date, self.devis)
        
    def test_Jane_cree_une_commande_mais_n_a_pas_le_droit_n_ajoute_pas(self):
        """Test Jane ajoute une commande, mais n'a pas le droit. L'ajout n'a alors pas lieu"""
        
        """
        given   : un devis valide, une date d'intervention valide, un utilisateur non autorise
        when    : ajoute le devis avec la date d'intervention dans une commande
        then    : la commande n'est pas ajoutee a la liste des commandes
        """
        
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
        
        """
        given   : une prestation valide (proposee par l'entreprise), un devis non finalise
        when    : ajoute la prestation au devis
        then    : l'ensemble des prestations du devis contient la prestation
        """
        
        new_prestation = mock()
        when(self.storage).includes(self.devis).thenReturn(False)
        self.devis.addPrestation(new_prestation)
        verify(self.prestations).append(new_prestation)

    def test_Jane_edite_son_devis_en_pdf(self):
        """Test l'edition d'un devis en pdf"""
        
        """
        given   : un devis contenant des prestations
        when    : edite le devis en pdf
        then    : la version pdf contient un recapitulatif des prestations sous la forme "#{nom} - CU: #{PU}euros"
        """
            
        prestation = mock()
        lib = mock()
        when(self.prestations).select().thenReturn([prestation])
        
        self.devis.buildPDF(lib)
        verify(lib).build_output_for(self.devis)
        
    def test_total_HT(self):
        """Test le calcul du total HT du devis"""
        
        """
        given   : un devis contenant des prestations
        when    : calcule le total HT du devis
        then    : retourne la somme HT de l'ensemble des prestations contenues dans le devis
        """
        
        prestation = mock()
        when(prestation).coutHT().thenReturn(45)
        
        prestation2 = mock()
        when(prestation2).coutHT().thenReturn(35)
        
        when(self.prestations).select().thenReturn([prestation, prestation2])
        totalHT = self.devis.computeTotalHT()
        expectedTotal = 80
        self.assertEqual(expectedTotal, totalHT)
        
    def test_total_TTC(self):
        """Test le calcul du total TTC du devis"""
        
        """
        given   : un devis contenant des prestations
        when    : calcule le total TTC du devis
        then    : retourne la somme TTC de l'ensemble des prestations contenues dans le devis
        """
        
        prestation = mock()
        when(prestation).coutHT().thenReturn(45)
        
        prestation2 = mock()
        when(prestation2).coutHT().thenReturn(35)
        
        when(self.prestations).select().thenReturn([prestation, prestation2])
        taux = 19.8
        totalTTC = self.devis.computeTotalTTC(taux)

        expectedTotal = 80 * 1.198
        self.assertEqual(expectedTotal, totalTTC)
        
    def test_Jane_sauve_un_devis_dans_le_storage(self):
        """Test quand Jane sauvegarde le devis dans la base"""
        
        """
        given   : un devis
        when    : sauve le devis dans la base
        then    : la base contient le devis
        """
        
        self.devis.store()
        when(self.storage).includes(self.devis).thenReturn(False)
        verify(self.storage).insert(self.devis)
        
    def test_Jane_sauve_un_devis__deja_sauve_dans_le_storage_leve_une_exception(self):
        """Test quand Jane sauvegarde le devis dans la base"""
        
        """
        given   : un devis deja sauve dans la base
        when    : sauve le devis dans la base
        then    : une exception est levee (DevisFinalise)
        """
        
        when(self.storage).includes(self.devis).thenReturn(True)
        self.assertRaises(DevisFinalise, self.devis.store)
        
    def test_Jane_sauve_un_devis__deja_sauve_dans_le_storage_leve_une_exception(self):
        """Test quand Jane sauvegarde le devis dans la base"""
        
        """
        given   : un devis
        when    : sauve le devis dans la base
        then    : la base ne re-ajoute pas le devis
        """
        
        when(self.storage).includes(self.devis).thenReturn(True)
        try:
            self.devis.store()
        except(DevisFinalise):
            pass
        verify(self.storage, never).insert(self.devis)
        
            
    def test_Jane_ajoute_dans_un_devis_sauve_leve_exception(self):
        """Test quand Jane essaye d'ajouter dans un devis deja sauve, leve une exception"""
        
        """
        given   : une prestation valide, un devis sauve dans la base
        when    : on ajoute la prestation au devis
        then    : leve une exception (DevisFinalise)
        """
        
        new_prestation = mock()
        when(self.storage).includes(self.devis).thenReturn(True)
        self.assertRaises(DevisFinalise, self.devis.addPrestation, new_prestation) 
        
    def test_Jane_ajoute_dans_un_devis_sauve_ajoute_pas(self):
        """Test quand Jane essaye de modifer un devis deja sauve, n'ajoute rien"""
        
        """
        given   : une prestation valide, un devis sauve dans la base
        when    : on ajoute la prestation au devis
        then    : la prestation n'est pas ajoutee au devis
        """
        
        new_prestation = mock()
        when(self.storage).includes(self.devis).thenReturn(True)
        try:
            self.devis.addPrestation(new_prestation)
        except(DevisFinalise):
            pass
        verify(self.prestations, never).append(new_prestation)
        
    def test_Jane_modifie_quantite_prestation_existante_dans_un_devis_non_sauve(self):
        """test la modifiaction d'une prestation existante dans un devis non sauve"""
        
        """
        given   : un devis non sauve dans la base et une prestation qui est dans le devis
        when    : on modifie la quantite de la prestation du devis
        then    : la quantite est modifiee
        """
        
        prestation = mock()   

        new_quantity = 5
        when(self.prestations).includes(prestation).thenReturn(True)
        self.devis.change_number_of_to(prestation, new_quantity)
        verify(self.prestations).set_number_of_to(prestation, new_quantity)
        
    def test_Jane_modifie_quantite_prestation_inexistante_dans_un_devis_non_sauve_leve_une_exception(self):    
        """test la modification de la quantite d'une prestation qui n'apparait pas sur un devis non finalise. Une exception est levee"""
        
        """
        given   : un devis non sauve dans la base et une prestation non presente sur le devis
        when    : on modifie la quantite
        then    : leve une exception (PrestationInconnue)
        """
        
        prestation = mock()   
        when(self.prestations).includes(prestation).thenReturn(False)
        new_quantity = 5
        self.assertRaises(PrestationInconnue, self.devis.change_number_of_to, prestation, new_quantity)
        
    def test_Jane_modifie_quantite_prestation_inexistante_dans_un_devis_non_sauve_ne_modifie_pas(self):    
        """test la modification de la quantite d'une prestation qui n'apparait pas sur un devis non finalise. La quantite n'est pas modifiee (pas de sens de toute facon)"""
        
        """
        given   : un devis non sauve dans la base et une prestation non presente sur le devis
        when    : on modifie la quantite
        then    : la quantite n'est pas modifiee
        """
        
        prestation = mock()   
        when(self.prestations).includes(prestation).thenReturn(False)
        new_quantity = 5
        try:
            self.devis.change_number_of_to(prestation, new_quantity)
        except (PrestationInconnue):
            pass
        verify(self.prestations, never).set_number_of_to(prestation, new_quantity)
        
    def test_Jane_modifie_quantite_prestation_existante_dans_un_devis_sauve_leve_une_exception(self):    
        """test la modification de la quantite d'une prestation qui apparait sur un devis finalise. Une exception est levee"""
        
        """
        given   : un devis sauve dans la base et une prestation presente sur le devis
        when    : on modifie la quantite
        then    : leve une exception (DevisFinalise)
        """
        
        prestation = mock()   
        when(self.prestations).includes(prestation).thenReturn(True)
        when(self.storage).includes(self.devis).thenReturn(True)
        new_quantity = 5
        self.assertRaises(DevisFinalise, self.devis.change_number_of_to, prestation, new_quantity)
        

    def test_Jane_modifie_quantite_prestation_existante_dans_un_devis_sauve_leve_ne_modifie_pas(self):    
        """test la modification de la quantite d'une prestation qui apparait sur un devis finalise. La quantite n'est pas modifiee"""
        
        """
        given   : un devis sauve dans la base et une prestation presente sur le devis
        when    : on modifie la quantite
        then    : la quantite n'est pas modifiee
        """
        
        prestation = mock()   
        when(self.prestations).includes(prestation).thenReturn(True)
        when(self.storage).includes(self.devis).thenReturn(True)
        new_quantity = 5
        try:
            self.devis.change_number_of_to(prestation, new_quantity)
        except (DevisFinalise):
            pass
        verify(self.prestations, never).set_number_of_to(prestation, new_quantity)
    