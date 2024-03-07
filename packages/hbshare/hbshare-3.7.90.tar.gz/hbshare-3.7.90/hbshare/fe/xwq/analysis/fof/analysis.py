# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


class Analysis:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = data_path

    def index_compare(self):
        market_index_data = HBDB().read_index_daily_k_given_date_and_indexs(self.start_date, ['000300', '000852', '932000'])
        market_index_data['jyrq'] = market_index_data['jyrq'].astype(str)
        market_index_data = market_index_data.pivot(index='jyrq', columns='zqdm', values='spjg').sort_index()
        market_index_data = market_index_data[['000300', '000852', '932000']]
        market_index_data = market_index_data.rename(columns={'000300': '沪深300', '000852': '中证1000', '932000': '中证2000'})
        howbuy_index_data = HBDB().read_private_index_daily_k_given_indexs(['HB1001', 'HB1002'], self.start_date, self.end_date)
        howbuy_index_data['TRADE_DATE'] = howbuy_index_data['TRADE_DATE'].astype(str)
        howbuy_index_data = howbuy_index_data.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        howbuy_index_data = howbuy_index_data[['HB1001', 'HB1002']]
        howbuy_index_data = howbuy_index_data.rename(columns={'HB1001': '好买主观多头', 'HB1002': '好买量化多头'})
        index_data = market_index_data.merge(howbuy_index_data, left_index=True, right_index=True, how='right')
        index_data.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), index_data.index)
        index_data = index_data.dropna().sort_index()
        index_data.to_excel('{0}index_data.xlsx'.format(self.data_path))
        return


if __name__ == '__main__':
    start_date = '20131231'
    end_date = '20240208'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/analysis/'
    analysis = Analysis(start_date, end_date, data_path)
    analysis.index_compare()