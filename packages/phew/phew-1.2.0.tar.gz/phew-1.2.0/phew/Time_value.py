class Time_value():
    
    """Returns time value of money"""
    
    def future_value(amount : float,interest_rate : float, periods : float):
        """Returns future value of an amount
        
        args:
            amount (float) : present value
            interest_rate (float) : interest rate
            periods (float) : number of periods
            
        Returns:
            float : future value
        """
        return amount * ((1 + interest_rate) ** periods )
        
    def present_value(amount : float,interest_rate : float, periods : float):
        """Returns present value of an amount
        
        args:
            amount (float) : future value
            interest_rate (float) : interest rate
            periods (float) : number of periods
            
        Returns:
            float :  present value
        """
        return amount * (1 / ((1 + interest_rate) ** periods))