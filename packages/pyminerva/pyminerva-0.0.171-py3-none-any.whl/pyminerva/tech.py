# Copyright 2023-2025 Jeongmin Kang, jarvisNim @ GitHub
# See LICENSE for details.
'''
Prgram 명: technical Analysis 만들기
Author: jeongmin Kang
Mail: jarvisNim@gmail.com
History
- 20240228  Create
'''
import sys, os, time
import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import yfinance as yf

from scipy import signal
from datetime import date, datetime, timedelta
from .utils import constant as cst
# from .utils.techs_funcs import (
#     find_30days_ago,
# )
from . import base

'''
0. 공통영역 설정
'''
# logging
base.logger.warning(sys.argv[0] + ' :: ' + str(datetime.today()))
base.logger2.info('')
base.logger2.info(sys.argv[0] + ' :: ' + str(datetime.today()))

#####################################
# funtions
#####################################

# 3개월단위로 순차적으로 읽어오는 경우의 시작/종료 일자 셋팅
# to_date_2 = pd.to_datetime(to_date2)
# three_month_days = relativedelta(weeks=12)
# from_date = (to_date_2 - three_month_days).date()
# to_date_2 = to_date_2.date()

TECH_LIST = ['sma','ema','macd','adx','psar','ichmoku',  # Trend
           'rsi','stoch','roc','cci','willr','ao','stochrsi','ppo',  # Monentum
           'obv','pvt','pvi','cmf','vwap','adosc','mfi','kvo','nvi',  # Volume
           'atr','bbands','donchian','kc','rvi',]  # Volatility

def get_tech_types(tech_type):
    trend_indics = ['sma','ema','macd','adx','psar','ichmoku','obv','vwap','adosc','atr','donchian',
                    'rvi',]
    overBoughtSold_indics = ['rsi','stoch','willr','mfi','pvi',]
    trendReversal_indics = ['roc','ao','nvi','bbands','kc',]
    kReversal_indics = ['kvo','cmf',]

    if tech_type in trend_indics:
        result = 'trend'
    elif tech_type in overBoughtSold_indics:
        result = 'overBoughtSold'
    elif tech_type in trendReversal_indics:
        result = 'trendReversal'
    elif tech_type in kReversal_indics:
        result = 'kReversal'
    else:
        result = None

    return result


# Loading data, and split in train and test datasets
def get_tech_data(ticker, window):

    ticker_obj = yf.Ticker(ticker)
    # History Data
    df_hist = ticker_obj.history(period='36mo') # test: 10mo, real: 36mo
    try:
        df_hist['feature'] = signal.detrend(df_hist['Close'])
    except ValueError as e: # ValueError: cannot reshape array of size 0 into shape (0,newaxis)
            time.sleep(5)
            base.logger2.error(f'get_tech_data Value error 1: {e}')
            df_hist = ticker_obj.history(period='36mo') # test: 10mo, real: 36mo
    df_hist['mean'] = df_hist['feature'].rolling(window=window).mean()
    df_hist['std'] = df_hist['feature'].rolling(window=window).std()

    # Financial Data
    pnl = ticker_obj.financials
    bs = ticker_obj.balancesheet
    cf = ticker_obj.cashflow
    # concatenate into one dataframe
    _df_fin = pd.concat([pnl, bs, cf]) 
    # make dataframe format nicer
    # Swap dates and columns
    df_fin = _df_fin.T
    # reset index (date) into a column
    df_fin = df_fin.reset_index()
    # Rename old index from '' to Date
    df_fin.columns = ['Date', *data.columns[1:]]

    
    return df_hist, df_fin


