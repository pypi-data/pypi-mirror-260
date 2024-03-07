import pandas as pd
import hbshare as hbs
hbs.set_token("qwertyuisdfghjkxcvbn1000")

# 取数据
def get_df(sql, db, page_size=2000):
    data = hbs.db_data_query(db, sql, page_size=page_size, timeout=120)
    pages = data['pages']
    data = pd.DataFrame(data['data'])
    if pages > 1:
        for page in range(2, pages + 1):
            temp_data = hbs.db_data_query(db, sql, page_size=page_size, page_num=page, timeout=120)
            data = pd.concat([data, pd.DataFrame(temp_data['data'])], axis=0)
    return data

def index_cjl(start_date,end_date):
    from datetime import datetime
    wind_start = datetime.strptime(str(start_date), '%Y%m%d').strftime('%Y-%m-%d')
    wind_end = datetime.strptime(str(end_date), '%Y%m%d').strftime('%Y-%m-%d')

    # 000300.SH	沪深300
    # 000905.SH	中证500
    # 000852.SH	中证1000
    # 932000.CSI 中证2000
    # 8841431.WI 万得微盘股指数

    # 指数成交量时序
    sql_zs = "select jyrq 交易日期, zqdm 证券代码, zqmc 证券名称, cjjs 成交量 from st_market.t_st_zs_hqql \
              where jyrq >={0} and jyrq <={1} and zqdm in (000300,000905,000852,932000)".format(start_date, end_date)

    zs_cjl = get_df(sql_zs, db='alluser')
    zs_cjl_pivot = zs_cjl.pivot_table(values='成交量', index='交易日期', columns='证券名称').reset_index()

    # 万得微盘股指数成交量时序
    from WindPy import w
    w.start()
    wind_wp_cjl = w.wsd("8841431.WI", "amt", wind_start, wind_end, "unit=1", usedf=True)[1].reset_index(
        drop=False).rename(columns={"index": "交易日期", "AMT": "万得微盘股指数"})
    w.stop()
    wind_wp_cjl['交易日期'] = pd.to_datetime(wind_wp_cjl['交易日期']).dt.strftime('%Y%m%d')
    wind_wp_cjl['交易日期'] = wind_wp_cjl['交易日期'].astype(int)

    zs_cjl_ts = pd.merge(zs_cjl_pivot, wind_wp_cjl, how='left', on='交易日期')

    # 上证指数 000001.SH
    # 深证A指 399107.SZ
    # 创业板综 399102.SZ

    # 全市场成交量时序
    sql_market = "select jyrq 交易日期, zqdm 证券代码, zqmc 证券名称, cjjs 成交量 from st_market.t_st_zs_hqql \
              where jyrq >={0} and jyrq <={1} and zqdm in (000001,399107,399102)".format(start_date, end_date)

    market_cjl = get_df(sql_market, db='alluser')
    market_cjl_pivot = market_cjl.pivot_table(values='成交量', index='交易日期', columns='证券名称').reset_index()
    market_cjl_pivot['全市场'] = market_cjl_pivot['上证指数'] + market_cjl_pivot['创业板综'] + market_cjl_pivot[
        '深证Ａ指']

    market_cjl_ts = market_cjl_pivot[['交易日期', '全市场']]

    # 合并 指数与全市场成交量时序
    zs_market_cjl_ts = pd.merge(zs_cjl_ts, market_cjl_ts, on='交易日期', how='left')
    zs_market_cjl_ts['中证1000_成交量占比'] = 100 * (zs_market_cjl_ts['中证1000'] / zs_market_cjl_ts['全市场'])
    zs_market_cjl_ts['中证2000_成交量占比'] = 100 * (zs_market_cjl_ts['中证2000'] / zs_market_cjl_ts['全市场'])
    zs_market_cjl_ts['中证500_成交量占比'] = 100 * (zs_market_cjl_ts['中证500'] / zs_market_cjl_ts['全市场'])
    zs_market_cjl_ts['沪深300_成交量占比'] = 100 * (zs_market_cjl_ts['沪深300'] / zs_market_cjl_ts['全市场'])
    zs_market_cjl_ts['万得微盘股指数_成交量占比'] = 100 * (
                zs_market_cjl_ts['万得微盘股指数'] / zs_market_cjl_ts['全市场'])

    # 指数成交量时序
    cjl_index_ts = zs_market_cjl_ts[['交易日期', '沪深300', '中证500', '中证1000',
                                     '中证2000', '万得微盘股指数', '全市场']]

    # 指数成交量占比时序
    cjl_index_pct_ts = zs_market_cjl_ts[['交易日期', '沪深300_成交量占比', '中证500_成交量占比', '中证1000_成交量占比',
                                         '中证2000_成交量占比', '万得微盘股指数_成交量占比']]

    return cjl_index_ts,cjl_index_pct_ts

