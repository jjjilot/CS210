'''
10/20 - Lab 4
Author: Josh Jilot
Credit: Just me :)
'''

def hello(firstname: str): 
    ''' Prints a greeting to the specified name ''' 
    print("Hello, "+firstname+"!") 
    return None 

def ciao(firstname: str): 
    ''' Prints an Italian greeting to the specified name ''' 
    print("Ciao, "+firstname+"!") 
    return None

def Greeting(f, s):
    ''' Calls the specified greeting function for the specified name '''
    print(f'Calling {f.__name__}!')
    f(s)
    return None