def make_tech_plot(ticker, df, tech_type, TECH_LIST, idx):
    
    _df = df.copy() # 그래프만 그리면 되고, 본 df 에는 영향을 주지않기위해 복사본 만듬.
    # _df = _df.dropna()  # @@@ 그래프 종료일자까지 일부 그래프가 달라지는 현상이 있어 검증을 위해 제거

    h_limit = 70  # 밴드형 상단 기준선
    l_limit = 30  # 밴드형 하단 기준선
    base_limit = 0  # 기준선형 기준선

    plt.subplot(len(TECH_LIST), 1, idx)    

    max_val = max(_df[tech_type])
    min_val = min(_df[tech_type])

    if tech_type in ['sma','ema','macd','adx','ppo','psar','ichmoku','stoch','roc','ao',
                     'obv','pvt','pvi','cmf','vwap','adosc','kvo','nvi','atr','rvi',]:  # 기준선형 그래프로
        
        if tech_type in ['obv','pvt','cmf','vwap','adosc']:  # Volume 베이스 들은 수치가 커서 지표그래프 안보임.
            pass
        else:
            plt.plot(_df.index, _df['Close'], color='royalblue')

        if tech_type == 'adx':
            offset = 25  # offset: DI+ 와 DI- 차이가 25% 이상 또는 이하이면 signal ON
            _df[tech_type] = _df[tech_type] - offset
            plt.plot(_df.index, _df['DMP_14'], color='orange')
            plt.plot(_df.index, _df['DMN_14'], color='orange')
        elif tech_type == 'stoch':
            h_limit = 85
            l_limit = 15            
            plt.plot(_df.index, _df['STOCHk_14_3_3'], color='orange')
            plt.plot(_df.index, _df['STOCHd_14_3_3'], color='orange')
            plt.axhline(y=h_limit, linestyle='--', lw=1.4, color='gray',)
            plt.axhline(y=l_limit, linestyle='--', lw=1.4, color='gray',)            

        plt.bar(_df.index, _df[tech_type], color=['g' if _df[tech_type].iloc[i] > base_limit else 'r' for i in range(len(_df))])

        _df['pivot'] = np.where((_df[tech_type] > base_limit) & (_df[tech_type].shift(1) <= base_limit), 1, 0)  # Buy signal
        _df['pivot'] = np.where((_df[tech_type] < base_limit) & (_df[tech_type].shift(1) >= base_limit), -1, _df['pivot']) # Sell signal
        _1 = _df[_df['pivot'] == -1]
        _2 = _df[_df['pivot'] == 1]

        plt.axhline(y=base_limit, linestyle='--', color='red', linewidth=1)

    else:  # top과 Buttom 구간값을 기준으로 설정하는 밴드형인경우    

        if tech_type == 'cci':  
            h_limit = 100
            l_limit = -100
        elif tech_type == 'willr':
            h_limit = -20
            l_limit = -80

        plt.plot(_df.index, _df['Close'], color='royalblue')

        if tech_type == 'bbands':  # 
            plt.plot(_df.index, _df['BBU_5_2.0'], color='orange')  # Upper line
            plt.plot(_df.index, _df['BBL_5_2.0'], color='orange')  # Lower line
            # print(_df)
            _df['pivot'] = np.where((_df[tech_type] >= _df['BBU_5_2.0']) & (_df[tech_type].shift(1) <= _df['BBU_5_2.0']).shift(1), 1, 0)  # Sell signal
            _df['pivot'] = np.where((_df[tech_type] <= _df['BBL_5_2.0']) & (_df[tech_type].shift(1) >= _df['BBL_5_2.0']).shift(1), -1, _df['pivot']) # Buy signal
        elif tech_type == 'donchian':  # 
            plt.plot(_df.index, _df['DCU_20_20'], color='orange')  # Upper line
            plt.plot(_df.index, _df['DCL_20_20'], color='orange')  # Lower line
            # print(_df)
            _df['pivot'] = np.where((_df[tech_type] >= _df['DCU_20_20']) & (_df[tech_type].shift(1) <= _df['DCU_20_20']).shift(1), 1, 0)  # Sell signal
            _df['pivot'] = np.where((_df[tech_type] <= _df['DCL_20_20']) & (_df[tech_type].shift(1) >= _df['DCL_20_20']).shift(1), -1, _df['pivot']) # Buy signal
        elif tech_type == 'kc':  # 
            plt.plot(_df.index, _df['KCUe_20_2'], color='orange')  # Upper line
            plt.plot(_df.index, _df['KCLe_20_2'], color='orange')  # Lower line
            _df['pivot'] = np.where((_df[tech_type] > _df['KCUe_20_2']) & (_df[tech_type].shift(1) <= _df['KCUe_20_2']).shift(1), 1, 0)  # Sell signal
            _df['pivot'] = np.where((_df[tech_type] < _df['KCLe_20_2']) & (_df[tech_type].shift(1) >= _df['KCLe_20_2']).shift(1), -1, _df['pivot']) # Buy signal

        else:
            plt.plot(_df.index, _df[tech_type], color='orange')
            plt.axhline(y=h_limit, linestyle='--', lw=1.4, color='gray',)
            plt.axhline(y=l_limit, linestyle='--', lw=1.4, color='gray',)
            _df['pivot'] = np.where((_df[tech_type] >= h_limit) & (_df[tech_type].shift(1) <= h_limit), 1, 0)  # Sell signal
            _df['pivot'] = np.where((_df[tech_type] <= l_limit) & (_df[tech_type].shift(1) >= l_limit), -1, _df['pivot']) # Buy signal

        _1 = _df[_df['pivot'] == 1]  # Sell signal
        _2 = _df[_df['pivot'] == -1]  # Buy signal
        for date in _1.index:  # Sell signal
            plt.axvline(date, color='r', linestyle='--', lw=1,  alpha=1)  # Sell signal

        for date in _2.index:  # Buy signal
            plt.axvline(date, color='g', linestyle='--', lw=1,  alpha=1)  # Buy signal
 
    signal = get_tech_types(tech_type)
    # print(signal)

    if _1.empty and _2.empty:
        latest_date = '9999-99-99'
        decision = '현상태 유지'
    elif _1.empty:
        latest_date = max(_2.index)
        if signal == 'trend':
            decision = '추세상승 시작'
        elif signal == 'overBoughtSold':
            decision = '과매도 시작'
        elif signal == 'trendReversal':
            decision = '바닥지나 상승 시작'
        elif signal == 'trendReversal':
            decision = 'k 상승반전 시작'            
        else:
            decision = '분할매수 시작'
    elif _2.empty:
        latest_date = max(_1.index)
        if signal == 'trend':
            decision = '추세하락 시작'
        elif signal == 'overBoughtSold':
            decision = '과매수 시작'
        elif signal == 'trendReversal':
            decision = '천정지나 하락 시작'
        elif signal == 'trendReversal':
            decision = 'k 하락반전 시작'            
        else:
            decision = '분할매도 시작'
    else:
        latest_date = max(_1.index[-1], _2.index[-1])
        if latest_date == _1.index[-1]:
            if signal == 'trend':
                decision = '추세하락 시작'
            elif signal == 'overBoughtSold':
                decision = '과매수 시작'
            elif signal == 'trendReversal':
                decision = '천정지나 하락 시작'
            elif signal == 'trendReversal':
                decision = 'k 하락반전 시작'            
            else:
                decision = '분할매도 시작'
        else:
            if signal == 'trend':
                decision = '추세상승 시작'
            elif signal == 'overBoughtSold':
                decision = '과매도 시작'
            elif signal == 'trendReversal':
                decision = '바닥지나 상승 시작'
            elif signal == 'trendReversal':
                decision = 'k 상승반전 시작'            
            else:
                decision = '분할매수 시작'

    try:
        latest_date = latest_date.date()
    except:
        pass
    plt.title(f"{ticker}: {tech_type} / {latest_date}부터 {decision} ", fontdict={'fontsize':20, 'color':'g'})    
    plt.grid(lw=0.7, color='lightgray')
    # plt.xlabel(f'Last Date: {latest_date}', loc='right', fontsize=18)
    
    return latest_date




