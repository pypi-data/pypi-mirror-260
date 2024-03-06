
import math as mt
import numpy as np
from scipy.stats import norm

from finderivatives.derivative import EuropeanOption


#%%  Put
class Put(EuropeanOption):
    
    def __init__(self, strike, notional, maturity, position, premium=0):
        super().__init__(strike, notional, maturity, position, premium)
    
    
    def payoff(self):
        """
        🚧 ¡Under construction! 🚧
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._payoff = np.maximum(0, self._strike-self._spot) * self._notional * self._position
        return self._payoff
    
    
    def profit(self):
        """
        🚧 ¡Under construction! 🚧
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._profit = self.payoff() - self._premium * self._notional * self._position
        return self._profit
    
    
    def pricing_bs(self):
        """
        🚧 ¡Under construction! 🚧
                

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # Probabilities
        self._d1 = (np.log(self._spot/self._strike) +
                    (self._r - (self._vol**2)/2) / self._dt) \
            / (self._vol * mt.sqrt(self._dt))
        self._d2 = self._d1 - self._vol * mt.sqrt(self._dt)
        self._n_d1 = norm.cdf(-self._d1)
        self._n_d2 = norm.cdf(-self._d2)
        # Pricing
        self._pricing = (
            self._strike * np.exp(-self._r*(self._dt)) * self._n_d2
            - self._spot * self._n_d1
            ) * self._notional * self._position 
        return self._pricing
    
    
#%% Direct execution
if __name__ == '__main__':
    print(' Direct execution ... \n')
    