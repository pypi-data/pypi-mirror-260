# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime
import numpy as np
import pandas as pd
import xlwings


def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'jyrq': 'CALENDAR_DATE', 'sfjj': 'IS_OPEN', 'sfzm': 'IS_WEEK_END', 'sfym': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df


def quantile_definition(idxs, col, daily_df):
    part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
    q = (1.0 - np.count_nonzero(part_df[col].iloc[-1] < part_df[col]) / len(part_df)) if len(part_df[col].dropna()) != 0 else np.nan
    return q


def df_add_info(df, info):
    df = df.T
    df.index.name = 'INDEX'
    df = df.reset_index()
    df['TYPE'] = info
    df = df.set_index(['TYPE', 'INDEX']).T
    return df


class IndexTracking:
    def __init__(self, start_date, end_date, report_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.report_date = report_date
        self.data_path = data_path
        # 日历
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date('19000101', self.end_date)
        self.dates()
        # 指数
        self.index_list = ['881001', '000300', '000905', '000852', '932000', '399303', '8841431']
        self.index_name_dict = {'881001': '万得全A', '000300': '沪深300', '000905': '中证500', '000852': '中证1000', '932000': '中证2000', '399303': '国证2000', '8841431': '万得微盘股'}

    def dates(self):
        self.trade_df = self.trade_df.sort_values('TRADE_DATE')
        self.date_1w = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-5]
        self.date_1m = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-20 * 1]
        self.date_3m = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-20 * 3]
        self.date_6m = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-20 * 6]
        self.date_1y = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-250]
        self.date_ytd0 = self.trade_df[self.trade_df['TRADE_DATE'] < '20240101']['TRADE_DATE'].iloc[-1]
        self.date_ytd1 = self.trade_df[self.trade_df['TRADE_DATE'] < '20230101']['TRADE_DATE'].iloc[-1]
        self.date_ytd2 = self.trade_df[self.trade_df['TRADE_DATE'] < '20220101']['TRADE_DATE'].iloc[-1]
        self.date_ytd3 = self.trade_df[self.trade_df['TRADE_DATE'] < '20210101']['TRADE_DATE'].iloc[-1]
        self.date_all = self.trade_df[self.trade_df['TRADE_DATE'] < '20140101']['TRADE_DATE'].iloc[-1]
        return

    def index(self):
        index = HBDB().read_index_daily_k_given_date_and_indexs(self.start_date, self.index_list)
        index = index[['zqdm', 'jyrq', 'spjg']]
        index = index.rename(columns={'zqdm': 'INDEX_SYMBOL', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX'})
        index['TRADE_DATE'] = index['TRADE_DATE'].astype(str)
        index = index[index['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        index = index[(index['TRADE_DATE'] >= self.start_date) & (index['TRADE_DATE'] <= self.end_date)]
        index = index.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        index = index.replace(0.0, np.nan).fillna(1000.0)
        index = index[self.index_list].rename(columns=self.index_name_dict)

        close = index.copy(deep=True)
        close = df_add_info(close, '收盘价')

        close_norm = index.copy(deep=True)
        close_norm = close_norm / close_norm.iloc[0]
        close_norm = df_add_info(close_norm, '收盘价（归一化）')

        close_relative = index.copy(deep=True)
        close_relative['沪深300/中证1000'] = close_relative['沪深300'] / close_relative['中证1000']
        close_relative = close_relative[['沪深300/中证1000']]
        close_relative = df_add_info(close_relative, '比值')

        close_year = index[index.index >= self.date_ytd0]
        close_year = df_add_info(close_year, '收盘价（今年以来）')

        close_norm_year = index[index.index >= self.date_ytd0]
        close_norm_year = close_norm_year / close_norm_year.iloc[0]
        close_norm_year = df_add_info(close_norm_year, '收盘价（归一化，今年以来）')

        close_relative_year = index[index.index >= self.date_ytd0]
        close_relative_year['沪深300/中证1000'] = close_relative_year['沪深300'] / close_relative_year['中证1000']
        close_relative_year = close_relative_year[['沪深300/中证1000']]
        close_relative_year = df_add_info(close_relative_year, '比值（今年以来）')

        close_current = index.copy(deep=True)
        close_current = pd.DataFrame(close_current.iloc[-1])
        close_current.columns = ['当前点位']

        ret_1w = index.pct_change(5)
        ret_1w = pd.DataFrame(ret_1w.iloc[-1])
        ret_1w.columns = ['近一周']

        ret_1m = index.pct_change(20 * 1)
        ret_1m = pd.DataFrame(ret_1m.iloc[-1])
        ret_1m.columns = ['近一月']

        ret_3m = index.pct_change(20 * 3)
        ret_3m = pd.DataFrame(ret_3m.iloc[-1])
        ret_3m.columns = ['近三月']

        ret_6m = index.pct_change(20 * 6)
        ret_6m = pd.DataFrame(ret_6m.iloc[-1])
        ret_6m.columns = ['近六月']

        ret_1y = index.pct_change(250)
        ret_1y = pd.DataFrame(ret_1y.iloc[-1])
        ret_1y.columns = ['近一年']

        index_ytd0 = index[index.index >= self.date_ytd0]
        ret_ytd0 = index_ytd0 / index_ytd0.iloc[0] - 1
        ret_ytd0 = pd.DataFrame(ret_ytd0.iloc[-1])
        ret_ytd0.columns = ['今年以来']

        index_ytd1 = index[(index.index >= self.date_ytd1) & (index.index <= self.date_ytd0)]
        ret_ytd1 = index_ytd1 / index_ytd1.iloc[0] - 1
        ret_ytd1 = pd.DataFrame(ret_ytd1.iloc[-1])
        ret_ytd1.columns = [str(int(self.date_ytd1[:4]) + 1) + '年']

        index_ytd2 = index[(index.index >= self.date_ytd2) & (index.index <= self.date_ytd1)]
        ret_ytd2 = index_ytd2 / index_ytd2.iloc[0] - 1
        ret_ytd2 = pd.DataFrame(ret_ytd2.iloc[-1])
        ret_ytd2.columns = [str(int(self.date_ytd2[:4]) + 1) + '年']

        index_ytd3 = index[(index.index >= self.date_ytd3) & (index.index <= self.date_ytd2)]
        ret_ytd3 = index_ytd3 / index_ytd3.iloc[0] - 1
        ret_ytd3 = pd.DataFrame(ret_ytd3.iloc[-1])
        ret_ytd3.columns = [str(int(self.date_ytd3[:4]) + 1) + '年']

        index_all = index[index.index >= self.date_all]
        ret_all = index_all / index_all.iloc[0] - 1
        ret_all = pd.DataFrame(ret_all.iloc[-1])
        ret_all.columns = [str(int(self.date_all[:4]) + 1) + '年以来']

        ret = pd.concat([close_current, ret_1w, ret_1m, ret_3m, ret_6m, ret_1y, ret_ytd0, ret_ytd1, ret_ytd2, ret_ytd3, ret_all], axis=1)

        close = pd.concat([close, close_norm, close_relative, close_year, close_norm_year, close_relative_year], axis=1)
        close.index = map(lambda x: datetime.strptime(x, '%Y%m%d').date(), close.index)
        return close, ret

    def valuation(self):
        valuation = HBDB().read_index_daily_k_given_date_and_indexs(self.start_date, self.index_list)
        valuation = valuation[['zqdm', 'jyrq', 'pe']]
        valuation = valuation.rename(columns={'zqdm': 'INDEX_SYMBOL', 'jyrq': 'TRADE_DATE', 'pe': 'PE（TTM）'})
        valuation['TRADE_DATE'] = valuation['TRADE_DATE'].astype(str)
        valuation = valuation[valuation['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        valuation = valuation[(valuation['TRADE_DATE'] >= self.start_date) & (valuation['TRADE_DATE'] <= self.end_date)]
        valuation = valuation.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE（TTM）').sort_index()
        valuation = valuation.replace(0.0, np.nan)
        valuation = valuation[self.index_list].rename(columns=self.index_name_dict)
        valuation['IDX'] = range(len(valuation))

        pettm = valuation.drop('IDX', axis=1)
        pettm = df_add_info(pettm, 'PETTM')

        pettm_relative = valuation.drop('IDX', axis=1)
        pettm_relative['沪深300/中证1000'] = pettm_relative['沪深300'] / pettm_relative['中证1000']
        pettm_relative = pettm_relative[['沪深300/中证1000']]
        pettm_relative['IDX'] = range(len(pettm_relative))
        pettm_relative['近一年分位水平'] = pettm_relative['IDX'].rolling(250 * 1).apply(lambda x: quantile_definition(x, '沪深300/中证1000', pettm_relative))
        pettm_relative['近三年分位水平'] = pettm_relative['IDX'].rolling(250 * 3).apply(lambda x: quantile_definition(x, '沪深300/中证1000', pettm_relative))
        pettm_relative['近五年分位水平'] = pettm_relative['IDX'].rolling(250 * 5).apply(lambda x: quantile_definition(x, '沪深300/中证1000', pettm_relative))
        pettm_relative['近十年分位水平'] = pettm_relative['IDX'].rolling(250 * 10).apply(lambda x: quantile_definition(x, '沪深300/中证1000', pettm_relative))
        pettm_relative = pettm_relative.drop('IDX', axis=1)
        pettm_relative = df_add_info(pettm_relative, '比值')

        pettm_current = valuation.copy(deep=True).drop('IDX', axis=1)
        pettm_current = pd.DataFrame(pettm_current.iloc[-1])
        pettm_current.columns = ['当前PETTM']

        pettm_q1 = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q1.columns):
            pettm_q1[col] = valuation['IDX'].rolling(250 * 1).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q1 = pd.DataFrame(pettm_q1.iloc[-1])
        pettm_q1.columns = ['近一年分位水平']

        pettm_q3 = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q3.columns):
            pettm_q3[col] = valuation['IDX'].rolling(250 * 3).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q3 = pd.DataFrame(pettm_q3.iloc[-1])
        pettm_q3.columns = ['近三年分位水平']

        pettm_q5 = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q5.columns):
            pettm_q5[col] = valuation['IDX'].rolling(250 * 5).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q5 = pd.DataFrame(pettm_q5.iloc[-1])
        pettm_q5.columns = ['近五年分位水平']

        pettm_q10 = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q10.columns):
            pettm_q10[col] = valuation['IDX'].rolling(250 * 10).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q10 = pd.DataFrame(pettm_q10.iloc[-1])
        pettm_q10.columns = ['近十年分位水平']

        pettm_q = pd.concat([pettm_current, pettm_q1, pettm_q3, pettm_q5, pettm_q10], axis=1)

        pettm = pd.concat([pettm, pettm_relative], axis=1)
        pettm.index = map(lambda x: datetime.strptime(x, '%Y%m%d').date(), pettm.index)
        return pettm, pettm_q

    def get_all(self):
        close, ret = self.index()
        pettm, pettm_q = self.valuation()

        filename = '{0}index_tracking.xlsx'.format(self.data_path)
        app = xlwings.App(visible=False)
        wookbook = app.books.open(filename)
        wooksheet = wookbook.sheets['表格']
        wooksheet.clear()
        wooksheet["A1"].options(pd.DataFrame, header=1, expand='table').value = ret
        wooksheet["A9"].options(pd.DataFrame, header=1, expand='table').value = pettm_q
        wooksheet = wookbook.sheets['指数']
        wooksheet.clear()
        wooksheet["A1"].options(pd.DataFrame, header=1, expand='table').value = close
        wooksheet = wookbook.sheets['估值']
        wooksheet.clear()
        wooksheet["A1"].options(pd.DataFrame, header=1, expand='table').value = pettm
        wookbook.save(filename)
        wookbook.close()
        app.quit()
        return


if __name__ == '__main__':
    start_date = '20131231'
    end_date = '20240227'
    report_date = '20230930'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/index_tracking/'
    IndexTracking(start_date, end_date, report_date, data_path).get_all()