"""

pendiente:
    incluir validaciones
    ajustar put
    

"""

from finderivatives import validations as val

#%%
class EuropeanOption():
    
    def __init__(self, strike, notional, maturity, position, premium=0):
        self._strike = val.validate_strike(strike)
        self._notional = val.validate_notional(notional)
        self._maturity = val.validate_maturity(maturity)
        self._dt = val.validate_maturity(maturity)
        self._position = val.validate_position(position)
        self._premium = val.validate_premium(premium)
        # self._flows = {}
    
    
    def __str__(self):
        return 'xxxxx'
    
    
#    def __add__(self, other):
#        payoff = self.payoff() + other.payoff()
#        profit = self.profit() + other.profit()
#        pricing_bs = self.pricing_bs() + other.pricing_bs()
#        addition = {
#            'payoff': payoff,
#            'profit': profit,
#            'pricing_bs': pricing_bs
#            }
#        return addition
    
    
    def get_strike(self):
        return self._strike
    
    
    def get_maturity(self):
        return self._maturity
    
    
    def get_position(self):
        return self._position
    
    
    def set_spot(self, spot):
        self._spot = val.validate_spot(spot)
    
    
    def set_volatility(self, vol):
        self._vol = vol
    
    
    def set_r(self, r):
        self._r = r
    
    
    def set_market_inputs(self, spot, vol, r):
        self.set_spot(spot)
        self.set_volatility(vol)
        self.set_r(r)
    


#%% Direct execution
if __name__ == '__main__':
    print(' Direct execution ... \n')
    