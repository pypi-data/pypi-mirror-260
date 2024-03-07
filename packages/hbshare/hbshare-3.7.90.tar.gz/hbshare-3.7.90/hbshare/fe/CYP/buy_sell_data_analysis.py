import pandas as pd
import plotly.graph_objects as go
import hbshare as hbs
hbs.set_token("qwertyuisdfghjkxcvbn1000")

import plotly.io as pio
pio.renderers.default = 'browser'

def get_df(sql, db, page_size=2000):
    data = hbs.db_data_query(db, sql, page_size=page_size, timeout=120)
    pages = data['pages']
    data = pd.DataFrame(data['data'])
    if pages > 1:
        for page in range(2, pages + 1):
            temp_data = hbs.db_data_query(db, sql, page_size=page_size, page_num=page, timeout=120)
            data = pd.concat([data, pd.DataFrame(temp_data['data'])], axis=0)
    return data

def buy_sell_data_process(data_path,quant_strat_path,start_date,end_date):
    start_date = start_date
    end_date = end_date
    buy_sell_df = pd.read_excel(data_path)
    buy_sell_df = buy_sell_df.dropna()
    buy_sell_df = buy_sell_df[~(buy_sell_df['一级策略标签'].isin(['另类']))]
    buy_sell_df = buy_sell_df[~(buy_sell_df['资配二级'].isin(['暂不放','另类']))]
    buy_sell_df.loc[buy_sell_df[buy_sell_df['基金简称'].str.contains('明汯股票精选')].index, '大类标签'] = '量化'

    def zs_month_nav_get(end_date):
        sql_hb = "select zsdm 指数代码,tjyf 年月, hb1y 月回报 from st_hedge.t_st_sm_zhmzsyhb where rqzh <= {0} and zsdm in ('HB1001','HB1002') and hb1y!=99999".format(end_date)
        hb_index = get_df(sql_hb,db='highuser')
        hb_index['指数代码'].replace(["HB1001","HB1002"],["好买主观多头指数","好买量化多头指数"],inplace=True)
        hb_index = hb_index.pivot_table(values='月回报',index='年月',columns='指数代码')
        hb_index = hb_index.reset_index()

        sql_index = "select zqdm 指数代码,tjyf 年月, hb1y 月回报 from st_market.t_st_zs_yhb where rqzh <= {0} and zqdm in ('CBA00301') and hb1y!=99999".format(end_date)
        zz_index = get_df(sql_index,db='alluser')
        zz_index['指数代码'].replace('CBA00301','中债-总财富指数',inplace=True)
        zz_index = zz_index.pivot_table(values='月回报',index='年月',columns='指数代码')
        zz_index = zz_index.reset_index()

        zs_index = pd.merge(hb_index,zz_index,on='年月',how='left')
        zs_index.set_index('年月',inplace=True)

        zs_index_nav = (zs_index.fillna(0) / 100 + 1).cumprod()

        return zs_index_nav
        # # 归一化处理
        # zs_index_nav = zs_index_nav / zs_index_nav.iloc[0, :]

    global zs_nav
    zs_nav = zs_month_nav_get(end_date)

    # 分类~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # 大类标签
    # 固收 -> 固定收益
    buy_sell_df.loc[buy_sell_df[(buy_sell_df['一级策略标签'].isin(['固定收益']))|(buy_sell_df['资配二级'].isin(['类固收']))].index,'大类标签'] = '固定收益'
    # 宏多 -> 宏观对冲_多策略
    buy_sell_df.loc[buy_sell_df[(buy_sell_df['资配二级'].isin(['多策略（非多空）','宏观对冲']))].index,'大类标签'] = '宏观对冲_多策略'
    # 主观 -> 主观股票
    buy_sell_df.loc[buy_sell_df[(buy_sell_df['资配二级'].isin(['主观股票']))].index,'大类标签'] = '主观'
    # 量化 -> CTA, 市场中性, 量化指增, 灵活对冲
    buy_sell_df.loc[buy_sell_df[buy_sell_df['大类标签'].isna()].index,'大类标签'] = '量化'

    # 操作类型 -> buy or sell
    buy_sell_df.loc[buy_sell_df[(buy_sell_df['交易类型'].isin(['申购确认','认购确认']))].index,'操作类型'] = 'buy'
    buy_sell_df.loc[buy_sell_df[(buy_sell_df['交易类型'].isin(['赎回确认']))].index,'操作类型'] = 'sell'

    # 年月标签
    buy_sell_df['年月'] = buy_sell_df['交易日期'].astype(str).str[0:6]

    # 最新一周的截面数据
    dates = buy_sell_df['交易日期'].unique().tolist()
    last_week_dates = dates[-5:]
    buy_sell_df_week = buy_sell_df[(buy_sell_df['交易日期'].isin(last_week_dates))].reset_index(drop=True)

    # 按大类标签分组计算最新一周申赎份额
    buy_sell_df_week_1 = buy_sell_df_week.groupby(['交易日期','大类标签','操作类型'])[['确认份额']].sum().reset_index().sort_values(by=['交易日期','大类标签'])

    # 计算周度净申赎份额函数
    def cal_net_buy_sell_week(buy_sell_df_week_1):
        buy_sell_df_temp = buy_sell_df_week_1.copy()
        for date in buy_sell_df_temp['交易日期'].unique().tolist():
            temp_df = buy_sell_df_temp[buy_sell_df_temp['交易日期']==date]
            for type in temp_df['大类标签'].unique().tolist():
                temp_df2 = temp_df[temp_df['大类标签']==type]
                if len(temp_df2['操作类型'].unique()) == 1:
                    if 'sell' in temp_df2['操作类型'].unique():
                        temp_df3 = temp_df2.copy()
                        temp_df3['操作类型'] = 'net'
                        temp_df3['确认份额'] = 0 - temp_df3['确认份额']
                        buy_sell_df_temp = pd.concat([buy_sell_df_temp,temp_df3],axis='rows',ignore_index=True)
                    if 'buy' in temp_df2['操作类型'].unique():
                        temp_df3 = temp_df2.copy()
                        temp_df3['操作类型'] = 'net'
                        temp_df3['确认份额'] = temp_df3['确认份额'] - 0
                        buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df3], axis='rows', ignore_index=True)
                else:
                    temp_df3 = temp_df2.copy()
                    temp_df4 = pd.DataFrame(columns=temp_df3.columns)
                    net_amounts = temp_df3.loc[temp_df3['操作类型'] == 'buy','确认份额'].values[0] - temp_df3.loc[temp_df3['操作类型'] == 'sell','确认份额'].values[0]
                    temp_df4['交易日期'] = temp_df3['交易日期'].unique()
                    temp_df4['大类标签'] = temp_df3['大类标签'].unique()
                    temp_df4['操作类型'] = 'net'
                    temp_df4['确认份额'] = net_amounts
                    buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df4], axis='rows', ignore_index=True)

        buy_sell_df_temp = buy_sell_df_temp.sort_values(by=['交易日期','大类标签']).reset_index(drop=True)
        return buy_sell_df_temp

    # 计算周度净申赎份额
    buy_sell_df_week_2 = cal_net_buy_sell_week(buy_sell_df_week_1)
    buy_sell_df_week_2['确认份额'] = buy_sell_df_week_2['确认份额'].astype(int)

    # 最近一周度数据整合
    buy_sell_df_week_final = buy_sell_df_week_2.groupby(['大类标签','操作类型'])['确认份额'].sum().reset_index()
    buy_sell_df_week_final = buy_sell_df_week_final.pivot_table(values='确认份额',index='操作类型',columns='大类标签')
    buy_sell_df_week_final = buy_sell_df_week_final.T
    buy_sell_df_week_final = buy_sell_df_week_final[['buy','sell','net']]
    buy_sell_df_week_final = buy_sell_df_week_final.T

    # 周度申赎截面柱状图函数
    def plot_bar_week(buy_sell_df_week_final,title_name):

        fig = go.Figure()
        def add_bar(class_name):

            buy_sell_df_week_final_temp = buy_sell_df_week_final[[class_name]]
            operation_types = buy_sell_df_week_final.index.tolist()
            x_list = operation_types
            y_list = buy_sell_df_week_final_temp[class_name].tolist()

            if class_name == '主观': each_color='#1f77b4'
            if class_name == '量化': each_color = '#d62728'
            if class_name == '宏观对冲_多策略': each_color = '#2ca02c'
            if class_name == '固定收益': each_color = '#9467bd'

            fig.add_bar(x=x_list,
                        y=y_list,
                        name=class_name,
                        marker=dict(color=each_color))

        for class_name in buy_sell_df_week_final.columns.tolist():
            add_bar(class_name)

        fig.layout.bargap = 0.5
        fig.update_layout(barmode="group",width=1600,title=title_name)

        fig.show()

    plot_bar_week(buy_sell_df_week_final,title_name=str(last_week_dates[0])+'-'+str(last_week_dates[-1])+' 周度申赎柱状图')

    # 按大类标签分组计算月度申赎份额
    buy_sell_df_1 = buy_sell_df.groupby(['年月','大类标签','操作类型'])[['确认份额']].sum().reset_index().sort_values(by=['年月','大类标签'])

    # 计算月度净申赎份额函数
    def cal_net_buy_sell_month(buy_sell_df_1):
        buy_sell_df_temp = buy_sell_df_1.copy()
        for month in buy_sell_df_temp['年月'].unique().tolist():
            temp_df = buy_sell_df_temp[buy_sell_df_temp['年月']==month]
            for type in temp_df['大类标签'].unique().tolist():
                temp_df2 = temp_df[temp_df['大类标签']==type]
                if len(temp_df2['操作类型'].unique()) == 1:
                    if 'sell' in temp_df2['操作类型'].unique():
                        temp_df3 = temp_df2.copy()
                        temp_df3['操作类型'] = 'net'
                        temp_df3['确认份额'] = 0 - temp_df3['确认份额']
                        buy_sell_df_temp = pd.concat([buy_sell_df_temp,temp_df3],axis='rows',ignore_index=True)
                    if 'buy' in temp_df2['操作类型'].unique():
                        temp_df3 = temp_df2.copy()
                        temp_df3['操作类型'] = 'net'
                        temp_df3['确认份额'] = temp_df3['确认份额'] - 0
                        buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df3], axis='rows', ignore_index=True)
                else:
                    temp_df3 = temp_df2.copy()
                    temp_df4 = pd.DataFrame(columns=temp_df3.columns)
                    net_amounts = temp_df3.loc[temp_df3['操作类型'] == 'buy','确认份额'].values[0] - temp_df3.loc[temp_df3['操作类型'] == 'sell','确认份额'].values[0]
                    temp_df4['年月'] = temp_df3['年月'].unique()
                    temp_df4['大类标签'] = temp_df3['大类标签'].unique()
                    temp_df4['操作类型'] = 'net'
                    temp_df4['确认份额'] = net_amounts
                    buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df4], axis='rows', ignore_index=True)

        buy_sell_df_temp = buy_sell_df_temp.sort_values(by=['年月','大类标签']).reset_index(drop=True)
        return buy_sell_df_temp

    # 计算月度净申赎份额
    buy_sell_df_2 = cal_net_buy_sell_month(buy_sell_df_1)
    buy_sell_df_2['确认份额'] = buy_sell_df_2['确认份额'].astype(int)

    # 月度申赎时序柱状图函数
    def plot_bar_month(buy_sell_df_2,title_name,zs_nav_each):

        zs_nav_ts = zs_nav_each.copy().set_index('年月')
        #归一化处理
        zs_nav_ts = zs_nav_ts / zs_nav_ts.iloc[0,:]

        fig = go.Figure()

        for class_name in buy_sell_df_2['大类标签'].unique().tolist():
            temp_buy_sell_df_2 = buy_sell_df_2[buy_sell_df_2['大类标签']==class_name]
            year_month_list = temp_buy_sell_df_2['年月'].tolist()
            x_list = year_month_list
            y_list = temp_buy_sell_df_2['确认份额'].astype(int).tolist()

            if class_name == '主观': each_color='#1f77b4'
            if class_name == '量化': each_color = '#d62728'
            if class_name == '宏观对冲_多策略': each_color = '#2ca02c'
            if class_name == '固定收益': each_color = '#9467bd'

            fig.add_bar(x=x_list,
                        y=y_list,
                        name=class_name,
                        marker=dict(color=each_color))

        for zs_name in ['好买主观多头指数', '好买量化多头指数', '中债-总财富指数']:
            if zs_name == '好买主观多头指数': each_color = 'blue'
            if zs_name == '好买量化多头指数': each_color = 'red'
            if zs_name == '中债-总财富指数': each_color = 'purple'

            fig.add_trace(
                go.Scatter(
                    x=zs_nav_ts.index.tolist(),
                    y=zs_nav_ts[zs_name].values.tolist(),
                    name=zs_name,
                    xaxis='x',
                    yaxis='y2',
                    marker=dict(color=each_color)))

        fig.layout.bargap = 0.5
        fig.update_layout(barmode='group',width=1600, title=title_name,yaxis2=dict(anchor='x', overlaying='y', side='right'))

        fig.show()

    years = buy_sell_df_2['年月'].str[0:4].unique().tolist()
    years.reverse()

    for year in years:
        each_year_buy_sell_df = buy_sell_df_2[buy_sell_df_2['年月'].str.contains(year)].reset_index(drop=True)
        for each_operation in ['净申赎','申购','赎回']:
            if each_operation == '净申赎':
                eng_operation = 'net'
            if each_operation == '申购':
                eng_operation = 'buy'
            if each_operation == '赎回':
                eng_operation = 'sell'
            each_year_buy_sell_df_new = each_year_buy_sell_df[each_year_buy_sell_df['操作类型']==eng_operation]
            zs_nav_each = zs_nav.reset_index().copy()
            zs_nav_each = zs_nav_each[zs_nav_each['年月'].astype(str).str.contains(year)]
            year_month_list = each_year_buy_sell_df_new['年月'].astype(int).unique().tolist()
            zs_nav_each = zs_nav_each[(zs_nav_each['年月'].isin(year_month_list))]
            plot_bar_month(each_year_buy_sell_df_new,title_name=year+" 月度"+each_operation+"时序图",zs_nav_each=zs_nav_each)

    # 量化按策略细分
    def quant_detail(buy_sell_df,start_date,end_date):
        quant_strat = pd.read_excel(quant_strat_path)
        quant_strat = quant_strat[['基金代码', '二级策略']]
        quant_strat = quant_strat.drop_duplicates()

        buy_sell_df_quant = buy_sell_df[buy_sell_df['大类标签']=='量化'].reset_index(drop=True)
        buy_sell_df_quant = pd.merge(buy_sell_df_quant,quant_strat,on='基金代码',how='left')

        buy_sell_df_quant.loc[buy_sell_df_quant[buy_sell_df_quant['二级策略'].isna()].index,'二级策略'] = buy_sell_df_quant.loc[buy_sell_df_quant[buy_sell_df_quant['二级策略'].isna()].index,'资配二级']

        # 量化一级标签
        # 量化股票
        buy_sell_df_quant.loc[buy_sell_df_quant[(buy_sell_df_quant['二级策略'].isin(['量化多头','量化多头（美元）',
        '1000指数增强','1000指增','500指数增强','500指增','500指数增强（美元）','300指数增强','小市值指数增强',
        '2000指数增强']))].index, '量化一级标签'] = '量化股票'
        # 管理期货
        buy_sell_df_quant.loc[buy_sell_df_quant[(buy_sell_df_quant['二级策略'].isin(['CTA','混合多策略CTA','混合类CTA',
        '主观CTA','趋势CTA','趋势CTA（美元）','趋势类CTA','短周期CTA','管理期货','基本面量化CTA',
        '横截面CTA','高频CTA','量化CTA']))].index, '量化一级标签'] = '管理期货'
        # 市场中性
        buy_sell_df_quant.loc[buy_sell_df_quant[(buy_sell_df_quant['二级策略'].isin(['市场中性','混合市场中性',
        '混合市场中性（美元）','股票 - 市场中性','1000市场中性',
        '500市场中性','300市场中性','T0']))].index, '量化一级标签'] = '市场中性'
        # 多空仓型
        buy_sell_df_quant.loc[buy_sell_df_quant[(buy_sell_df_quant['二级策略'].isin(['灵活对冲',
        '量化多空']))].index, '量化一级标签'] = '多空仓型'

        # 最新一周的截面数据
        buy_sell_df_quant_week = buy_sell_df_quant[
        (buy_sell_df_quant['交易日期']>=start_date)&(buy_sell_df_quant['交易日期']<=end_date)].reset_index(drop=True)
        last_week_dates = buy_sell_df_quant_week['交易日期'].unique().tolist()

        # 按量化一级标签分组计算最新一周申赎份额
        buy_sell_df_quant_week_1 = buy_sell_df_quant_week.groupby(['交易日期', '量化一级标签', '操作类型'])[
            ['确认份额']].sum().reset_index().sort_values(by=['交易日期', '量化一级标签'])

        # 计算量化周度净申赎份额函数
        def cal_net_buy_sell_quant_week(buy_sell_df_quant_week_1):
            buy_sell_df_temp = buy_sell_df_quant_week_1.copy()
            for date in buy_sell_df_temp['交易日期'].unique().tolist():
                temp_df = buy_sell_df_temp[buy_sell_df_temp['交易日期'] == date]
                for type in temp_df['量化一级标签'].unique().tolist():
                    temp_df2 = temp_df[temp_df['量化一级标签'] == type]
                    if len(temp_df2['操作类型'].unique()) == 1:
                        if 'sell' in temp_df2['操作类型'].unique():
                            temp_df3 = temp_df2.copy()
                            temp_df3['操作类型'] = 'net'
                            temp_df3['确认份额'] = 0 - temp_df3['确认份额']
                            buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df3], axis='rows', ignore_index=True)
                        if 'buy' in temp_df2['操作类型'].unique():
                            temp_df3 = temp_df2.copy()
                            temp_df3['操作类型'] = 'net'
                            temp_df3['确认份额'] = temp_df3['确认份额'] - 0
                            buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df3], axis='rows', ignore_index=True)
                    else:
                        temp_df3 = temp_df2.copy()
                        temp_df4 = pd.DataFrame(columns=temp_df3.columns)
                        net_amounts = temp_df3.loc[temp_df3['操作类型'] == 'buy', '确认份额'].values[0] - \
                                      temp_df3.loc[temp_df3['操作类型'] == 'sell', '确认份额'].values[0]
                        temp_df4['交易日期'] = temp_df3['交易日期'].unique()
                        temp_df4['量化一级标签'] = temp_df3['量化一级标签'].unique()
                        temp_df4['操作类型'] = 'net'
                        temp_df4['确认份额'] = net_amounts
                        buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df4], axis='rows', ignore_index=True)

            buy_sell_df_temp = buy_sell_df_temp.sort_values(by=['交易日期', '量化一级标签']).reset_index(drop=True)
            return buy_sell_df_temp

        # 计算量化周度净申赎份额
        buy_sell_df_quant_week_2 = cal_net_buy_sell_quant_week(buy_sell_df_quant_week_1)
        buy_sell_df_quant_week_2['确认份额'] = buy_sell_df_quant_week_2['确认份额'].astype(int)

        buy_sell_df_quant_week_final = buy_sell_df_quant_week_2.groupby(['量化一级标签', '操作类型'])[
            '确认份额'].sum().reset_index()
        buy_sell_df_quant_week_final = buy_sell_df_quant_week_final.pivot_table(values='确认份额', index='操作类型',
                                                                                columns='量化一级标签')
        buy_sell_df_quant_week_final = buy_sell_df_quant_week_final.T
        buy_sell_df_quant_week_final = buy_sell_df_quant_week_final[['buy', 'sell', 'net']]
        buy_sell_df_quant_week_final = buy_sell_df_quant_week_final.T

        # 输出到函数之外
        global buy_sell_df_quant_week_final_copy
        buy_sell_df_quant_week_final_copy = buy_sell_df_quant_week_final.copy()

        # 量化周度申赎截面柱状图函数
        def plot_bar_quant_week(buy_sell_df_quant_week_final, title_name):

            fig = go.Figure()

            def add_bar(class_name):
                buy_sell_df_quant_week_final_temp = buy_sell_df_quant_week_final[[class_name]]
                operation_types = buy_sell_df_quant_week_final.index.tolist()
                x_list = operation_types
                y_list = buy_sell_df_quant_week_final_temp[class_name].tolist()

                if class_name == '管理期货': each_color = '#1f77b4'
                if class_name == '量化股票': each_color = '#d62728'
                if class_name == '市场中性': each_color = '#2ca02c'
                if class_name == '多空仓型': each_color = '#9467bd'

                fig.add_bar(x=x_list,
                            y=y_list,
                            name=class_name,
                            marker=dict(color=each_color))

            for class_name in buy_sell_df_quant_week_final.columns.tolist():
                add_bar(class_name)

            fig.layout.bargap = 0.5
            fig.update_layout(barmode="group", width=1600, title=title_name)

            fig.show()

        plot_bar_quant_week(buy_sell_df_quant_week_final,
                      title_name=str(last_week_dates[0]) + '-' + str(last_week_dates[-1]) + ' 量化周度申赎柱状图')

        # 按量化一级标签分组计算月度申赎份额
        buy_sell_df_quant_1 = buy_sell_df_quant.groupby(['年月', '量化一级标签', '操作类型'])[
            ['确认份额']].sum().reset_index().sort_values(by=['年月', '量化一级标签'])

        # 计算量化月度净申赎份额函数
        def cal_net_buy_sell_quant_month(buy_sell_df_quant_1):
            buy_sell_df_temp = buy_sell_df_quant_1.copy()
            for month in buy_sell_df_temp['年月'].unique().tolist():
                temp_df = buy_sell_df_temp[buy_sell_df_temp['年月'] == month]
                for type in temp_df['量化一级标签'].unique().tolist():
                    temp_df2 = temp_df[temp_df['量化一级标签'] == type]
                    if len(temp_df2['操作类型'].unique()) == 1:
                        if 'sell' in temp_df2['操作类型'].unique():
                            temp_df3 = temp_df2.copy()
                            temp_df3['操作类型'] = 'net'
                            temp_df3['确认份额'] = 0 - temp_df3['确认份额']
                            buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df3], axis='rows', ignore_index=True)
                        if 'buy' in temp_df2['操作类型'].unique():
                            temp_df3 = temp_df2.copy()
                            temp_df3['操作类型'] = 'net'
                            temp_df3['确认份额'] = temp_df3['确认份额'] - 0
                            buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df3], axis='rows', ignore_index=True)
                    else:
                        temp_df3 = temp_df2.copy()
                        temp_df4 = pd.DataFrame(columns=temp_df3.columns)
                        net_amounts = temp_df3.loc[temp_df3['操作类型'] == 'buy', '确认份额'].values[0] - \
                                      temp_df3.loc[temp_df3['操作类型'] == 'sell', '确认份额'].values[0]
                        temp_df4['年月'] = temp_df3['年月'].unique()
                        temp_df4['量化一级标签'] = temp_df3['量化一级标签'].unique()
                        temp_df4['操作类型'] = 'net'
                        temp_df4['确认份额'] = net_amounts
                        buy_sell_df_temp = pd.concat([buy_sell_df_temp, temp_df4], axis='rows', ignore_index=True)

            buy_sell_df_temp = buy_sell_df_temp.sort_values(by=['年月', '量化一级标签']).reset_index(drop=True)
            return buy_sell_df_temp

        # 计算量化月度净申赎份额
        buy_sell_df_quant_2 = cal_net_buy_sell_quant_month(buy_sell_df_quant_1)
        buy_sell_df_quant_2['确认份额'] = buy_sell_df_quant_2['确认份额'].astype(int)

        # 量化月度申赎时序柱状图函数
        def plot_bar_quant_month(buy_sell_df_quant_2, title_name,zs_nav_each):

            zs_nav_ts = zs_nav_each.copy().set_index('年月')
            # 归一化处理
            zs_nav_ts = zs_nav_ts / zs_nav_ts.iloc[0, :]

            fig = go.Figure()

            len_df = []
            name = []

            for class_name_bis in buy_sell_df_quant_2['量化一级标签'].unique().tolist():
                temp_df = buy_sell_df_quant_2[buy_sell_df_quant_2['量化一级标签'] == class_name_bis]
                len_df.append(len(temp_df))
                name.append(temp_df['量化一级标签'].unique()[0])

            max_val = max(len_df)
            max_position = len_df.index(max_val)

            first_class = name[max_position]

            class_name_list = buy_sell_df_quant_2['量化一级标签'].unique().tolist()
            class_name_list.remove(first_class)
            class_name_list.insert(0,first_class)

            for class_name in class_name_list:
                temp_buy_sell_df_quant_2 = buy_sell_df_quant_2[buy_sell_df_quant_2['量化一级标签'] == class_name]
                year_month_list = temp_buy_sell_df_quant_2['年月'].tolist()
                x_list = year_month_list
                y_list = temp_buy_sell_df_quant_2['确认份额'].astype(int).tolist()

                if class_name == '管理期货': each_color = '#1f77b4'
                if class_name == '量化股票': each_color = '#d62728'
                if class_name == '市场中性': each_color = '#2ca02c'
                if class_name == '多空仓型': each_color = '#9467bd'

                fig.add_bar(x=x_list,
                            y=y_list,
                            name=class_name,
                            marker=dict(color=each_color))

            for zs_name in ['好买量化多头指数']:
                if zs_name == '好买量化多头指数': each_color = 'hotpink'

                fig.add_trace(
                    go.Scatter(
                        x=zs_nav_ts.index.tolist(),
                        y=zs_nav_ts[zs_name].values.tolist(),
                        name=zs_name,
                        xaxis='x',
                        yaxis='y2',
                        marker=dict(color=each_color)))

            fig.layout.bargap = 0.5
            fig.update_layout(barmode='group', width=1600, title=title_name,
                              yaxis2=dict(anchor='x', overlaying='y', side='right'))

            fig.show()

        years_quant = buy_sell_df_quant_2['年月'].str[0:4].unique().tolist()
        years_quant.reverse()

        for year_quant in years_quant:
            each_year_buy_sell_qaunt_df = buy_sell_df_quant_2[buy_sell_df_quant_2['年月'].str.contains(year_quant)].reset_index(drop=True)
            for each_operation in ['净申赎', '申购', '赎回']:
                if each_operation == '净申赎':
                    eng_operation = 'net'
                if each_operation == '申购':
                    eng_operation = 'buy'
                if each_operation == '赎回':
                    eng_operation = 'sell'
                each_year_buy_sell_quant_df_new = each_year_buy_sell_qaunt_df[each_year_buy_sell_qaunt_df['操作类型'] == eng_operation]
                zs_nav_each = zs_nav.reset_index().copy()
                zs_nav_each = zs_nav_each[zs_nav_each['年月'].astype(str).str.contains(year_quant)]
                year_month_list = each_year_buy_sell_quant_df_new['年月'].astype(int).unique().tolist()
                zs_nav_each = zs_nav_each[(zs_nav_each['年月'].isin(year_month_list))]
                plot_bar_quant_month(each_year_buy_sell_quant_df_new, title_name=year_quant + " 量化月度" + each_operation + "时序图",zs_nav_each=zs_nav_each)


    quant_detail(buy_sell_df,start_date,end_date)

    # 最新一周数据按管理人进行合并
    def group_by_manager(buy_sell_df,start_date,end_date):

        new_df = buy_sell_df.copy()
        new_df_week = new_df[(new_df['交易日期']>=start_date)&(new_df['交易日期']<=end_date)]

        # 宏观对冲_多策略
        new_df_hgdcl = new_df_week[new_df_week['大类标签']=='宏观对冲_多策略'].reset_index(drop=True)
        new_df_hgdcl_final = new_df_hgdcl.groupby(['真实管理人','资配二级','操作类型'])[['确认份额']].sum().reset_index()

        # 主观
        new_df_zg = new_df_week[new_df_week['大类标签']=='主观'].reset_index(drop=True)
        sql = "select rydm,jjdm from st_hedge.t_st_jjjl where ryzt=-1 and jjdm in {} AND m_opt_type<>'03'".format(
            tuple(new_df_zg['基金代码'].unique()))
        prv_funds_manager = get_df(sql, db='highuser')

        sql = "select rydm,ryxm as 私募基金经理 from st_hedge.t_st_sm_jlpf where rydm in {} AND m_opt_type<>'03'".format(
            tuple(prv_funds_manager['rydm'].unique().tolist()))
        ryxm = get_df(sql, db='highuser').drop_duplicates('rydm', keep='last').drop_duplicates('私募基金经理',keep='last')

        prv_funds_manager = pd.merge(prv_funds_manager, ryxm, how='left', on='rydm')
        prv_funds_manager = prv_funds_manager.groupby('jjdm')['私募基金经理'].apply(lambda x: x.str.cat(sep=',')).to_frame('私募基金经理')
        prv_funds_manager = prv_funds_manager.reset_index()
        prv_funds_manager.rename(columns={"jjdm":"基金代码"},inplace=True)

        new_df_zg = pd.merge(new_df_zg,prv_funds_manager,on='基金代码',how='left')
        new_df_zg.loc[new_df_zg[new_df_zg['私募基金经理'].isna()].index,'私募基金经理'] = '暂无'

        cl_jjjl = new_df_zg.copy()

        cl_jjjl = cl_jjjl[['基金代码', '真实管理人', '私募基金经理']]

        cl_jjjl = cl_jjjl[cl_jjjl['私募基金经理'] != '暂无']

        cl_jjjl = list(cl_jjjl.groupby('真实管理人'))

        temp_dfs = []

        for j in range(len(cl_jjjl)):
            temp_df = cl_jjjl[j][1].copy()
            temp_df = temp_df.drop_duplicates('基金代码')
            temp_df['私募基金经理'] = temp_df['私募基金经理'].str.split(',')
            result = pd.DataFrame(temp_df.explode('私募基金经理')['私募基金经理'].value_counts())
            temp_df.set_index('基金代码', inplace=True)
            for jj in temp_df.index:
                temp_df.loc[jj, '私募基金经理'] = \
                    (result.loc[temp_df.loc[jj]['私募基金经理']]).sort_values('私募基金经理').index[-1]

            temp_df = temp_df.reset_index()
            temp_dfs.append(temp_df)

        new_cl_jjjl = pd.concat(temp_dfs, axis=0)
        new_cl_jjjl = new_cl_jjjl.drop_duplicates().reset_index(drop=True)

        new_zg = new_df_zg.drop(columns='私募基金经理',axis=0)
        new_df_zg_2 = pd.merge(new_zg,new_cl_jjjl,on=['基金代码','真实管理人'],how='left')

        new_df_zg_final = new_df_zg_2.groupby(['真实管理人','私募基金经理','操作类型'])[['确认份额']].sum().reset_index()

        # 量化
        new_df_quant = new_df_week[new_df_week['大类标签']=='量化'].reset_index(drop=True)
        quant_strat = pd.read_excel(quant_strat_path)
        quant_strat = quant_strat[['基金代码', '二级策略']]
        quant_strat = quant_strat.drop_duplicates()
        new_df_quant = pd.merge(new_df_quant,quant_strat,on='基金代码',how='left')
        new_df_quant.loc[new_df_quant[new_df_quant['二级策略'].isna()].index,'二级策略'] = new_df_quant.loc[new_df_quant[new_df_quant['二级策略'].isna()].index,'资配二级']
        new_df_quant_final = new_df_quant.groupby(['真实管理人','二级策略','操作类型'])[['确认份额']].sum().reset_index()
        new_df_quant_final.rename(columns={"二级策略":"资配二级"},inplace=True)

        # 固定收益
        new_df_fixed_income = new_df_week[new_df_week['大类标签']=='固定收益'].reset_index(drop=True)
        new_df_fixed_income_final = new_df_fixed_income.groupby(['真实管理人','资配二级','操作类型'])[['确认份额']].sum().reset_index()

        new_df_all_final = pd.concat([new_df_quant_final,new_df_hgdcl_final,new_df_fixed_income_final,new_df_zg_final],axis='rows')
        new_df_all_final.rename(columns={"资配二级":"策略标签"},inplace=True)
        new_df_all_final = new_df_all_final[['真实管理人', '策略标签', '私募基金经理','操作类型', '确认份额']]

        new_df_all_buy = new_df_all_final[new_df_all_final['操作类型']=='buy']
        new_df_all_sell = new_df_all_final[new_df_all_final['操作类型']=='sell']

        new_df_all_net = pd.merge(new_df_all_buy,new_df_all_sell,on=['真实管理人', '策略标签', '私募基金经理'],how='outer')
        new_df_all_net['确认份额_x'] = new_df_all_net['确认份额_x'].fillna(0)
        new_df_all_net['确认份额_y'] = new_df_all_net['确认份额_y'].fillna(0)
        new_df_all_net['确认份额'] =  new_df_all_net['确认份额_x'] - new_df_all_net['确认份额_y']
        new_df_all_net_2 = new_df_all_net[['真实管理人', '策略标签', '私募基金经理','确认份额']]
        new_df_all_net_2['操作类型'] = 'net'

        new_df_all_net_2 = new_df_all_net_2[['真实管理人','策略标签','私募基金经理','操作类型','确认份额']]

        return new_df_all_net_2,new_df_all_buy,new_df_all_sell

    new_df_all_net,new_df_all_buy,new_df_all_sell = group_by_manager(buy_sell_df,start_date,end_date)

    return buy_sell_df_week_final,buy_sell_df_quant_week_final_copy,new_df_all_net,new_df_all_buy,new_df_all_sell

