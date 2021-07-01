## Plot your favorite stocks 
This learning project creates a simple (unattractive) python web app to generate interactive plots for prices of stocks selected by the user. In the main application stocks.py, data is obtained from the AlphaVantage API, plotted using bokeh, and a page is generated and refreshed using Flask and html /templates. Other files support the site deployment on Heroku, including the Procfile, runtime.txt, and requirements.txt.

The deployed application ['stock-stock-stock'](https://stock-stock-stock.herokuapp.com/) can be viewed and used on [Heroku](http://heroku.com/).

If you were looking for a fully featured site to plot stock price movements this is not it.[TradingView](https://www.tradingview.com/) is popular and has many good features.


#### limitations / caveats
Styling on the webpage is barebones for this practice exerise on building an interactive application using [Flask](https://flask.palletsprojects.com/) (page buidling) and [Bokeh](https://docs.bokeh.org/) (interactive visualization). It is not pretty without CSS or bootstrap (or React), but I am not aiming to be a web dev. Interactions are fairly primitive, and do not support users explicitly. Techincal indicators for stock price movements (e.g. RSI, MACD) are not currently included.

#### learning resources
If you are looking for resources to build interactive data apps, Bokeh and Heroku have good straightforward documentation with quickstart guides. Although Flask also has a quickstart, the learning curve is fairly steep for those without a web development background, and a [tutorial for this audience](https://github.com/bev-a-tron/MyFlaskTutorial) may be quite helpful. Alternate plotting (Plotly, Altair) and web development packages (Django) may also be of interest.

#### user interactions
From a user query for a stock of interest, prices are retrieved from the [AlphaVantage API](https://www.alphavantage.co/) using a heroku config key. Prices shown are adjusted daily closing prices. The user may also select a maximum window for prices in the past using radio buttons for maximum data displayed (1, 2, 5, 10, 20 years max), though the time window displayed will only show the complete history of the stock (not more). Users may also use Bokeh's interactive widgets to pan, zoom, and reset the plot. Failed user queries should redirect to plot the starting page (QQQ) and return a warning, though in practice the hosted site has returned to the last valid query.

#### components
The main app is stocks.py which contains code for requests to the AlphaVantage API, and refers to the simple html template in templates/index.html. Stocks.py uses requests & json (API), os (API key, pandas and bokeh (data munging and plotting) and flask under the hood, while GET and POST arguements are passed to templates by Jinja2. Several files support Heroku builds including the Heroku Procfile (points to app name), runtime.txt (gives python version), and requirements.txt (gives the system environment build).   

#### internal routing
The single page app uses GET and POST arguements to draw the page and send user input. This is accomplished by a redirect to the main page (and action = '' in the html form). Handling of user input error requires a default page to load. I chose a default plot rather than the last viable query as a shortcut. In turn, this requires storage of the default data (in the app.vars dict), which further required a counter for page redirects (in app.vars) to cache the API data on initial loading. This is probably a poor implementation.

#### future improvements
As this was a quick technology learning project, there are many. For UX, styling is needed (css & bootstrap) to bring the page back to the future (from < 1990s state). For scalability, a proper cache (or DB) should be implemented, and likely the counter should be replaced. For usability, the yfinance python package would be a better data source than AlphaVantage (free tier) due to its faster updates and smaller available increments, though the integrity of Yahoo's data has been questioned. For good coding practice, docstrings, testing and encapsulation are needed, and OOP would support scaling of new features (like stock technical indicators) with consistent APIs. 

Additional features: Many features like SMA, RSI, MACD can be calculated by the python ta library, or returned from AlphaVantage, which can also deliver company metadata (dividends, shares, PE, etc). yfinance also provides this data. Candlestick plots can be made in [bokeh](https://docs.bokeh.org/en/latest/docs/gallery/candlestick.html) or [plotly](https://plotly.com/python/candlestick-charts/. Methods are also available to capture social media sentiment, or that use deep learning (e.g. LSTM, ...) for price forecasting. The first user requested support for user registration and chat features, and I suppose that user would like cryptocurency support (some in yfinance). One can imagine a kitchen sink of features available on various commercial and proprietary platforms.