
from finderivatives.european_call import Call
from finderivatives.european_put import Put
from finderivatives.portfolio import Portfolio
from finderivatives.underlying import UnderlyingAsset
from finderivatives import validations as val

#%% Covered Call
class CoveredCall(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike (_type_): _description_
        maturity (_type_): _description_
        premium (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike, notional, maturity, premium=0):
        self._call = Call(strike=strike,
                          notional=notional,
                          maturity=maturity,
                          position=-1,
                          premium=premium)
        self._underlying = UnderlyingAsset(notional=notional, position=1)
        super().__init__(self._call, self._underlying)
    


#%% Reverse Covered Call

class ReverseCoveredCall(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike (_type_): _description_
        maturity (_type_): _description_
        premium (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike, notional, maturity, premium=0):
        self._call = Call(strike=strike,
                          notional=notional,
                          maturity=maturity,
                          position=1,
                          premium=premium)
        self._underlying = UnderlyingAsset(notional=notional, position=-1)
        super().__init__(self._call, self._underlying)


#%% Protective Put

class ProtectivePut(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike (_type_): _description_
        maturity (_type_): _description_
        premium (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike, notional, maturity, premium=0):
        self._put = Put(strike=strike,
                        notional=notional,
                          maturity=maturity,
                          position = 1,
                          premium = premium)
        self._underlying = UnderlyingAsset(notional=notional, position=1)
        super().__init__(self._put, self._underlying)

#%% Reverse Protective Put


class ReverseProtectivePut(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike (_type_): _description_
        maturity (_type_): _description_
        premium (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike, notional, maturity, premium=0):
        self._put = Put(strike=strike,
                        notional=notional,
                          maturity=maturity,
                          position = -1,
                          premium = premium)
        self._underlying = UnderlyingAsset(notional=notional, position=-1)
        super().__init__(self._put, self._underlying)



#%% Bull Spread

#### Bull Spread Call
class BullSpreadCall(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, notional, maturity, premium1=0, premium2=0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Less")
        self._call01 = Call(strike=strike1,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        
        self._call02 = Call(strike=strike2,
                            notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium2)
        
        super().__init__(self._call01, self._call02)
        
        

#### Bull Spread Put
class BullSpreadPut(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, notional, maturity, premium1=0, premium2=0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Less")
        self._put01 = Put(strike=strike1,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._put02 = Put(strike=strike2,
                          notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium2)
        super().__init__(self._put01, self._put02)
        
        

#%% Bear Spread

#### Bear Spread Call
class BearSpreadCall(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, notional, maturity, premium1=0, premium2=0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Greater")
        self._call01 = Call(strike=strike1,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._call02 = Call(strike=strike2,
                            notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium2)
        super().__init__(self._call01, self._call02)
        

#### Bear Spread Put
class BearSpreadPut(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, notional, maturity, premium1=0, premium2=0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Greater")
        self._put01 = Put(strike=strike1,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._put02 = Put(strike=strike2,
                          notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium2)
        super().__init__(self._put01, self._put02)


#%% Butterfly Spread

#### Butterfly Spread Call
    ###Precio de compra: X - a y X + a - Precio de venta: X 

class ButterflySpreadCall(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        strike3 (_type_): _description_
        strike4 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
        premium3 (int, optional): _description_. Defaults to 0.
        premium4 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, strike3, strike4, notional, maturity, premium1 = 0,
                 premium2 = 0, premium3 = 0, premium4 = 0):
        strike1, strike2, strike3, strike4 = val.validate_strikes_butterly(strike1, strike2, strike3, strike4)
        self._call01 = Call(strike=strike1,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._call02 = Call(strike=strike2,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium2)
        self._call03 = Call(strike=strike3,
                            notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium3)
        self._call04 = Call(strike=strike4,
                            notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium4)
        super().__init__(self._call01, self._call02, self._call03, self._call04)
        
    

#### Butterfly Spread Put
class ButterflySpreadPut(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        strike3 (_type_): _description_
        strike4 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
        premium3 (int, optional): _description_. Defaults to 0.
        premium4 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, strike3, strike4, notional, maturity, premium1 = 0,
                 premium2 = 0, premium3 = 0, premium4 = 0):
        strike1, strike2, strike3, strike4 = val.validate_strikes_butterly(strike1, strike2, strike3, strike4)
        self._put01 = Put(strike=strike1,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._put02 = Put(strike=strike2,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium2)
        self._put03 = Put(strike=strike3,
                          notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium3)
        self._put04 = Put(strike=strike4,
                          notional=notional,
                            maturity=maturity,
                            position=-1,
                            premium=premium4)
        super().__init__(self._put01, self._put02, self._put03, self._put04)


#%% Straddle
    #### Precios de strike iguales
    
class StraddleSpread(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, notional, maturity, premium1 = 0, premium2 = 0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Equal")
        self._call01 = Call(strike=strike1,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._put01 = Put(strike=strike2,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium2)
        super().__init__(self._call01, self._put01)


#%% Strip

class StripSpread(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        strike3 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
        premium3 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, strike3, notional, maturity, premium1 = 0, 
                 premium2 = 0, premium3 = 0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Equal")
        strike1, strike3 = val.validate_strikes(strike1, strike3, "Equal")
        self._call01 = Call(strike=strike1,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        
        self._put01 = Put(strike=strike2,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium2)
        
        self._put02 = Put(strike=strike3,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium3)
        super().__init__(self._call01, self._put01, self._put02)


#%% Strap

class StrapSpread(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        strike3 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
        premium3 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, strike3, notional, maturity, premium1 = 0, 
                 premium2 = 0, premium3 = 0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Equal")
        strike1, strike3 = val.validate_strikes(strike1, strike3, "Equal")
        self._call01 = Call(strike=strike1,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._call02 = Call(strike=strike2,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium2)
        self._put01 = Put(strike=strike3,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium3)
        super().__init__(self._call01, self._call02, self._put01)

#%% Strangle
    
class StrangleSpread(Portfolio):
    """_summary_ 🚧 ¡Under construction! 🚧

    Args:
        strike1 (_type_): _description_
        strike2 (_type_): _description_
        maturity (_type_): _description_
        premium1 (int, optional): _description_. Defaults to 0.
        premium2 (int, optional): _description_. Defaults to 0.
    """
    def __init__(self, strike1, strike2, notional, maturity, premium1 = 0, premium2 = 0):
        strike1, strike2 = val.validate_strikes(strike1, strike2, "Greater")
        self._call01 = Call(strike=strike1,
                            notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium1)
        self._put01 = Put(strike=strike2,
                          notional=notional,
                            maturity=maturity,
                            position=1,
                            premium=premium2)
        super().__init__(self._call01, self._put01)




#%% Direct execution
if __name__ == '__main__':
    print(' Direct execution ... \n')
    