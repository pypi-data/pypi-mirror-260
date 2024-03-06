
from finderivatives import validations as val

class UnderlyingAsset():
    
    def __init__(self, notional, position):
        self._notional = val.validate_notional(notional)
        self._position = val.validate_position(position)
        
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
    
    def payoff(self):
        """
        🚧 ¡Under construction! 🚧

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._payoff = self._spot * self._notional * self._position
        return self._payoff
    
    
    def profit(self):
        """
        🚧 ¡Under construction! 🚧

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._profit = self._spot * self._notional * self._position
        return self._profit
    
    
    def pricing_bs(self):
        """
        🚧 ¡Under construction! 🚧

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._pricing = self._spot * self._notional * self._position
        return self._pricing




