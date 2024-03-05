class Annuity:
    """Returns time values of an annuity
    
    args:
        interest_rate (float) : interest rate
        number_of_terms (int) : number of periods
        amount (float : amount)
    """
    
    def __init__(self,interest_rate : float,number_of_terms : int,amount : float = 1):
        self.interest_rate = interest_rate
        self.number_of_terms = number_of_terms
        self.amount = amount
        
    def certain_present_value(self):
        """Returns present value of annuity certain
        
        Returns:
            float : present value for annuity certain
        """
        
        return self.amount*((1-(1+self.interest_rate)**(-self.number_of_terms))/self.interest_rate)
        
    def certain_future_value(self):
        """Returns future value of annuity certain
        
        Returns:
            float : future value for annuity certain
        """
        
        return self.amount*((((1+self.interest_rate)**self.number_of_terms)-1)/self.interest_rate)
        
    def due_present_value(self):
        """Returns present value of annuity due
        
        Returns:
            float : present value for annuity due
        """
        
        return self.amount*((1-(1+self.interest_rate)**(-self.number_of_terms))/(self.interest_rate/(self.interest_rate + 1)))
        
    def due_future_value(self):
        """Returns future value of annuity due
        
        Returns:
            float : future value for annuity due
        """
        
        return self.amount*((((1+self.interest_rate)**self.number_of_terms)-1)/(self.interest_rate/(self.interest_rate + 1)))