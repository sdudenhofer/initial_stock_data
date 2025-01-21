
import yfinance as yf
import pandas as pd
import altair as alt
import streamlit as st

tickers = ['AAPL', 'NVDA', 'MSFT', 'AMZN', 'GOOG']

data = yf.download(tickers, start="2024-01-01", end="2024-12-31")
data = data.loc[(slice(None)),(slice(None),slice(None))].copy()
data = data.stack()
data = data.reset_index()
data.rename(columns={'level_1': 'Symbol'}, inplace=True)

st.header("Stock Data")

# sidebar
st.sidebar.header("Options")
years = st.sidebar.selectbox(
    'Select which year you would like to see.',
    ('2023', '2024')
)

stock_data = st.sidebar.selectbox(
    'Choose the stock(s)',
    tickers
)
single_source = yf.Ticker(stock_data)

st.sidebar.write("Price to Earning Ratio")
st.sidebar.write(single_source.info['forwardPE'])
st.sidebar.write("Market Cap")
st.sidebar.write(single_source.info['marketCap'])
st.sidebar.write("Volume")
st.sidebar.write(single_source.info['volume'])
st.sidebar.write("Day High")
st.sidebar.write(single_source.info["dayHigh"])
st.sidebar.write("Day Low")
st.sidebar.write(single_source.info["dayLow"])

# charts
base = alt.Chart(data).encode(
    alt.Color("Ticker").legend(None),
    tooltip = "Close"
).properties(
    width=900,
    height=500,
    title="2024 Closing Price by Month"
)

line = base.mark_line().encode(
    x="Date", y="Close",
)


last_price = base.mark_circle().encode(
    alt.X("last_date['Date']:T"),
    alt.Y("last_date['Close']:Q")
).transform_aggregate(
    last_date="argmax(Date)",
    groupby=["Ticker"]
)

company_name = last_price.mark_text(align="left", dx=4).encode(
    text="Ticker",
)

chart_2024 = (line + last_price + company_name).encode(
    x=alt.X().title("Date"),
    y=alt.Y().title("Closing Price"),
)

data_2023 = yf.download(tickers, start="2023-01-01", end="2023-12-31")
data_2023 = data_2023.loc[(slice(None)),(slice(None),slice(None))].copy()
data_2023 = data_2023.stack()
data_2023 = data_2023.reset_index()
data_2023.rename(columns={'level_1': 'Symbol'}, inplace=True)

base_2023 = alt.Chart(data_2023).encode(
    alt.Color("Ticker").legend(None),
    tooltip = "Close"
).properties(
    width=900,
    height=500,
    title="2023 Closing Price by Month"
)

line_2023 = base_2023.mark_line().encode(x="Date", y="Close")


last_price_2023 = base_2023.mark_circle().encode(
    alt.X("last_date['Date']:T"),
    alt.Y("last_date['Closing Price']:Q")
).transform_aggregate(
    last_date="argmax(Date)",
    groupby=["Ticker"]
)

company_name_2023 = last_price_2023.mark_text(align="left", dx=4).encode(text="Ticker")

chart_2023 = (line_2023 + last_price_2023 + company_name_2023).encode(
    x=alt.X().title("Date"),
    y=alt.Y().title("Close")
)


if years == '2024':
    st.write(chart_2024 )
else:
    st.write(chart_2023)

