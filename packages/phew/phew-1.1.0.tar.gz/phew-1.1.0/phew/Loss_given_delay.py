import numpy as np
from scipy import stats

class Loss_given_delay:
    """Returns loss given a trip delay event
    
    args:
        number_of_days (list) : number of days in a year categorised by seasons
        ratio_of_workers_to_population (float) : probability of finding a formal sector worker in a bus
        carrying_capacity (int) : average carrying capacity for buses
        benefit (float) : benefit received at loss event
        expected_daily_delays_in_a_season (float) : expected daily delays categorised by seasons
    """
    
    def __init__(self,number_of_days : list,ratio_of_workers_to_population : float,carrying_capacity : int,benefit : float,expected_daily_delays_in_a_season : list):
        
        self.number_of_days = number_of_days
        self.ratio_of_workers_to_population = ratio_of_workers_to_population
        self.carrying_capacity = carrying_capacity
        self.benefit = benefit
        self.expected_daily_delays_in_a_season = expected_daily_delays_in_a_season
        self.expected_daily_loss_in_season = None
        self.expected_daily_claims_in_season = None
        self.expected_seasonal_loss = None
        
    def daily_loss_compute(self,number_of_replications : int):
        """Returns daily loss in seasons specified through Monte Carlo simulation
        
        args:
            number_of_replications (int) : number of replications
        
        Returns:
            dict : daily loss
        """
        
        expected_daily_loss_in_season_ = []
        expected_daily_claims_in_season_ = []
        
        delays_output = []
        monteCarlo_loss_output = []
        monteCarlo_claims_output = []
        
        
        for i in self.expected_daily_delays_in_a_season:
            
            losses = []
            daily_claims = []
            delays_rv = []
            
            for delays in stats.poisson.rvs(mu = i,size = number_of_replications):
                
                claims = self.ratio_of_workers_to_population * self.carrying_capacity * delays
                loss = self.ratio_of_workers_to_population * self.carrying_capacity * self.benefit * delays
                
                daily_claims.append(claims)
                losses.append(loss)
                delays_rv.append(delays)
                
            expected_daily_loss_in_season_.append(np.array(losses).mean())
            expected_daily_claims_in_season_.append(np.array(daily_claims).mean())
            
            delays_output.append(delays_rv)
            monteCarlo_loss_output.append(losses)
            monteCarlo_claims_output.append(daily_claims)
            
            
        self.expected_daily_loss_in_season = expected_daily_loss_in_season_
        self.expected_daily_claims_in_season = expected_daily_claims_in_season_
        
        return {'expected_daily_loss' : {'season {}'.format(y) : i for i,y in zip(self.expected_daily_loss_in_season,list(range(len(self.expected_daily_loss_in_season))))},'daily_losses_output' : {'season {}'.format(y) : i for i,y in zip(monteCarlo_loss_output,list(range(len(monteCarlo_loss_output))))},'daily_claims_output' : {'season {}'.format(y) : i for i,y in zip(monteCarlo_claims_output,list(range(len(monteCarlo_claims_output))))},'daily_delays_values' :  {'season {}'.format(y) : i for i,y in zip(delays_output,list(range(len(delays_output))))}}
    
    def seasonal_loss_compute(self,expected_daily_loss : list):
        """Returns seasonal loss
        
        args:
            expected_daily_loss (list) : expected daily loss computed
        
        Returns:
            dict : seasonal loss
        """
        
        if sum(self.number_of_days) == 365:
            self.expected_seasonal_loss = np.array(self.number_of_days) * np.array(expected_daily_loss)
            return {'season {}'.format(y) : i for i,y in zip(np.array(self.number_of_days) * np.array(expected_daily_loss),list(range(len(expected_daily_loss))))}
                           
        else:
            return "number of days should equal 365"
        
    def yearly_loss_compute(self,expected_loss_in_season : list):
        """Returns yearly loss
        
        args:
            expected_loss_in_season (list) : expected seasonal loss computed
        
        Returns:
            dict : yearly loss
        """
        
        if type(self.seasonal_loss_compute(self.expected_daily_loss_in_season)) == str:
            return "number of days should equal 365"
        
        return {'yearly loss': sum(expected_loss_in_season)}
    
    def expected_claims(self,time_frame : str = 'day'):
        """Returns expected claims in a day,season and year through Monte Carlo simulation
        
        args:
            time_frame (str) : 'day','season','year'
            
        Returns:
            dict : expected claims
        """
        
        if type(self.seasonal_loss_compute(self.expected_daily_loss_in_season)) == str:
            return "number of days should equal 365"
        
        else:
            if time_frame == 'day':

                return {'season {}'.format(y) : i for i,y in zip(np.array(self.expected_daily_claims_in_season),list(range(len(np.array(self.expected_daily_claims_in_season)))))}

            elif time_frame == 'season':

                return {'season {}'.format(y) : i for i,y in zip(np.array(np.array(self.expected_daily_claims_in_season) * self.number_of_days),list(range(len(np.array(np.array(self.expected_daily_claims_in_season) * self.number_of_days)))))}

            elif time_frame == 'year':

                return {'year' : sum(np.array(self.expected_daily_claims_in_season) * self.number_of_days)}