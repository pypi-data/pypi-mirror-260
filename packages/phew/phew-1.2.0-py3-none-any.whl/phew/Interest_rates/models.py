class vasicek():

    """Returns functions for simulating evolution of interest rates using vasicek model
    
    args:
        data (list) : interest rate data
        number_of_prediction_points (int) : number of prediction points
    """
    
    def __init__(self,data : list,number_of_prediction_points : int):
        self.data = data
        self.number_of_prediction_points = number_of_prediction_points
        self.mean_reversion = None
        self.drift = None
        self.volatility = None
        self.interest_rate_now = self.data[len(self.data)-1]
        self.ols_model = None
        
    def fit(self):
        """Calibration of the model"""
        
        import statsmodels.formula.api as sm
        import pandas as pd
        
        rates = pd.DataFrame({'Rates':self.data})
        rates['Diff'] = rates.diff()
        rates['Lag'] = rates['Rates'].shift()
        
        model =sm.ols('Diff~Lag',data = rates)
        results = model.fit()
        
        self.ols_model = results
        
        self.mean_reversion = abs(results.params.Lag)
        self.drift = (results.params.Intercept) / self.mean_reversion
        self.volatility = results.mse_resid ** (1/2)
    
    def expectation(self):
        """Returns expected rate today
        
        Returns:
            list: expected rate today
        """
        
        import math
        
        forecasts_rt = []
        
        for i in list(range(1,self.number_of_prediction_points + 1)):
            expected_rate = self.interest_rate_now * math.exp(-self.mean_reversion*i) + self.drift*(1 - math.exp(-self.mean_reversion*i))
            forecasts_rt.append(expected_rate)
            
        return forecasts_rt
    
    def variance(self):
        """Returns variance of the rate today
        
        Returns:
            list: variance
        """
            
        import math
        
        variance_rt = []
        
        for i in list(range(1,self.number_of_prediction_points + 1)):
            rate_dev = ((self.volatility ** 2)/2*self.mean_reversion) * (1 - math.exp(-2 * self.mean_reversion*i))
            variance_rt.append(rate_dev)
        
        return variance_rt
    
    def ols_model_results(self):
        """Returns statistics for ols model used in calibration
        
        Returns:
            object: Returns statistics for ols model used in calibration
        """
        print(self.ols_model.summary())