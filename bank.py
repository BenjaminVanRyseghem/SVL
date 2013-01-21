class Account(object):
    
    def __init__(self):
        self.operations = list()
        
    def historique(self):
        return list(self.operations)
            
    def balance(self):
        return sum(self.operations)
        
    def credit(self, value):
        if value < 0:
            raise ValueError("The value should be positive. You have provided {0}".format(value))
        self.operations.append(value);
        
    def debit(self, value):
        if value < 0:
            raise ValueError("The value should be positive. You have provided {0}".format(value))
        if self.balance() < 0:
            raise ValueError("Balance negative")
        self.operations.append(-value);
        