def stock_A_cjl(start_date,end_date,stock_A_path):
    # stock_A_path = r'D:\cyp\周度跟踪数据\数据源\A股.xlsx'

    Astock_list = pd.read_excel(stock_A_path)
    Astock_list = Astock_list[['证券代码', '证券简称']]

    Astock_dm = Astock_list['证券代码'].str[0:6]

    # 个股成交量时序
    sql_stock = "select jyrq 交易日期, zqdm 证券代码, zqmc 证券名称, cjjs 成交量 from st_ashare.t_st_ag_gpjy \
                 where jyrq >={0} and jyrq <={1} and zqdm in {2}".format(start_date, end_date, tuple(Astock_dm))

    stock_cjl = get_df(sql_stock, db='alluser')
    stock_cjl = stock_cjl.pivot_table(values='成交量', index='交易日期', columns='证券名称')

    # 个股成交量总和时序
    stock_total_cjl_ts = stock_cjl.copy()
    stock_total_cjl_ts['全A股'] = stock_total_cjl_ts.apply(lambda x: x.sum(), axis='columns')
    all_stock_total_cjl_ts = stock_total_cjl_ts[['全A股']].reset_index()

    # first_5%
    first_5pct = int(len(Astock_dm) * 0.05)

    # first_10%
    first_10pct = int(len(Astock_dm) * 0.1)

    stock_cjl_ts = stock_cjl.T
    stock_cjl_ts = stock_cjl_ts.sort_values(by=stock_cjl_ts.columns.to_list(), ascending=False)

    # 前5%/10%成交量
    cjl_first_5pct = stock_cjl_ts.iloc[:first_5pct, :].T
    cjl_first_5pct['前5%成交量'] = cjl_first_5pct.apply(lambda x: x.sum(), axis='columns')
    cjl_first_5pct = cjl_first_5pct[['前5%成交量']].reset_index()

    cjl_first_10pct = stock_cjl_ts.iloc[:first_10pct, :].T
    cjl_first_10pct['前10%成交量'] = cjl_first_10pct.apply(lambda x: x.sum(), axis='columns')
    cjl_first_10pct = cjl_first_10pct[['前10%成交量']].reset_index()

    cjl_first_5pct_10pct = pd.merge(cjl_first_5pct, cjl_first_10pct, on='交易日期', how='left')
    cjl_first_5pct_10pct = pd.merge(cjl_first_5pct_10pct, all_stock_total_cjl_ts, on='交易日期', how='left')

    cjl_first_5pct_10pct['前5%成交量占比'] = 100 * (
                cjl_first_5pct_10pct['前5%成交量'] / cjl_first_5pct_10pct['全A股'])
    cjl_first_5pct_10pct['前10%成交量占比'] = 100 * (
                cjl_first_5pct_10pct['前10%成交量'] / cjl_first_5pct_10pct['全A股'])

    # 前5%/10%成交量时序
    cjl_first_5pct_10pct_ts = cjl_first_5pct_10pct[['交易日期', '前5%成交量', '前10%成交量', '全A股']]

    # 个股成交量集中度时序
    cjl_pct_first_5pct_10pct_ts = cjl_first_5pct_10pct[['交易日期', '前5%成交量占比', '前10%成交量占比']]

def etf_cjl(start_date,end_date,etf_path):
    # etf_path = r'D:\cyp\周度跟踪数据\数据源\ETF.xlsx'

    etf = pd.read_excel(etf_path)
    etf['基金代码'] = etf['证券代码'].str[0:6]

    for col in list(etf['证券简称'].unique()):
        if "300" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "300"

        if "500" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "500"

        if "1000" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "1000"

        if "2000" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "2000"

    etf_dm = tuple(etf['证券代码'].str[0:6].unique())

    sql_etf = "select jyrq 交易日期, jjdm 基金代码, zqmc 基金名称, cjjs 成交量 from st_fund.t_st_gm_jjjy \
               where jyrq >={0} and jyrq <={1} and jjdm in {2}".format(start_date, end_date, etf_dm)

    etf_cjl = get_df(sql_etf, db='funduser')
    etf_cjl = pd.merge(etf_cjl, etf[['基金代码', 'type']], on='基金代码', how='left')

    etf_cjl_300 = etf_cjl[etf_cjl['type'] == '300']
    etf_cjl_300 = etf_cjl_300.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_300['300成交量'] = etf_cjl_300.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_500 = etf_cjl[etf_cjl['type'] == '500']
    etf_cjl_500 = etf_cjl_500.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_500['500成交量'] = etf_cjl_500.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_1000 = etf_cjl[etf_cjl['type'] == '1000']
    etf_cjl_1000 = etf_cjl_1000.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_1000['1000成交量'] = etf_cjl_1000.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_2000 = etf_cjl[etf_cjl['type'] == '2000']
    etf_cjl_2000 = etf_cjl_2000.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_2000['2000成交量'] = etf_cjl_2000.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_300 = etf_cjl_300.reset_index()
    etf_cjl_300 = etf_cjl_300[['交易日期', '300成交量']]

    etf_cjl_500 = etf_cjl_500.reset_index()
    etf_cjl_500 = etf_cjl_500[['交易日期', '500成交量']]

    etf_cjl_1000 = etf_cjl_1000.reset_index()
    etf_cjl_1000 = etf_cjl_1000[['交易日期', '1000成交量']]

    etf_cjl_2000 = etf_cjl_2000.reset_index()
    etf_cjl_2000 = etf_cjl_2000[['交易日期', '2000成交量']]

    etf_cjls = pd.merge(etf_cjl_300, etf_cjl_500, on='交易日期', how='left')
    etf_cjls = pd.merge(etf_cjls, etf_cjl_1000, on='交易日期', how='left')
    etf_cjls = pd.merge(etf_cjls, etf_cjl_2000, on='交易日期', how='left')