if __name__ == '__main__':
    data_path = r'D:\cyp\每周历史申赎数据分析\数据源\实际历史申赎.xlsx'
    quant_strat_path = r'D:\cyp\每周历史申赎数据分析\数据源\量化存量产品更新表（打标）.xlsx'
    start_date = 20240222
    end_date = 20240229
    buy_sell_df_week_final,buy_sell_df_quant_week_final,new_df_all_net,new_df_all_buy,new_df_all_sell=buy_sell_data_process(data_path=data_path,quant_strat_path=quant_strat_path,start_date=start_date,end_date=end_date)

    import xlwings as xw
    # Load the existing Excel file
    workbook = xw.Book(r'D:\cyp\每周历史申赎数据分析\python输出\每周申赎数据监控.xlsx')
    # Get the sheets you want to write to
    sheet_total = workbook.sheets['整体']
    sheet_quant = workbook.sheets['量化']
    sheet_glr = workbook.sheets['管理人']
    # Write buy_sell_df_week_final to '整体' sheet starting from A1
    sheet_total.range('A1').value = buy_sell_df_week_final
    # Write buy_sell_df_quant_week_final to '量化' sheet starting from A1
    sheet_quant.range('A1').value = buy_sell_df_quant_week_final
    #
    sheet_glr.range('A1').value = new_df_all_net
    sheet_glr.range('G1').value = new_df_all_buy
    sheet_glr.range('M1').value = new_df_all_sell
    # Save the workbook
    workbook.save()
    # Close the workbook
    workbook.close()
