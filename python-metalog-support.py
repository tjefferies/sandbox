
# coding: utf-8

# In[58]:

import numpy as np
import pandas as pd

# YEAR: 2019
# COPYRIGHT HOLDER: Travis Jefferies

# Adapted from the R package `rmetalog` by Isaac J. Faber


# In[2]:

def quantileMetalog(a, y, t, bounds = (0,1), boundedness = 'u'):
    """
    TODO: write docstring
    """
    # TODO: write assertions
    
    f = y - 0.5
    l = np.log(y/(1-y))
    
    # For the first three terms
    x = a[0] + a[1] * l + a[2] * f * l

    # For the fourth term
    if t > 3:
        x = x + a[3] * f
    
    # Some tracking variables
    o = 2
    e = 2

    # For all other terms greater than 4
    if t > 4:
        for i in range(5,t+1):
            if i % 2 == 0:
                x = x + a[i] * np.power(f,e) * l
                e = e + 1

            if i % 2 != 0: 
                x = x + a[i] * np.power(f,o)
                o = o + 1
                
    if boundedness == 'sl':
        x = bounds[1] + np.exp(x)

    if boundedness == 'su':
        x = bounds[2] - np.exp(-x)

    if boundedness == 'b':
        x = (bounds[0] + bounds[1] * np.exp(x)) / (1 + np.exp(x))

    return(x)


# In[3]:

def pdfMetalog(a, y, t, bounds = (0,1), boundedness = 'u'):
    """
    TODO: write docstring
    """
    # TODO: write assertions
    
    d = y*(1-y)
    f = y - 0.5
    l = np.log(y/(1-y))
    
    # Initiate pdf

    # For the first three terms
    x = a[1] / d
    
    if a[2] != 0:
        x = x + a[2] * ((f/d) + l)
        
    # For the fourth term
    if t > 3:
        x = x + a[3]
        
    # Initalize some counting variables
    e = 1
    o = 1
    
    # For all other terms greater than 4
    if t > 4:
        for i in range(5,t+1):
            if i % 2 != 0:
                # iff odd
                x = x + ((o + 1) * a[i] * np.power(f,o))
                o = o + 1

            if i % 2 == 0:
                # iff even
                x = x + a[i] * (((np.power(f,(e + 1))) / d) + (e + 1) * (np.power(f,e)) * l)
                e = e + 1
                
    # Some change of variables here for boundedness

    x = np.power(x, -1)

    if boundedness != 'u':
        M = quantileMetalog(a, y, t, bounds = bounds, boundedness = 'u')

    if boundedness == 'sl':
        x = x * np.exp(-M)

    if boundedness == 'su':
        x = x * np.exp(M)

    if boundedness == 'b':
        x = x * (1 + np.power(np.exp(M),2)) / ((bounds[2] - bounds[1]) * np.exp(M))

    return(x)


# In[4]:

def pdfMetalogValidation(x):
    """
    TODO: write docstring
    """
    # TODO: write assertions
    
    y = min(x)
    if y >= 0:
        return 'yes'
    if y <0:
        return 'no'


# In[33]:

def flatten(items, seqtypes=(list, tuple)):
    """
    TODO: write docstring
    """
    # TODO: write assertions
    
    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i:i+1] = items[i]
    return items


# In[77]:

def pdf_quantile_builder(temp, y, term_limit, bounds, boundedness):
    """
    TODO: write docstring
    """
    
    # TODO: write assertions
    
    myList = dict()
    
    # Build pdf
    m = pdfMetalog(temp, y[1], term_limit, bounds = bounds,
                    boundedness = boundedness)
    
    for j in range(len(y)):
        tempPDF = pdfMetalog(temp, y[j], term_limit, bounds = bounds,
                            boundedness = boundedness)
        m = [m, tempPDF]
        
    # Build quantile values
    M = quantileMetalog(temp, y[1], term_limit, bounds = bounds,
                         boundedness = boundedness)

    for j in range(len(y)):
        tempQant = quantileMetalog(temp, y[j], term_limit, bounds = bounds,
                                  boundedness = boundedness)
        M = [M, tempQant]
        
    # Add trailing and leading zero's for pdf bounds
    
    if boundedness == 'sl':
        m = [0] + m
        M = [bounds[0]] + M

    if boundedness == 'su':
        m = m + [0]
        M = [M] + [bounds[1]]

    if boundedness == 'b':
        m = [0] + [m] + [0]
        M = [bounds[1]] + [M] + [bounds[2]]

    # Add y values for bounded models
    if boundedness == 'sl':
        y = [0] + [y]

    if boundedness == 'su':
        y = [y] + [1]

    if boundedness == 'b':
        y = [0] + [y] + [1]
    
    m = list(flatten(m))
    M = list(flatten(M))
    
    m = list(filter(lambda v: v==v, m))
    M = list(filter(lambda v: v==v, M))
    
    myList['m'] = m
    myList['M'] = M
    myList['y'] = y
    
    # PDF validation
    myList['valid'] = pdfMetalogValidation(myList['m'])

    return(myList)

