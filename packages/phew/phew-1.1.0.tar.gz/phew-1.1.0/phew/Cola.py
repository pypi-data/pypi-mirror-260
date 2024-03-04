import numpy as np

class Cola:
    """Returns movement of fund when Cost of living adjustment (COLA) is applied
    
    args:
        initial_fund (float) : initial amount
        data (list) : expected cpi/inflation values for the next periods
        method (str) : 'cpi','inflation'
    """
    
    def __init__(self,initial_fund : float,data : list,method : str = 'cpi'):
        
        self.initial_fund = initial_fund
        self.data = data
        self.method = method
        
    def fund_growth(self): 
        """Returns movement fund
        
        Returns:
            float : expected fund values
        """
        
        if self.method == 'cpi':
            
            fund_rates = []
            
            for i,y in zip(self.data,list(range(len(self.data)))):

                if len(fund_rates) == 0:
                    fund_rates.append(i)      
                else:
                    fund_rates.append(i * np.array(fund_rates)[y-1])

            return self.initial_fund * np.array(fund_rates)
        
        elif self.method == 'inflation':
            
            fund_rates = []
            
            for i,y in zip(self.data,list(range(len(self.data)))):
            
                if len(fund_rates) == 0:
                    fund_rates.append(1 + i)
                else:
                    fund_rates.append((1 + i) * np.array(fund_rates)[y-1])
            
            return self.initial_fund * np.array(fund_rates)