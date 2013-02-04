class ServiceCommande(object):
    
    def __init__(self, commandes_dependency, fabrique):
        self.commandes = commandes_dependency
        self.fabrique = fabrique
        
    def devis_valide(self, devis):
        return not devis.expire()
        
    def date_valide(self, date):
        return not date.expire()
        
    def createur_valide(self, createur):
        return createur.peut_creer_commandes()
    
    def ajouter_commande(self, createur, date, devis):
        if not self.createur_valide(createur):
            raise UtilisateurNonAutorise
        if not self.devis_valide(devis):
            raise DevisInvalide
        if not self.date_valide(date):
            raise DateInterventionInvalide
        commande = self.fabrique.nouvelle_commande(createur, date, devis)   
        self.commandes.append(commande)
        
        
class Devis(object):
    
    def __init__(self, prestations, storage):
        self.prestations = prestations
        self.storage = storage

    def addPrestation(self, prestation):
        if not prestation.exists():
            raise PrestationInconnue
        if self.storage.includes(self):
            raise DevisFinalise
        self.prestations.append(prestation)
        
    def buildPDF(self):
        string = "Devis"
        for prestation in self.prestations.select():
            string += "\n"+prestation.description()+ " - CU: "+ str(prestation.cout_unitaire())+"euros"
        return string
    
    def computeTotalHT(self):
        total = 0
        for prestation in self.prestations.select():
            total += prestation.coutHT()
        return total
        
    def _tauxTTC(self):
        return 1.2
        
    def computeTotalTTC(self):
        total = 0
        for prestation in self.prestations.select():
            total += prestation.coutHT()
        return total * self._tauxTTC()
        
    def store(self):
        self.storage.insert(self)
        
class DevisInvalide(Exception):
    pass
    
class DateInterventionInvalide(Exception):
    pass
    
class UtilisateurNonAutorise(Exception):
    pass
    
class PrestationInconnue(Exception):
    pass
    
class DevisFinalise(Exception):
    pass