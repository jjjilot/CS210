'''
Pizza Calculator - Lab 3
Author: Josh Jilot
Credits: Just Me :)
'''
import math
import doctest

def circle_area(diameter: int) -> float:
    '''
    Returns area of a circle given its diameter

    >>> circle_area(4)
    12.566
    >>> circle_area(6)
    28.274
    '''

    r = diameter / 2 
    area = math.pi * r**2
    area = round(area, 3)

    return area

def pizza_calculator(diameter, cost): 
    ''' 
    (int, num) -> float 

    Calculates and returns the cost per square inch 
    of pizza for a pizza of given diameter and cost. 
    Examples: 

    >>> pizza_calculator(14, 18) 
    0.117
    >>> pizza_calculator(14, 20.25)  
    0.132
    ''' 
    area = circle_area(diameter)
    
    cost_per_inch = cost / area 
    cost_per_inch = round(cost_per_inch, 3) 
    return cost_per_inch

print(doctest.testmod())
