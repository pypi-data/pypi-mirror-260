"""
指增FOF组合优化专题报告代码
"""
import os

import numpy as np
import pandas as pd
import datetime
import riskfolio as rp
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import (get_fund_nav_from_sql, get_trading_day_list,
                                                               get_index_return_from_sql)
import statsmodels.api as sm
from hbshare.quant.Kevin.quant_room.MyUtil.util_func import cal_annual_return, \
    cal_annual_volatility, cal_sharpe_ratio, cal_max_drawdown
from tqdm import tqdm
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params, style_names
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class PortfolioConstructor:
    def __init__(self, start_date, end_date, path, reb_freq=3, back_window=12):
        """
        :param start_date: 回测的起始日期
        :param end_date: 结束日期
        :param path: 参数配置文件的路径
        :param reb_freq: 再平衡频率，单位：月
        :param back_window: 回看周期，单位：月
        """
        self.start_date = start_date
        self.end_date = end_date
        self.path = path
        self.reb_freq = reb_freq
        self.back_window = back_window

    def _load_data(self):
        config_df = pd.read_excel(os.path.join(self.path, "指增FOF优化的基金池.xlsx"), sheet_name=0)
        config_df['净值起始'] = config_df['净值起始'].fillna("20991231")
        config_df['净值起始'] = config_df['净值起始'].apply(lambda x: x.strftime('%Y%m%d')).replace('20991231', np.NaN)
        config_df['入池日期'] = config_df['入池日期'].apply(lambda x: x.strftime('%Y%m%d'))
        start_dt = datetime.datetime.strptime(self.start_date, '%Y%m%d')
        pre_date = (start_dt - datetime.timedelta(days=500)).strftime('%Y%m%d')
        week_list = get_trading_day_list(pre_date, self.end_date, "week")
        # 定位起始日和调仓日
        tmp = pd.Series(index=week_list, data=1.).to_frame('date')
        tmp['trade_date'] = tmp.index
        tmp['trade_dt'] = tmp['trade_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y%m%d"))
        tmp['month'] = tmp['trade_dt'].apply(lambda x: x.month)
        tmp['year'] = tmp['trade_dt'].apply(lambda x: x.year)
        month_end = tmp[tmp['month'].shift(-1) != tmp['month']]['trade_date'].tolist()
        reb_dates = month_end[month_end.index(self.start_date) - self.back_window::self.reb_freq]
        data_start = reb_dates[0]
        reb_dates = [x for x in reb_dates if x >= self.start_date]
        # 净值数据
        fund_dict = config_df.set_index('基金名称')['基金代码'].to_dict()
        fund_nav = get_fund_nav_from_sql(data_start, self.end_date, fund_dict).reindex(week_list).loc[data_start:]

        assert (config_df.shape[0] == fund_nav.shape[1])

        # 先用均值填充，再定位
        median_df = fund_nav.pct_change(limit=1).median(axis=1).fillna(0.)
        nav_start_dict = config_df.set_index('基金名称')['净值起始'].to_dict()
        for key, value in nav_start_dict.items():
            nav_series = fund_nav[key].copy()
            cp_df = nav_series.pct_change(limit=1).to_frame(key).merge(
                median_df.to_frame('中位数'), left_index=True, right_index=True)
            cp_df[key] = np.where(cp_df[key].isnull(), cp_df['中位数'], cp_df[key])
            # 定位
            if value in week_list:
                date1 = week_list[week_list.index(value) - 1]
                cp_df.loc[:date1, key] = np.NaN

            fund_nav[key] = (1 + cp_df[key]).cumprod()

        self.data_param = {
            "fund_nav": fund_nav,
            "reb_dates": reb_dates,
            "month_end": month_end,
            "config_df": config_df
        }

    @staticmethod
    def prepare_factor_return(start_date, end_date):
        trading_day_list = get_trading_day_list(start_date, end_date, "week")
        sql_script = ("SELECT * FROM factor_return where "
                      "TRADE_DATE >= {} and TRADE_DATE <= {}").format(start_date, end_date)
        engine = create_engine(engine_params)
        factor_return = pd.read_sql(sql_script, engine)
        factor_return['trade_date'] = factor_return['trade_date'].apply(
            lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        factor_return = pd.pivot_table(
            factor_return, index='trade_date', columns='factor_name', values='factor_ret').sort_index()
        factor_return = (1 + factor_return).cumprod().reindex(trading_day_list).pct_change().dropna()[style_names]

        return factor_return

    @staticmethod
    def calc_portfolio_index(nav_df):
        portfolio_index_df = pd.DataFrame(
            index=nav_df.columns, columns=['超额年化收益', '超额年化波动', '最大回撤', 'Sharpe', '胜率', '平均损益比'])
        portfolio_index_df.loc[:, '超额年化收益'] = nav_df.pct_change().dropna(how='all').apply(cal_annual_return, axis=0)
        portfolio_index_df.loc[:, '超额年化波动'] = \
            nav_df.pct_change().dropna(how='all').apply(cal_annual_volatility, axis=0)
        portfolio_index_df.loc[:, '最大回撤'] = nav_df.apply(cal_max_drawdown, axis=0)
        portfolio_index_df.loc[:, 'Sharpe'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
        portfolio_index_df.loc[:, '胜率'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: x.gt(0).sum() / len(x), axis=0)
        portfolio_index_df.loc[:, '平均损益比'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: x[x > 0].mean() / x[x < 0].abs().mean(), axis=0)
        portfolio_index_df.index.name = '产品名称'
        portfolio_index_df.reset_index(inplace=True)
        # 格式处理
        portfolio_index_df['超额年化收益'] = portfolio_index_df['超额年化收益'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['超额年化波动'] = portfolio_index_df['超额年化波动'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['最大回撤'] = portfolio_index_df['最大回撤'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['Sharpe'] = portfolio_index_df['Sharpe'].round(2)
        portfolio_index_df['胜率'] = portfolio_index_df['胜率'].apply(lambda x: format(x, '.1%'))
        portfolio_index_df['平均损益比'] = portfolio_index_df['平均损益比'].round(2)

        return portfolio_index_df

    def optimization(self, Y, model_param):
        config_df = self.data_param['config_df']
        universe_df = config_df[config_df['基金名称'].isin(Y.columns)]
        # 线性约束
        asset_classes = universe_df.rename(
            columns={"基金名称": "Assets", "三级策略": "Class1", "管理人": "Class2"})[['Assets', 'Class1', 'Class2']]
        linear_constraints = pd.read_excel(os.path.join(self.path, "优化配置文件.xlsx"), sheet_name="线性约束")
        # 单个管理人的约束
        append_cons = pd.DataFrame(columns=linear_constraints.columns)
        append_cons['Position'] = asset_classes['Class2'].unique()
        append_cons['Disabled'] = False
        append_cons['Type'] = 'Classes'
        append_cons['Set'] = 'Class2'
        append_cons['Sign'] = '<='
        append_cons['Weight'] = 0.15
        linear_constraints = pd.concat([linear_constraints, append_cons], axis=0)
        A, B = rp.assets_constraints(linear_constraints, asset_classes)
        # 优化参数
        port = rp.Portfolio(returns=Y)
        # method_mu = "hist"
        # method_cov = "hist"
        method_mu = "ewma1"
        method_cov = "ewma2"
        port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.974)  # 半衰期

        port.ainequality = A
        port.binequality = B

        model = 'Classic'
        rm = 'MV'
        obj = model_param["obj"]  # MinRisk, MaxRet, Utility or Sharpe
        hist = True
        rf = 0
        l = model_param["risk_aversion"]  # Risk aversion factor

        w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
        # ax = rp.plot_pie(w=w_effective, title='Sharpe Mean Variance', others=0.0, nrow=25, cmap="tab20",
        #                  height=6, width=10, ax=None)
        # 有效前沿
        # points = 50
        # frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)
        # # Plotting the efficient frontier in Std. Dev. dimension
        # label = 'Max Utility Portfolio'
        # mu = port.mu  # Expected returns
        # cov = port.cov  # Covariance matrix
        # returns = port.returns  # Returns of the assets
        # ax = rp.plot_frontier(w_frontier=frontier, mu=mu, cov=cov, returns=returns, rm=rm,
        #                       rf=rf, alpha=0.05, cmap='viridis', w=w, label=label,
        #                       marker='*', s=16, c='r', height=6, width=10, ax=None, t_factor=52)

        return w


    def run(self):
        self._load_data()
        data_param = self.data_param
        reb_dates = data_param["reb_dates"]
        fund_nav = data_param["fund_nav"]
        config_df = data_param["config_df"]
        weight_list = []
        ret_list = []
        reb_dates.append(self.end_date)
        print("开始优化...")
        for reb_date in tqdm(reb_dates[-2:-1]):
            print("优化日期: {}".format(reb_date))
            month_end = data_param["month_end"]
            if reb_date < reb_dates[2]:
                back_window = 6
            else:
                back_window = self.back_window
            p_start = month_end[month_end.index(reb_date) - back_window]
            period_data = fund_nav.loc[p_start: reb_date]
            universe = config_df[config_df['入池日期'] <= reb_date]['基金名称'].tolist()
            universe_data = period_data[universe].dropna(axis=1)
            # 处理成超额
            benchmark_df = get_index_return_from_sql(p_start, reb_date, "000905")
            benchmark_return = benchmark_df.reindex(universe_data.index).pct_change().dropna()
            return_df = universe_data.pct_change().dropna().sub(benchmark_return, axis=0)
            # 处理正定的问题：N <= T
            T, N = return_df.shape[0], return_df.shape[1]
            if T > N:
                universe = universe_data.columns.tolist()
            else:  # 剔除处理
                annual_return = (1 + return_df).prod() ** (52 / T) - 1
                annual_vol = return_df.std() * np.sqrt(52)
                status_df = annual_return.to_frame('an_ret').merge(
                    annual_vol.to_frame('an_vol'), left_index=True, right_index=True)
                while status_df.shape[0] >= T:
                    status_df = status_df[(status_df['an_ret'] >= status_df['an_ret'].median()) |
                                            (status_df['an_vol'] <= status_df['an_vol'].median())]
                universe = status_df.index.tolist()
            return_df = return_df[universe]
            # 风格收益
            # factor_return = self.prepare_factor_return(p_start, reb_date)
            # optimization
            model_param = {"obj": "Utility", "risk_aversion": 20}
            opt_w = self.optimization(return_df, model_param)
            w_effective = opt_w[opt_w['weights'] >= 1e-6]
            weight_list.append(w_effective.rename(columns={"weights": reb_date}))
            # 计算组合收益
            next_reb = reb_dates[reb_dates.index(reb_date) + 1]
            future_data = fund_nav.loc[reb_date: next_reb, universe].copy()
            future_data /= future_data.iloc[0]
            port_ret = future_data.dot(opt_w).pct_change()
            benchmark_return_fu = get_index_return_from_sql(reb_date, next_reb, "000905").reindex(
                port_ret.index).pct_change()
            port_ret = port_ret.merge(benchmark_return_fu, left_index=True, right_index=True).dropna()
            port_ret.rename(columns={"weights": "组合", "TCLOSE": "中证500"}, inplace=True)
            # 添加等权组合
            ave_ret = future_data.mean(axis=1).pct_change().dropna().to_frame('等权组合')
            port_ret = port_ret.merge(ave_ret, left_index=True, right_index=True)
            ret_list.append(port_ret)

        weight_df = pd.concat(weight_list, axis=1)
        # 回测净值
        ret_df = pd.concat(ret_list)
        # 衍复500做对比
        yf_nav = get_fund_nav_from_sql(self.start_date, self.end_date, {"衍复": "SJH866"})
        date_list = get_trading_day_list(self.start_date, self.end_date, "week")
        yf_return = yf_nav.reindex(date_list).pct_change().dropna()
        ret_df = ret_df.merge(yf_return, left_index=True, right_index=True)
        ret_df.loc[self.start_date] = 0.
        ret_df.sort_index(inplace=True)
        ret_df.eval("组合超额 = 组合 - 中证500", inplace=True)
        ret_df.eval("衍复超额 = 衍复 - 中证500", inplace=True)
        ret_df.eval("等权组合超额 = 等权组合 - 中证500", inplace=True)
        nav_df = (1 + ret_df).cumprod()

        portfolio_index_df = self.calc_portfolio_index(nav_df[['组合超额', '衍复超额', '等权组合超额']])

        return weight_df, nav_df, portfolio_index_df


if __name__ == '__main__':
    data_path = "D:\\研究基地\\G-专题报告\\【2024.1】FOF的组合配置优化"
    PortfolioConstructor("20201231", "20240223", data_path).run()