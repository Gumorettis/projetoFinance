# Project Finance 

This project is a simulator that can be used by the client to monitor their assets in the portfolio, applying filters to generate data according to your preference. 

The client will be able to have a notion of the fluctuation of the price of their assets in the financial market, be able to trace their strategies in that analyzed asset, and even predict the price of a selected asset.

![Diagram](Diagram%20Project%20Finance.png?raw=true "Diagram")

The project captures the current data of a chosen asset using the Yfinance library, performs a brief treatment of the captured data, and then plots the data on a candlestick chart, also plotting the values of the averages that were calculated and passed to the data frame containing the asset data during the data treatment process.

To execute the routines contained on the home page the following resources must be:

## Requirements
- Python 3.11
- Streamlit
<<<<<<< HEAD
- Libraries in Python: Pandas, yfinance, numpy, matplotlib, plotly and datetime
=======
- Libraries in Python: Pandas, yfinance, numpy, matplotlib, plotly, datetime, scikit-learn and xgboost
>>>>>>> a02234b (projetoFinance)

## How to run and install dependencies

1) Clone this repository

```
git clone ....
cd projetoFinance
```
2) Install libraries/dependencies

```
pip install streamlit
pip install pandas
pip install numpy
pip install yfinance
pip install matplotlib
pip install plotly
pip install datetime
<<<<<<< HEAD
=======
pip install -U scikit-learn
pip install xgboost
>>>>>>> a02234b (projetoFinance)
```

3) Run/start the aplication in terminal

```
streamlit run 1_home_projetoFinance.py
```
 
## Services
Currently the project has a service for predicting the prices of a selected asset, this has its own "readme" which explains better what it is and how it works:

- [Predict](pages/README.md)