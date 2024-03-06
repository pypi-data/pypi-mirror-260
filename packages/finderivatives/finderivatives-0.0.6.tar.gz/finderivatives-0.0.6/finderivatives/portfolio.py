


#%%
class Portfolio():
    
    def __init__(self, *derivatives):
        self._derivatives = derivatives
    
    
    def __str__(self):
        return 'xxxxx'
    
    
    def __add__(self, other):
        addition = Portfolio(*self.get_derivatives(), *other.get_derivatives())
        return addition
    
    
    def get_derivatives(self):
        """
        🚧 ¡Under construction! 🚧
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self._derivatives
    
    
    def set_market_inputs(self, spot, vol, r):
        """
        🚧 ¡Under construction! 🚧
        

        Parameters
        ----------
        spot : TYPE
            DESCRIPTION.
        vol : TYPE
            DESCRIPTION.
        r : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        for derivative in self._derivatives:
            derivative.set_market_inputs(spot, vol, r)
    
    
    def payoff(self):
        """
        🚧 ¡Under construction! 🚧
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._payoff = 0
        for derivative in self._derivatives:
            self._payoff += derivative.payoff()
        
        return self._payoff
    
    
    def profit(self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._profit = 0
        for derivative in self._derivatives:
            self._profit += derivative.profit()
        
        return self._profit
    
    
    def pricing_bs(self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self._pricing = 0
        for derivative in self._derivatives:
            self._pricing += derivative.pricing_bs()
        
        return self._pricing



#%% Direct execution
if __name__ == '__main__':
    print(' Direct execution ... \n')
    