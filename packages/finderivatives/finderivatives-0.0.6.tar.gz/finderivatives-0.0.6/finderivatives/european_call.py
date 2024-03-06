
import math as mt
import numpy as np
from scipy.stats import norm

from finderivatives.derivative import EuropeanOption


#%% Call
class Call(EuropeanOption):
    """Opcion Europea de Compra (Call)

    Args:
        strike (int, float or list): _description_
        maturity (int or float): _description_
        position (int or float): _description_
        premium (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike, notional, maturity, position, premium=0):
        super().__init__(strike, notional, maturity, position, premium)
        
        
    def payoff(self):
        """
        Función de pago del derivado a partir de uno o varios precios spot.
        
        🚧 ¡Under construction! 🚧

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._payoff = np.maximum(0, self._spot-self._strike) * self._position
        return self._payoff
    
    
    def profit(self):
        """
        Función del beneficio o perdida del derivado a partir de uno o varios precios spot.
        
        🚧 ¡Under construction! 🚧
        
        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._profit = self.payoff() - self._premium * self._position
        return self._profit
    
    
    def pricing_bs(self):
        """
        Función de valoración del derivado bajo el modelo de Black-Scholes.
        
        🚧 ¡Under construction! 🚧
        

        Returns
        -------
        TYPE
            Precio justo de la opción.

        """
        # Probabilities
        self._d1 = (np.log(self._spot/self._strike) + 
                    (self._r - (self._vol**2)/2) / self._dt) \
            / (self._vol * mt.sqrt(self._dt))
        self._d2 = self._d1 - self._vol * mt.sqrt(self._dt)
        self._n_d1 = norm.cdf(self._d1)
        self._n_d2 = norm.cdf(self._d2)
        # Pricing
        self._pricing = (
            self._spot * self._n_d1\
            - self._strike * np.exp(-self._r*(self._dt)) * self._n_d2
            ) * self._position
        return self._pricing
    
    
#%% Direct execution
if __name__ == '__main__':
    print(' Direct execution ... \n')
    