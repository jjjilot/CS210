def bowtie(length):
    '''
    draws a bowtie (yay!)

    >>> bowtie(1)
    *
    >>> bowtie(3)
    ***
    **
    *
    **
    ***
    '''
    if length <= 0:
        return
    elif length == 1:
        print('*')
    else:
        print('*' * length)
        bowtie(length - 1)
        print('*' * length)

def count_vowels(string):
    '''
    return number of vowels in string

    >>> count_vowels('abc de')
    2
    >>> count_vowels('Hi Everyone!')
    5
    '''
    vowels = ['A', 'E', 'I', 'O', 'U']
    if len(string) == 0:
        return 0
    elif string[0].upper() in vowels:
        return 1 + count_vowels(string[1:])
    else:
        return count_vowels(string[1:])

def is_list(var) -> bool:
    return isinstance(var, list)

def deep_reverse(a):
    '''
    reverse a list and any lists within that
    list and any lists within that list and...
    
    >>> deep_reverse([1, 2, 3])
    [3, 2, 1]
    >>> deep_reverse([1, [2, 3], 4])
    [4, [3, 2], 1]
    >>> deep_reverse([1, [2, [3, 4], [5, [6, 7], 8]]])
    [[[8, [7, 6], 5], [4, 3], 2], 1]
    '''
    if is_list(a):
        a.reverse()
    for element in a:
        if is_list(element):
            deep_reverse(element)
    return a

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print('Doctests Complete!')
