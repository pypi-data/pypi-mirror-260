"""

"""

class PositionError(Exception):
    def __init__(self):
        self.value = None
        self.value_type = None
        self.message = 'The argument "position" must be of type int and take '\
            'the value of 1 or -1. For long position use 1 and for short '\
            'position use -1. '\
            '\nValue received: {value}, type: {value_type}.'
    
    
    def __str__(self):
        return self.message.format(value = self.value,
                                   value_type = self.value_type)
    
    
    def set_value_error(self, value):
        self.value = value
        self.value_type = type(value)



class StrikeError(Exception):
    def __init__(self):
        self.message = 'The argument "position" must be of type int and take '\
            'the value of 1 or -1. For long position use 1 and for short '\
            'position use -1.'
            
    
            

class SpotError(Exception):
    def __init__(self):
        self.value = None
        self.value_type = None
        self.message = 'The argument "spot" must be of type int, list, tuple '\
            'or darray. '\
            '\nValue received: {value}, type: {value_type}.'
    
    
    def __str__(self):
        return self.message.format(value = self.value,
                                   value_type = self.value_type)
    
    
    def set_value_error(self, value):
        self.value = value
        self.value_type = type(value)


#%% Direct execution
if __name__ == '__main__':
    print(' Direct execution ... \n')
    