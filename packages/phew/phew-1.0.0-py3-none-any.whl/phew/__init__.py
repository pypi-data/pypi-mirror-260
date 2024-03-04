""" 
The primary objective of this package is to simulate pricing of trip delay insurance coverage for salaried formal sector workers in Malawi who take buses when traveling long distances. The product is capable of providing benefits in a trip delay event as a way of managing unexpected expenses associated with the event. The product will be funded by tax and is being classified as a social travel insurance product. This package lays mathematical framework for calculation of losses associated with the delays and contains functions for calculation of different financial and economical variables. Social travel insurance plans have potential to incentivise workers to be productive. They can also be used as incentive for more takings of public transport which according to United Nations is one of the ways of reducing greenhouse gas emissions. Additionally, the work has potential to make social travel insurance become a well established academic discipline. For more information about the author visit https://preciousnliwasa.onrender.com
"""

from .Loss_given_delay import Loss_given_delay
from .Premium import Premium
from .Interest_rates import Interest_rates
from .Annuity import Annuity
from .Cola import Cola
from .Expenses import Expenses
from .Time_value import Time_value