'''
I. Technical Analysis

- 1. Trend
    Simple Moving Average (SMA)*
    Exponential Moving Average (EMA)*
    Weighted Moving Average (WMA)
    Moving Average Convergence Divergence (MACD)
    Average Directional Movement Index (ADX)*
    Vortex Indicator (VI)
    Trix (TRIX)
    Mass Index (MI)
    Detrended Price Oscillator (DPO)
    KST Oscillator (KST)
    Ichimoku Kinkō Hyō (Ichimoku)*
    Parabolic Stop And Reverse (Parabolic SAR)*
    Schaff Trend Cycle (STC)
    ZigZag Indicator.... (Not yet)

    
- 2. Momentum: https://medium.com/@crisvelasquez/top-6-momentum-indicators-in-python-bea0875e60a5
    Relative Strength Index (RSI)*
    Stochastic RSI (SRSI)
    True strength index (TSI)
    Ultimate Oscillator (UO)
    Stochastic Oscillator (SR)*
    Williams %R (WR)*
    Awesome Oscillator (AO)*
    Kaufman’s Adaptive Moving Average (KAMA)
    Rate of Change (ROC)*
    Percentage Price Oscillator (PPO)
    Percentage Volume Oscillator (PVO)
    Commodity Channel Index (CCI)*

    
- 3. Volume
    Money Flow Index (MFI)*
    Accumulation/Distribution Index (ADI)*
    On-Balance Volume (OBV)*
    Volume-price Trend (VPT)*    
    Chaikin Money Flow (CMF)*
    Force Index (FI)
    Ease of Movement (EoM, EMV)
    Negative Volume Index (NVI)*
    Volume Weighted Average Price (VWAP)*
    Ulcer Index (UI)
    Positive Volume Index (PVI)*
    Klinger Volume Oscillator(KVO)*

    
- 4. Volatility
    Average True Range (ATR)*
    Bollinger Bands (BB)*
    Donchian Channel (DC)*
    Keltner Channel (KC)*
    Relative Volatility Index (RVI).... (Not yet)
    Volatility Chaikin.... (Not yet)

'''

