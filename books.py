
class ServiceEmprunt(object):
    
    def __init__(self, emprunts_dependency, litiges_dependency):
        self.emprunts = emprunts_dependency
        self.litiges = litiges_dependency
    
    def rendre(self, livre):
        try:
            emprunt = self.emprunts.find(livre)
        except(ValueError):
            raise EmpruntInexistant
        emprunt.clore()
        if emprunt.en_retard(livre):
            self.litiges.notify(emprunt)
        
class EmpruntInexistant(Exception):
    pass