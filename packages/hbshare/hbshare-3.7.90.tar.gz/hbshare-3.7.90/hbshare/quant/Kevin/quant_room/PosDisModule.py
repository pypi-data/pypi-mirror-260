"""
轻量化持仓分布模块
"""
import pandas as pd
import numpy as np
import hbshare as hbs
import datetime
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params
from hbshare.fe.common.util.data_loader import get_trading_day_list
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import fetch_data_batch_hbs, get_benchmark_components_from_sql_new


def get_shift_date(trade_date):
    trade_dt = datetime.datetime.strptime(trade_date, '%Y%m%d')
    pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

    sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM st_main.t_st_gg_jyrl WHERE JYRQ >= {} and JYRQ <= {}".format(
        pre_date, trade_date)
    res = hbs.db_data_query('alluser', sql_script, page_size=5000)
    df = pd.DataFrame(res['data']).rename(
        columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                 "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
    df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
    df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
    df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

    trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

    return trading_day_list[-1]


def main():
    # 初始化配置
    engine = create_engine(engine_params)
    sql_script = "SELECT distinct trade_date FROM private_fund_holding"
    date_df = pd.read_sql(sql_script, engine)
    date_df['trade_date'] = date_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
    hold_dates = sorted([x for x in date_df['trade_date'].tolist() if x >= "20230831" and x[6:] >= "28"])
    dis_summary = []
    for trade_date in hold_dates:
        print("{} 期计算中...".format(trade_date))
        shift_date = get_shift_date(trade_date)
        sql_script = "SELECT * FROM private_fund_holding where trade_date = {}".format(trade_date)
        hold_df = pd.read_sql(sql_script, engine)
        # map_df = hold_df[['fund_name', 'fund_type']].drop_duplicates(subset=['fund_name'])
        # hold_df = hold_df.pivot_table(index='ticker', columns='fund_name', values="weight").fillna(0.)
        bm_components = get_benchmark_components_from_sql_new(shift_date)
        merged_df = hold_df.merge(bm_components, on='ticker', how='left').fillna('other')
        # 统计
        distribution_df = merged_df.groupby(['fund_name', 'benchmark_id'])['weight'].sum().reset_index()
        dis_df = distribution_df.pivot_table(index='fund_name', columns='benchmark_id', values='weight').fillna(0.)
        dis_df['not_equity'] = 100 - dis_df.sum(axis=1)
        dis_df /= 100.
        dis_df.rename(columns={"000300": "沪深300", "000905": "中证500", "000852": "中证1000", "932000": "中证2000",
                               "other": "超小票", "not_equity": "非权益仓位"}, inplace=True)
        dis_df['trade_date'] = trade_date
        dis_df.reset_index(inplace=True)

        dis_summary.append(dis_df)
        print("{} 期计算完成！！！".format(trade_date))

    dis_summary = pd.concat(dis_summary, axis=0)
    cols_order = ['fund_name', 'trade_date', '沪深300', '中证500', '中证1000', '中证2000', '超小票', '非权益仓位']
    dis_summary = dis_summary.sort_values(by=['fund_name', 'trade_date'])[cols_order]

    return dis_summary

if __name__ == '__main__':
    main()