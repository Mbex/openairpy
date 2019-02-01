"""
Set of functions for loading R and the R package Openair into python.
author: Michael Priestley
date: 2019-01-17 
"""


def loadOpenair():

    """
    import rpy2 functionality, prepare pandas for r objects and import openair
    """
    
    from rpy2.robjects.packages import importr
    openair = importr('openair')
    
    return openair


def pdtsdf2rtsdf(df):

    """
    convert pandas time series dataframe to r time series dataframe.
    wraps pandas2ri.py2ri() but takes care of datetime index for openair ts plotting
    df. pandas dataframe. 
    N.B. pd.DataFrame must have time series index!
    """
    from rpy2.robjects import pandas2ri

    pandas2ri.activate()
    r_df = df.copy()
    r_df['date'] = r_df.index
    r_df = pandas2ri.py2ri(r_df)

    return r_df


def displayOpenairPlot(func, figsize=(10,10), res=150, *args, **kwargs):
       
    """
    Displays openair plots inline.
    func. openair callback.
    figsize. tuple. figure size
    res. int. resolution of figure
    **kwargs. to be passed to func.

    -------------example of useage--------------------------------------
    >    from openairpy import OpenairPy
    >    openair = OpenairPy.loadOpenair()
    >    func = openair.corPlot
    >    OpenairPy.displayOpenairPlot(func, mydata=df, dendrogram=True)
    --------------------------------------------------------------------
    """

    import IPython
    from rpy2.robjects.lib import grdevices    

    pixel_per_inch = 0.0104166667
    width, height =figsize[0]/pixel_per_inch, figsize[1]/pixel_per_inch   
    with grdevices.render_to_bytesio(grdevices.png, width=width, height=height, res=res) as img:
        plot = func(*args, **kwargs)
    IPython.display.display(IPython.display.Image(data=img.getvalue(), format='png', embed=True))
    
    return None