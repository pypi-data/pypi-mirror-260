class compute():
    """Returns formulae for interest rates"""
    
    def nominal_interest_rate(real_interest_rate : float,inflation_rate : float):
        """Returns nominal interest rate by adding real interest rate to inflation rate
        
        args:
            real_interest_rate (float) : interest rate adjusted for inflation
            inflation rate (float) : rate of prices increase
            
        Returns:
            float : nominal interest rate
        """
        return real_interest_rate + inflation_rate
    
    def real_interest_rate(nominal_interest_rate : float,inflation_rate : float):
        """Returns real interest rate by subtracting inflation rate from nominal interest rate
        
        args:
            nominal_interest_rate (float) : real interest rate plus inflation
            inflation_rate (float) : rate of prices increase
            
        Returns:
            float : real interest rate
        """
        return nominal_interest_rate - inflation_rate
    
    def inflation_rate(real_interest_rate : float,nominal_interest_rate : float):
        """Returns inflation rate by subtracting real interest rate from nominal interest rate
        
        args:
            real_interest_rate (float) : interest rate adjusted for inflation
            nominal_interest_rate (float) : real interest rate plus inflation
            
        Returns:
            float : inflation rate
        """
        return nominal_interest_rate - real_interest_rate
    
    def effective_interest_rate(nominal_interest_rate : float, number_of_compounding_periods : int):
        """Returns effective interest rate converted from nominal interest rate
        
        args:
            nominal_interest_rate (float) : real interest rate plus inflation
            number_of_compounding_periods (int) : number of compounding periods
            
        Returns:
            float : effective interest rate
        """
        return ((1 + nominal_interest_rate/number_of_compounding_periods)**number_of_compounding_periods) -1