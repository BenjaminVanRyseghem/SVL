

"""
John rend un livre

Pour emprunter un livre, je dois rendre les livres empruntes d'abord


"""

import unittest
from mockito    import mock
from mockito    import when
from mockito    import verify
from mockito    import never
from books      import ServiceEmprunt
from books      import EmpruntInexistant 

class TestUnMembreRendUnLivre(unittest.TestCase):
      
    def setUp(self):
        self.livre = mock()
        self.emprunt = mock()
        self.emprunts = mock()  
        self.litiges = mock()
        self.service = ServiceEmprunt(self.emprunts, self.litiges)
        
    def test_date_de_retour_respectee_alors_emprunt_clos(self):
 
        when(self.emprunts).find(self.livre).thenReturn(self.emprunt)
        when(self.emprunt).en_retard(self.livre).thenReturn(False)
        self.service.rendre(self.livre)
        verify(self.emprunt).clore()
        
    def test_date_de_retour_respectee_alors_pas_de_notification(self):
 
        when(self.emprunts).find(self.livre).thenReturn(self.emprunt)
        when(self.emprunt).en_retard(self.livre).thenReturn(False)
        self.service.rendre(self.livre)
        verify(self.litiges, never).notify(self.emprunt)
        
    def test_le_livre_n_est_pas_emprunte_alors_une_exception_est_leve(self):        

        when(self.emprunts).find(self.livre).thenRaise(ValueError)
        self.assertRaises(EmpruntInexistant, self.service.rendre, self.livre)

    def test_date_de_retour_depasse_alors_notification_litige(self):
 
        when(self.emprunts).find(self.livre).thenReturn(self.emprunt)
        when(self.emprunt).en_retard(self.livre).thenReturn(True)
        self.service.rendre(self.livre)
        verify(self.emprunt).clore()
        verify(self.litiges).notify(self.emprunt)
        
    def test_date_de_retour_depasse_alors_cloture(self):
 
        when(self.emprunts).find(self.livre).thenReturn(self.emprunt)
        when(self.emprunt).en_retard(self.livre).thenReturn(True)
        self.service.rendre(self.livre)
        verify(self.emprunt).clore()
        