'''
1. Trend Indicators: https://medium.com/@crisvelasquez/top-6-trend-indicators-in-python-c922ac0674f9
'''
# Trend.Simple Moving Average (SMA)
# calculates the average price over a specific period, providing a smoothed representation of price movement.
# 특정 기간 동안의 평균 가격을 계산하여 가격 변동을 부드럽게 표현합니다.
def sma(ticker, df, tech_type, TECH_LIST, idx):
    df[tech_type] = df.ta.sma(20) - df.ta.sma(200)
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Trend.Exponential Moving Average (EMA)
# gives more weight to recent prices, making it more responsive to new information.
# 최근 가격에 더 많은 가중치를 부여하여 새로운 정보에 더 잘 반응합니다.
def ema(ticker, df, tech_type, TECH_LIST, idx):
    df[tech_type] = df.ta.ema(20) - df.ta.ema(200)
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Trend.Exponential Moving Average (EMA)
# shows the relationship between two moving averages of a security’s price.
# 증권 가격의 두 이동 평균 사이의 관계를 보여줍니다.
def macd(ticker, df, tech_type, TECH_LIST, idx):
    # Get the 26-day EMA of the closing price
    k = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 12-day EMA of the closing price
    d = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    df[tech_type] = (macd - macd_s)*5  # 폭이 너무 작아 크게 보이기 위해 *5
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Average Directional Movement Index (ADX):
# quantify the strength of a trend. 추세의 강도를 정량화합니다.
# The +DI and -DI lines can help identify the direction of the trend. 양의 방향 표시기(+DI) 및 음의 방향 표시기(-DI).
def adx(ticker, df, tech_type, TECH_LIST, idx):  # DMP_14(posituve) 와 DMN_14(negative) 두 개 칼럼 생성
    df.ta.adx(length=14, append=True)
    df[tech_type] = df['ADX_14']
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Parabolic Stop And Reverse (Parabolic SAR)
def psar(ticker, df, tech_type, TECH_LIST, idx):  # DMP_14(posituve) 와 DMN_14(negative) 두 개 칼럼 생성
    df.ta.psar(append=True)
    df['PSARl_0.02_0.2'] = df['PSARl_0.02_0.2'].fillna(0)
    df['PSARs_0.02_0.2'] = df['PSARs_0.02_0.2'].fillna(0)
    df[tech_type] = df['Close'] - (df['PSARl_0.02_0.2'] + df['PSARs_0.02_0.2'])  # PSARl_0.02_0.2 는 long 값, PSARl_0.02_0.2 는 short 값
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date


