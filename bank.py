class Account(object):
    
    def __init__(self, storage):
        self.operations = storage
        
    def historique(self):
        return list(self.operations.select())
            
    def balance(self):
        """Retourne le solde courant du compte
        """
        return sum(self.operations.select())
        
    def _negative_value_raises_an_error(self,value):    
        if not self.can_accept_credit(value):
            raise ValueError("The value should be positive. You have provided {0}".format(value))    
        
    def credit(self, value):
        """Credite le compte courant de value
        
        ValueError si value est negatif
        """
        self._negative_value_raises_an_error(value)
        self.operations.insert(value);
        
    def debit(self, value):
        """Debite le compte courant de value
        
        ValueError si value est negatif
        """
        self._negative_value_raises_an_error(value)
        current_balance = self.balance()
        if self.balance() < value:
            raise ValueError("Value os bigger than the current balance")
        self.operations.insert(-value);
        
    def can_accept_credit(self, value):
        """Retourne vrai si j'autorise un credit de value"""
        return value >= 0
        
class Transfert(object):
    """Class managing transfers between two accounts."""
    def __init__(self, src, dest):
        self.source = src
        self.destination = dest
        
    def transfer(self, amount):
        """Transfer amount from source to destination"""
        if not self.destination.can_accept_credit(amount):
            raise ValueError("Destination account can not accept a credit of {0}".format(amount))
        self.source.debit(amount)
        self.destination.credit(amount)