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
        if self.storage.includes(self):
            raise DevisFinalise
        self.prestations.append(prestation)
        
    def buildPDF(self, lib):
        return lib.build_output_for(self)
    
    def computeTotalHT(self):
        total = 0
        for prestation in self.prestations.select():
            total += prestation.coutHT()
        return total
        
    def computeTotalTTC(self, taux):
        total = 0
        ratio = 1.0+(taux/100)
        for prestation in self.prestations.select():
            total += prestation.coutHT()
        return total * ratio
        
    def store(self):
        if self.storage.includes(self):
            raise DevisFinalise
        self.storage.insert(self)
        
    def change_number_of_to(self, prestation, quantity):
        if not self.prestations.includes(prestation):
            raise PrestationInconnue
        if self.storage.includes(self):
            raise DevisFinalise            
        self.prestations.set_number_of_to(prestation, quantity)
        
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