# code for plotting alphavantage stock price data using flask & bokeh 

import numpy as np
import pandas as pd
import requests
import json
import numpy as np 
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure, show
from bokeh.models import Range1d        # setting axis ranges
from bokeh.embed import components      # export to html
import os
from flask import Flask, request, render_template, redirect #abort, Response
# from dotenv import load_dotenv          # local method for API hidden key.
# load_dotenv()
# key = os.getenv('ALPHA_VANTAGE_API_KEY')

# set SECRET KEY for API using CLI: heroku config:set NAME=value
key = os.environ.get('ALPHA_VANTAGE_API_KEY', None)  

app = Flask(__name__)

def get_stock_data(ticker, key, outsize = 'compact'):
    method = 'TIME_SERIES_DAILY_ADJUSTED'
    url = 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize={}&apikey={}'\
    .format(method, ticker, outsize, key)
    response = requests.get(url)
    return response    

def format_price_data(ticker, year_window = 1, key = key, outsize = 'compact'):
    
    try: 
        response = get_stock_data(ticker, key, outsize)
        data = response.json()
        prices = pd.DataFrame(data['Time Series (Daily)']).T
        prices.columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume', 'dividend','split_coef']
        prices.index = pd.to_datetime(prices.index)
    
        # keep only a number of years of data from present
        latest_date = prices.index[0]
        start_date = (latest_date - relativedelta(years=year_window))
        date_range = [start_date, latest_date]
        prices = prices.loc[latest_date:start_date]
        #prices = prices.loc[year] 

    except: 
        prices = pd.DataFrame()
        
    return prices

def line_plot(df, ticker):

    # Bokeh widgets
    TOOLS = 'hover, crosshair, pan, wheel_zoom, box_zoom, reset, tap, save, box_select'
    
    # simple Bokeh plot
    plot = figure(x_axis_type = 'datetime', title = '{} adjusted daily closing price'.format(ticker), tools= TOOLS) # some tools given by default
    plot.grid.grid_line_alpha = 0.3
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Price (USD)'

    # set range, some unknown glitches w/o
    ymin = pd.to_numeric(df.adj_close).min()*0.95
    ymax = pd.to_numeric(df.adj_close).max()*1.05
    plot.y_range = Range1d(ymin, ymax)  
    
    # plot 1: lines
    plot.line(df.index, df['adj_close'], color='navy', line_width = 2)
    
    return plot

# flask code for single looped webpage
app.vars = {}
app.vars['ncycles'] = 0     # track n page cycles

@app.route('/stock_prices', methods = ['GET', 'POST'])

def stock():  
      
    # defaults for initial page loading, else get from POST
    if app.vars['ncycles'] == 0:
        ticker = 'QQQ'
        years_usr = 2

    else:
        ticker = app.vars['ticker']
        years_usr =  int(app.vars['years'])
           

    # get data & plot -- years function broken, will want outsize = full
    if request.method == 'GET':
        
        df = format_price_data(ticker, year_window = years_usr, key = key, outsize = 'full')

        # store initial data for display if error(s) occur
        if app.vars['ncycles'] == 0:
            app.vars['default_df'] = df.copy(deep=True)

        # Plot data w error handling by empty price data or null ticker
        bad_data = {}

        if df.empty == False:
            bad_data = False
            plot = line_plot(df, ticker)           # plot new data

        else: 
            bad_data = True #or ticker = ''
            default = 'QQQ'
            df_default = app.vars['default_df']    # get default data
            plot = line_plot(df_default, default)  # plot default data

        # return plot render data, page vars   
        script, div = components(plot)
        kwargs = {'script': script, 'div': div}
        kwargs['title'] = ticker

        # error messages to pass 
        if bad_data:
            kwargs['error_msg'] = '{}  -ERROR- try again.'.format(ticker)
            kwargs['error_detail'] = '''  Note: max of 5 requests/min.  
                If your ticker is valid, wait 1 min to retry.'''

        return render_template('index.html', **kwargs)   

    else:  # get POST vars, redirect
        app.vars['ncycles'] += 1
        app.vars['ticker'] = request.form['ticker']
        app.vars['years'] = request.form['years']        
        return redirect('/stock_prices')

if __name__ == '__main__':
    app.run(debug=True)