# Ichimoku Kinkō Hyō (Ichimoku)
# a trend-following indicator that provides entry and exit points.
# 진입점과 이탈점을 제공하는 추세추종 지표입니다.
def ichmoku(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.ichimoku(append=True)
    # Tenkan Sen: ITS_9 > Kijun Sen: IKS_26 => Buy signal
    df[tech_type] = (df['ITS_9'] - df['IKS_26'])*5  # 폭이 너무 작아 크게 보이기 위해 *5
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date


'''
2. Momentum Indicators: https://medium.com/@crisvelasquez/top-6-momentum-indicators-in-python-bea0875e60a5
'''
# Momentum.Relative Strength Index (RSI) 
# measures the speed and change of price movements, oscillating between 0 and 100.
# 0과 100 사이에서 진동하는 가격 움직임의 속도와 변화를 측정합니다.
def rsi(ticker, df, tech_type, TECH_LIST, idx):    
    df[tech_type] = df.ta.rsi(14)
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Momentum.Stochastic Oscillator (STOCH): 
# comparing a particular closing price of a security to a range of its prices over a certain period of time.
# 특정 기간 동안의 특정 유가 증권 종가를 해당 가격 범위와 비교하는 것입니다.
def stoch(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.stoch(append=True)
    df[tech_type] = df['STOCHk_14_3_3'] - df['STOCHd_14_3_3']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Momentum.Rate of Change (ROC) Momentum Oscillator
# measures the percentage change in price between the current price and the price a certain number of periods ago.
# 현재 가격과 특정 기간 전 가격 사이의 가격 변화율을 측정합니다.
def roc(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.roc(append=True)
    df[tech_type] = df['ROC_10']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Momentum.Commodity Channel Index (CCI): identifies cyclical trends in securities 
# by comparing their current typical price (TP) to the average TP over a specific period, usually 20 days.
# 현재 일반 가격(TP)을 특정 기간(보통 20일) 동안의 평균 TP와 비교하여 증권의 순환 추세를 식별합니다.
def cci(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.cci(append=True)
    df[tech_type] = df['CCI_14_0.015']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Momentum.Williams %R (WR): reflects the level of the close relative to the highest high for a set period.
# 일정 기간 동안 최고가 대비 종가 수준을 반영합니다.
def willr(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.willr(append=True)
    df[tech_type] = df['WILLR_14']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Momentum.Awesome Oscillator (AO): designed to capture momentum in the market by comparing the recent market momentum with the general momentum over a wider frame of time.
# 최근 시장 모멘텀과 더 넓은 기간 동안의 일반적인 모멘텀을 비교하여 시장의 모멘텀을 포착합니다.
def ao(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.ao(append=True)
    df[tech_type] = df['AO_5_34']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Momentum.Stochastic RSI (STOCHRSI)
def stochrsi(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.stochrsi(append=True)    
    df[tech_type] = df['STOCHk_14_3_3'] - df['STOCHd_14_3_3']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Momentum.Percentage Price Oscillator (PPO):
# "Stochastic RSI and Dynamic Momentum Index" was created by Tushar Chande and Stanley Kroll and published in Stock & Commodities V.11:5 (189-199)
# It is a range-bound oscillator with two lines moving between 0 and 100.
def ppo(ticker, df, tech_type, TECH_LIST, idx):    
    buf= df.ta.ppo(close=df['Close'], append=True)
    df[tech_type] = buf['PPO_12_26_9']
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
                    
    return df, latest_date

'''
3. Volume Indicators: https://medium.com/@crisvelasquez/top-9-volume-indicators-in-python-e398791b98f9
'''
# Volume.On-Balance Volume (OBV)
# a cumulative indicator that relates volume to price change. 
# OBV increases or decreases during each trading day in line with whether the price closes higher or lower from the previous close.
# 거래량과 가격 변화를 연결하는 누적 지표입니다.
# OBV는 가격이 이전 종가보다 높게 또는 낮게 마감되는지 여부에 따라 각 거래일 동안 증가하거나 감소합니다.
def obv(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.obv(append=True)
    df['OBV_EMA'] = df['OBV'].ewm(span=30).mean()  # 20-day EMA of OBV
    df[tech_type] = df['OBV'] - df['OBV_EMA']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volume.Volume Price Trend (VPT)
# integrates volume with the percentage change in price, cumulatively indicating the trend’s strength and direction.
# 거래량과 가격 변동률을 통합하여 추세의 강도와 방향을 누적적으로 나타냅니다.
def pvt(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.pvt(append=True)
    df['PVT_MA'] = df['PVT'].rolling(window=30).mean()  # 20-day moving average
    df[tech_type] = df['PVT'] - df['PVT_MA']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volume.Positive Volume Index (PVI)
# @@@quantifies the percentage rate at which volume changes over a specific period, comparing current volume to volume from n days ago.
# @@@n일 전의 거래량과 현재 거래량을 비교하여 특정 기간 동안 거래량이 변경되는 비율을 정량화합니다.
def pvi(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.pvi(append=True)
    df['PVI_1_MA'] = df['PVI_1'].rolling(window=30).mean()  # 20-day moving average
    df[tech_type] = df['PVI_1'] - df['PVI_1_MA']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volume.Chaikin Money Flow (CMF)
# integrates price and volume to measure the buying and selling pressure over a specified period, typically 20 days.
# 특정 기간(일반적으로 20일) 동안의 매수 및 매도 압력을 측정하기 위해 가격과 거래량을 통합합니다.
def cmf(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.cmf(append=True)
    df[tech_type] = df['CMF_20']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volume.Volume-Weighted Average Price (VWAP)
# gives the average price a stock has traded at during the day, weighted by volume
# 거래량에 따라 가중치를 적용하여 하루 동안 주식이 거래된 평균 가격을 제공합니다.
def vwap(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.vwap(append=True)
    df[tech_type] = df['Close'] - df['VWAP_D']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volume.Accumulation/Distribution Oscillator (ADOSC)
# designed to reflect the cumulative flow of money into or out of a security, factoring in both the volume and the price movement.
# 거래량과 가격 변동을 모두 고려하여 증권 안팎으로의 누적 자금 흐름을 반영하도록 설계되었습니다.
def adosc(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.adosc(append=True)
    df[tech_type] = df['ADOSC_3_10']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volume.Money Flow Index (MFI)
# a technical momentum indicator that combines price and volume to assess the buying or selling pressure on an asset. 
# 자산에 대한 매수 또는 매도 압력을 평가하기 위해 가격과 거래량을 결합하는 기술적 모멘텀 지표입니다.
def mfi(ticker, df, tech_type, TECH_LIST, idx):
    df[tech_type] = df.ta.mfi(close=df['Close'],length=14, append=True)
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)

    return df, latest_date

# Volume.Klinger Volume Oscillator (KVO)
# It is designed to predict price reversals in a market by comparing volume to price
# 거래량과 가격을 비교하여 시장의 가격 반전을 예측하도록 설계되었습니다.
def kvo(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.kvo(append=True)
    df[tech_type] = df['KVO_34_55_13']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volume.Negative Volume Index (NVI)
# cumulative indicator that increases when the volume decreases compared to the previous session, suggesting that the “smart money” is active.
# 이전 세션에 비해 거래량이 감소할 때 증가하는 누적 지표로 '스마트머니'가 활성화되었음을 시사한다.
def nvi(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.nvi(append=True)
    df['NVI_1_SMA'] = df['NVI_1'].rolling(window=20).mean()    
    df[tech_type] = df['NVI_1'] - df['NVI_1_SMA']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date


'''
4. Volatility Indicators: https://medium.com/@crisvelasquez/top-6-volatility-indicators-in-python-14fbd7bf92d8
'''
# Volatility.Average True Range (ATR)
# quantifies market volatility by averaging the range of price movements.
# 가격 변동 범위를 평균하여 시장 변동성을 정량화합니다.
def atr(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.atr(append=True)
    df['ATRr_14_MA'] = df['ATRr_14'].rolling(window=20).mean()    
    df[tech_type] = df['ATRr_14'] - df['ATRr_14_MA']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date

# Volatility.Bollinger Bands (BB)
# provide insights into market volatility and overbought/oversold conditions.
# 시장 변동성과 과매수/과매도 상태에 대한 통찰력을 제공합니다.
def bbands(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.bbands(append=True)
    df[tech_type] = df['Close']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)    
    
    return df, latest_date

# Volatility.Donchian Channels (DONCHAIN)
# are based on the highest high and lowest low, offering a view of market range and volatility.
# 최고가와 최저가를 기반으로 하며 시장 범위와 변동성에 대한 시각을 제공합니다.
def donchian(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.donchian(append=True)
    df[tech_type] = df['Close']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)    
    
    return df, latest_date

# Volatility.Keltner Channels (KC)
# use ATR for band setting, making them sensitive to volatility spikes.
# 밴드 설정에 ATR을 사용하여 변동성 급증에 민감하게 만듭니다.
def kc(ticker, df, tech_type, TECH_LIST, idx):    
    df.ta.kc(append=True)
    df[tech_type] = df['Close']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)    
    
    return df, latest_date

# Volatility.Relative Volatility Index (RVI)
# volatility measurement that mirrors the RSI but uses standard deviation.
# RSI를 반영하지만 표준편차를 사용하는 변동성 측정입니다.
def rvi(ticker, df, tech_type, TECH_LIST, idx):
    df.ta.rvi(append=True)
    df['RVI_14_SMA'] = df['RVI_14'].rolling(window=20).mean()    
    df[tech_type] = df['RVI_14'] - df['RVI_14_SMA']
    # print(df.tail())
    latest_date = make_tech_plot(ticker, df, tech_type, TECH_LIST, idx)
    
    return df, latest_date