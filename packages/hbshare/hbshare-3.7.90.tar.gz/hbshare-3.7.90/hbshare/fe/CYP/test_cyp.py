import pandas as pd
from hbshare.fe.XZ import db_engine
localdb=db_engine.PrvFunDB().engine

sql = "select INDEX_NAME AS 指数名称, INDEX_SYMBOL AS 指数代码, TRADE_DATE AS 交易日期, INDEX_POINT AS 指数点位, 涨幅 from fe_temp_data.fund_index \
       where INDEX_NAME = '主动股票型基金指数' and TRADE_DATE >= '20130101' order by TRADE_DATE"

gmzdgp = pd.read_sql(sql,con=localdb)
gmzdgp = gmzdgp[['交易日期','涨幅']]
gmzdgp.rename(columns={"涨幅":"HM_gmzdgp"},inplace=True)
gmzdgp.set_index('交易日期',inplace=True)
gmzdgp = (gmzdgp / 100 + 1).cumprod()



