class Premium():
    """Returns formulae to compute premium"""

    def pure_premium_1(loss : float,exposures : float):
        """Returns pure premium by dividing losses by exposures
        
        args:
            loss (float) : losses from an event
            exposures (float) : number of individuals exposed to the loss
            
        Returns:
            float : pure premium
        """
        
        return loss/exposures
    
    def pure_premium_2(frequency : float,severity : float):
        """Returns pure premium by multiplying frequency by severity
        
        args:
            frequency (float) : rate at which events are taking place
            severity (float) : magnitude of the loss from the event(s)
            
        Returns:
            float : pure premium
        """
        
        return frequency * severity
    
    def gross_rate(pure_premium : float,expense_ratio : float):
        """Returns gross rate
        
        args:
            pure_premium (float) : price of insurance that excludes expenses
            expense_ratio (float) : ratio of costs to total fund value
            
        Returns:
            float : price of a single unit of exposure
            
        """
        
        return pure_premium / (1 - expense_ratio)
    
    def expense_ratio(fund_costs : float,fund_assets : float):
        """Returns expense ratio by dividing costs by fund amount
        
        args:
            fund_costs (float) : fund expenses
            funds_assets (float) : total fund value
            
        Returns:
            float : expense ratio
        """
        
        return fund_costs/fund_assets
    
    def gross_premium(gross_rate : float,units : float):
        """Returns gross premium by multiplying gross rate by units
        
        args:
            gross_rate (float) : price of a single unit of exposure
            units (float) : number of units (purchases)
            
        Returns:
            float : gross premium
        """
        
        return gross_rate * units
        