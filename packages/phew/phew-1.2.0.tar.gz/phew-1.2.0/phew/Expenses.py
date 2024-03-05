from scipy import stats
import numpy as np

class Expenses():
    
    """Returns expenses allocation
    
    args:
        mean_expenses (float) : x
        variance_expenses (float) : y
        fund_amount (float) : total fund value
    """
    
    def __init__(self,mean_expenses : float,variance_expenses : float,fund_amount:float):
        self.mean_expenses = mean_expenses
        self.variance_expenses = variance_expenses
        self.fund_amount = fund_amount
        
    def montecarlo(self,alpha : int,number_of_replications:int):
        """Returns optimal expense ratio and variance after running Monte Carlo where expenses is assumed to follow pareto distribution
        
        args:
            alpha (int) : alpha
            number_of_replications (int) : number of replications
            
         Returns:
             dict : optimal_ratio, ratio_output,expense_output
        """
        
        ratio_output_ = []
        expense_output_ = []
        
        for expense in stats.pareto.rvs(loc = self.mean_expenses - 2 * self.variance_expenses,scale = self.variance_expenses,b = alpha,size = number_of_replications):
            ratio_output_.append(expense/self.fund_amount)
            expense_output_.append(expense)
            
        optimal_ratio = np.array(ratio_output_).mean()
        
        return {'optimal_ratio':optimal_ratio,'ratio_output':ratio_output_,'expense_output':expense_output_}
        