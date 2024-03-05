# phew

a library housing basic mathematical and statistical formulae used in insurance.

### Purpose

The primary objective of this package is to simulate pricing of trip delay insurance 
coverage for salaried formal sector workers in Malawi who take buses when traveling 
long distances. This package lays mathematical framework for calculation of losses 
associated with the delays and contains functions for calculation of different financial 
and economical variables.

### Features

+ Annuity
+ Cost of living adjustment (COLA)
+ Expenses
+ Loss given delay
+ Premium
+ Time value
+ Interest rates

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install phew.

```bash
pip install phew
```

### Usage (examples)

#### Annuity

present value of an annuity certain can be calculated by the code below

```python
>> from phew import Annuity
>> annuity = Annuity(interest_rate = 0.1,number_of_terms = 4,amount = 500)
>> annuity.certain_present_value()
>> 1584.9327231746472
```

#### Interest rates

effective annual rate of interest can be calculated by the code below

```python
>> from phew import Interest_rates
>> rate = Interest_rates.compute.effective_interest_rate(nominal_interest_rate = 0.12,number_of_compounding_periods = 12)
>> rate
>> 0.12682503013196977
```

#### COLA
Growth of a fund given inflation values can be estimated by the following code

```python
>> from phew import Cola
>> cola = Cola(initial_fund = 1000,data = [0.12,0.2,0.21],method = 'inflation')
>> cola.fund_growth()
>> array([1120.  , 1344.  , 1626.24])
```

#### Premium 

Gross rate can be calculated by the following code

```python
>> from phew import Premium
>> gross_rate = Premium.gross_rate(pure_premium = 2000,expense_ratio = 0.23)
>> gross_rate
>> 2597.402597402597
```


### About project

The author is not encouraging use of this package in production.  For more info, please, email the author.

### Author
+ Name : Precious Nliwasa
+ Email : preciousnliwasa8@gmail.com

### License

[MIT](https://choosealicense.com/licenses/mit/)
