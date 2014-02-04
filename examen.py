import unittest
from mockito        import mock
from mockito        import verify
from mockito        import when
from mockito        import never

class TestJoeLeComptableEditeUneFacture(unittest.TestCase):
    
    def setUp(self):
        self.commande = mock()
        self.date = mock()
        self.service_comptable = mock()
        self.prestation = mock()
        self.delai = mock()
        
        when(self.commande).prestation().thenReturn(self.prestation)
        self.facture = Facture(self.commande, self.date, self.service_comptable)
        
        
    def test_edition_facture_non_deja_editee_apres_date_realisation_prestation_ajoute_au_service_comptable(self):
        """Test l'edition d'une facture apres la realisation de la prestation. La facture est ajoutee au service comptable"""
        
        """
        given   : une commande non editee
        when    : la facture est editee apres la date de realisation de la commande
        then    : la facture est ajoutee au service comptable
        """
        
        when(self.date).posterieur_a(self.prestation).thenReturn(True)
        when(self.commande).deja_editee().thenReturn(False)
        
        self.facture.edite(self.delai)
        verify(self.service_comptable).append(self.facture, self.delai)
    
    def test_edition_facture_non_deja_editee_avant_date_realisation_prestation_leve_une_exception(self):
        """Test l'edition d'une facture avant la date de realisation de la prestation. Une exception est levee (PrestationNonRealisee)"""
        
        """
        given   : une commande non editee
        when    : la facture est editee avant la date de realisation de la commande
        then    : une exception est levee (PrestationNonRealisee)
        """
        
        when(self.date).posterieur_a(self.prestation).thenReturn(False)
        when(self.commande).deja_editee().thenReturn(False)
        
        self.assertRaises(PrestationNonRealisee, self.facture.edite, self.delai)
        
    def test_edition_facture_non_deja_editee_avant_date_realisation_prestation_n_ajoute_pas_au_service_comptable(self):
        """Test l'edition d'une facture avant la date de realisation de la prestation. La facture n'est pas ajoutee"""
        
        """
        given   : une commande non editee
        when    : la facture est editee avant la date de realisation de la commande
        then    : la facture n'est pas ajoutee au service comptable
        """
        
        when(self.date).posterieur_a(self.prestation).thenReturn(False)
        when(self.commande).deja_editee().thenReturn(False)
        
        try: 
            self.facture.edite(self.delai)
        except(PrestationNonRealisee):
            pass
        verify(self.service_comptable, never).append(self.facture, self.delai)
        
    def test_edition_facture_deja_editee_apres_date_realisation_prestation_leve_une_exception(self):
        """Test l'edition d'une facture deja editee apres la date de realisation de la prestation. Une exception est levee (PrestationNonRealisee)"""
        
        """
        given   : une commande deja editee
        when    : la facture est editee apres la date de realisation de la commande
        then    : une exception est levee (FactureDejaEditee)
        """
        
        when(self.date).posterieur_a(self.prestation).thenReturn(True)
        when(self.commande).deja_editee().thenReturn(True)
        
        self.assertRaises(FactureDejaEditee, self.facture.edite, self.delai)
        
    def test_edition_facture_deja_editee_apres_date_realisation_prestation_n_ajoute_pas_au_service_comptable(self):
        """Test l'edition d'une facture deja editee apres la date de realisation de la prestation. La facture n'est pas ajoutee"""
        
        """
        given   : une commande deja editee
        when    : la facture est editee apres la date de realisation de la commande
        then    : la facture n'est pas ajoutee au service comptable
        """
        
        when(self.date).posterieur_a(self.prestation).thenReturn(True)
        when(self.commande).deja_editee().thenReturn(True)
        
        try: 
            self.facture.edite(self.delai)
        except(FactureDejaEditee):
            pass
        verify(self.service_comptable, never).append(self.facture, self.delai)
        
        
class Facture(object):
    
    def __init__(self, commande, date, service_comptable):
        self.commande = commande
        self.date = date
        self.service_comptable = service_comptable
        
    def edite(self, delai):
        if not (self.date.posterieur_a(self.commande.prestation())):
            raise PrestationNonRealisee
            
        if(self.commande).deja_editee():
            raise FactureDejaEditee
            
        return self.service_comptable.append(self, delai)
        
class PrestationNonRealisee(Exception):
    pass
    
class FactureDejaEditee(Exception):
    pass