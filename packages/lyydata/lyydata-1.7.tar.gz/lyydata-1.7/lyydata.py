import traceback
import os
import pandas as pd
import time
from pytdx.hq import TdxHq_API
import pandas as pd
from pandas import isnull
import lyywmdf
from lyylog import log
from datetime import datetime
from datetime import time as mk_time
from sqlalchemy import text
import lyytools
import lyycalendar
import lyybinary
import lyystkcode
import queue
from tqdm import tqdm

api_dict = {}
signal_id_dict = {"昨日换手": 777, "昨日回头波": 776}  # ,"涨停原因":888
column_mapping = {"时间": "datetime", "代码": "code", "名称": "name", "开盘": "open", "今开": "open", "收盘": "close", "最新价": "close", "最高": "high", "最低": "low", "涨跌幅": "change_rate", "涨跌额": "change_amount", "成交量": "vol", "成交额": "amount", "振幅": "amplitude", "换手率": "turnover_rate"}

tdx_path = r"D:\SOFT\_Stock\Tdx_202311"
df_all_cache_file = r"D:\UserData\resource\data\df_all_info.pkl"


df_all_info = pd.read_pickle(df_all_cache_file)
dict_all_code_guben = df_all_info.set_index("code")["流通股本亿"].to_dict()
import lyycfg


def calculate_minutes(dt1, dt2):
    # 创建一个新的日期范围，只包含周一到周五的9点31到15点
    # print("calculate_minutes",dt1,type(dt1),dt2,type(dt2))
    rng = pd.date_range(start=dt1, end=dt2, freq="T")
    rng = rng[rng.to_series().dt.dayofweek < 5]
    rng = rng[((rng.to_series().dt.time >= mk_time(9, 31)) & (rng.to_series().dt.time <= mk_time(11, 30))) | ((rng.to_series().dt.time >= mk_time(13, 1)) & (rng.to_series().dt.time <= mk_time(15, 0)))]
    return len(rng)


def update_min1_single(max_datetime, index, code, api, df_queue=None, debug=False):
    # 当前缓存df的最新时间是max_datetime，需要下载的分钟数是minutes.
    # print(f"-----------------{code}-------------------")
    if debug:
        print("maxdate in df=", max_datetime, type(max_datetime))
    if isnull(max_datetime):
        log(f"Skipping {code} because max_datetime is NaT,type=" + str(type(max_datetime)))
        return None
    # minutes = calculate_minutes(max_datetime, str(datetime.now()))

    minutes = lyycalendar.lyytc.计算相隔天数(max_datetime, lyycalendar.lyytc.最近完整收盘日(), debug=False) * 240 + 1
    if debug:
        print(api.ip, code, f"Code: {code}, 要下载的K线数量: {minutes}")
    df_single = lyywmdf.通达信下载原始分钟K线(api, code, 要下载的K线数量=minutes, ktype="1min", debug=debug)
    if len(df_single) < 1:
        print("in update_min1_single,", api.ip, code, "len(df_single)<1,return None")
        return None
    if debug:
        print("in update_min1_single, 获取成功df_single=\n", df_single)

    first_datetime = df_single["datetime"].iloc[0]
    if first_datetime == max_datetime:
        # print("first_datetime == max_datetime:")
        df_single = df_single[1:].copy()
        df_single["code"] = code
        if debug:
            print(df_single)
        if df_queue is not None:
            df_queue.put(df_single)
        else:
            print("df_queue is None，直接返回df_single，行数为", len(df_single))
            return df_single
    else:
        print("update_min1_single出错了，今天第一条不等于前天最后一条，对不上。请检查。\n", "firsttime=", first_datetime, ",max_datetime=", max_datetime)


def update_wmdf_realtime(wmdf, debug=False):

    pass


def update_wmdf_realtime_tdx(wmdf, debug=False):
    #        open  close   high    low           vol        amount    year  month   day  hour  minute          datetime    code value
    # 80.00  78.10  82.49  76.77  1.405300e+06  1.111376e+08  2024.0    1.0  24.0   9.0    31.0  2024-01-24 09:31  301577   NaN
    # 78.07  78.00  80.00  78.00  3.962000e+05  3.139237e+07  2024.0    1.0  24.0   9.0    32.0  2024-01-24 09:32  301577   NaN

    lyywmdf.通达信下载原始分钟K线(api, 股票数字代码, 要下载的K线数量, ktype="15min", debug=False)


def get_wmdf_min1_closed_tdx_fully(code_api_dict):
    dflist = []
    print("enter get_kline_min1_tdx_fully")
    # pbar = tqdm(len(self.code_api_dict), desc="get 1 min kline")
    pbar = tqdm(total=len(code_api_dict), desc="Get min1 kline")
    for code, api in code_api_dict.items():
        pbar.update(1)
        df_1min_single = lyywmdf.通达信下载原始分钟K线(api, code, 800, "1min", debug=False)
        df_1min_single["code"] = code
        dflist.append(df_1min_single)
    print("获取全部单个df成功")
    df1min_closed = pd.concat(dflist)
    df1min_closed.reset_index(drop=True, inplace=True)

    # df1min_closed.to_pickle(df1min_file)
    return df1min_closed


from concurrent.futures import ProcessPoolExecutor


def get_wmdf_min1_closed_tdx_fully_multi_process(code_api_dict):
    dflist = []
    print("enter get_kline_min1_tdx_fully")
    pbar = tqdm(total=len(code_api_dict), desc="Get min1 kline")

    # 创建一个进程池
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = []
        for code, api in code_api_dict.items():
            # 提交任务，并获取 Future 对象
            future = executor.submit(lyywmdf.通达信下载原始分钟K线, api, code, 800, "1min", False)
            futures.append(future)

        # 获取任务的返回结果
        for future in futures:
            try:
                df_1min_single = future.result()
                df_1min_single["code"] = code
                dflist.append(df_1min_single)
                pbar.update(1)
            except Exception as e:
                print("Error occurred: ", e)

    print("获取全部单个df成功")
    df1min_closed = pd.concat(dflist)
    df1min_closed.reset_index(drop=True, inplace=True)

    return df1min_closed


from concurrent.futures import ThreadPoolExecutor


def download_kline(api, code):
    df_1min_single = lyywmdf.通达信下载原始分钟K线(api, code, 800, "1min", debug=False)
    df_1min_single["code"] = code
    return df_1min_single


def get_wmdf_min1_closed_tdx_fully_multi_thread(code_api_dict):
    dflist = []
    print("enter get_kline_min1_tdx_fully")
    pbar = tqdm(total=len(code_api_dict), desc="Get min1 kline")

    # 创建一个线程池
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for code, api in code_api_dict.items():
            # 提交任务，并获取 Future 对象
            future = executor.submit(download_kline, api, code)
            futures.append(future)

        # 获取任务的返回结果
        for future in futures:
            try:
                df_1min_single = future.result()
                dflist.append(df_1min_single)
                pbar.update(1)
            except Exception as e:
                print("Error occurred: ", e)

    print("获取全部单个df成功")
    df1min_closed = pd.concat(dflist)
    df1min_closed.reset_index(drop=True, inplace=True)

    return df1min_closed


def update_wmdf_closed(wmdf_closed, code_api_dict, debug=False):
    """
    根据last_date_dict计算wmdf补充的日期，遍历代码，获取需要的数据，最后一次性合并。
    能够补到最新，不能保证是完整收盘。需要自选处理。比如：df_closed = wmdf[wmdf["dayint"] <= last_closed_date_int]
    """
    df_to_concat_list = [wmdf_closed]
    pbar = tqdm(range(100), desc="update wmdf closed")
    grouped = wmdf_closed.groupby("code").agg({"dayint": "max"})
    last_date_dict = grouped["dayint"].to_dict()
    # 遍历所有代码，获取单个wmdf，添加到df_list中，以供后续合并。
    if debug:
        print("enter fun: lyydata.update_wmdf_closed")
    if code_api_dict is None:
        if debug:
            print("code_api_dict is None, return")
        return
    for index, (code, api) in enumerate(code_api_dict.items()):
        if index % 53 == 0:
            pbar.update(1)
        db_last_date_int, 相差天数, kline_n = lyywmdf.calc_lastdate_kline_number(code, last_date_dict, debug=debug)
        if 相差天数 == 0:
            if debug:
                print("新", end="")
            continue
        try:
            if debug:
                print("code/type=", code, type(code), "server_ip=", api.ip, ",dblast_date/type=", db_last_date_int, type(db_last_date_int), "相差天数=", 相差天数, "kline_n=", kline_n)
            if code is None or api is None or kline_n is None or db_last_date_int is None:
                print("code/api/kline_n/db_last_date_int is None, continue")
                continue

            df_single = get_and_format_wmdf_for_single_code(code, api, db_last_date_int, kline_n, debug=False).copy()
            if debug:
                print(df_single, "df_single")
        except Exception as e:
            traceback.print_exc()
            log(code + api.ip + str(db_last_date_int) + str(kline_n) + str(e))
            continue
        if debug:
            if debug:
                print("finish codd=", code)
        if len(df_single) > 0:
            if debug:
                print("add df_single to df list")
            df_to_concat_list.append(df_single)
            if debug:
                print("finish add df_single to df list")
        else:  # raise Exception("df_single is empty")
            if debug:
                log(f"{code}@{api.ip} df_single is empty")
        # if debug: print("try to rename")
        # df_single=df_single.rename(columns={'day':  'dayint'})
        # df_single['day'] = df_single['dayint'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:8])
    wmdf_closed = pd.concat(df_to_concat_list)
    if debug:
        print("wmdf_closed\n", wmdf_closed)
    pbar.close()
    if debug:
        print("return wmdf_closed")
    return wmdf_closed


import multiprocessing


def update_wmdf_closed_multi(wmdf_closed, code_api_dict, debug=False):
    def process_code(code, api, last_date_dict, debug):
        db_last_date_int, 相差天数, kline_n = lyywmdf.calc_lastdate_kline_number(code, last_date_dict, debug=debug)
        if 相差天数 == 0:
            if debug:
                print("新", end="")
            return None
        try:
            if debug:
                print("code/type=", code, type(code), "server_ip=", api.ip, ",dblast_date/type=", db_last_date_int, type(db_last_date_int), "相差天数=", 相差天数, "kline_n=", kline_n)
            if debug:
                print(code, api.ip, kline_n, db_last_date_int)
            df_single = get_and_format_wmdf_for_single_code(code, api, db_last_date_int, kline_n, debug=debug).copy()
            if debug:
                print(df_single, "df_single")
            return df_single
        except Exception as e:
            traceback.print_exc()
            log(code + api.ip + str(db_last_date_int) + str(kline_n) + str(e))
            return None

    if code_api_dict is None:
        if debug:
            print("code_api_dict is None, return")
        return
    grouped = wmdf_closed.groupby("code").agg({"dayint": "max"})
    last_date_dict = grouped["dayint"].to_dict()
    p = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = []
    for code, api in code_api_dict.items():
        result = p.apply_async(process_code, args=(code, api, last_date_dict, debug))
        results.append(result)

    p.close()
    p.join()

    df_to_concat_list = [wmdf_closed]
    for result in results:
        df_single = result.get()
        if df_single is not None:
            df_to_concat_list.append(df_single)

    wmdf_closed = pd.concat(df_to_concat_list)
    return wmdf_closed


@lyytools.get_time
def update_wmdf_realtime(wmdf, debug=False):
    """
    Index(['序号', 'code', 'name', 'close', 'change_rate', 'change_amount', 'vol',
       'amount', 'amplitude', 'high', 'low', 'open', '昨收', '量比',
       'turnover_rate', '市盈率-动态', '市净率', '总市值', '流通市值', '涨速', '5分钟涨跌',
       '60日涨跌幅', '年初至今涨跌幅', '流通股本亿', '流通市值亿'],

       "['day', 'volume', 'up', 'tenhigh', 'chonggao', 'huitoubo', 'notfull', 'dayint'] not in index"

    """
    if wmdf is None:
        wmdf = pd.read_pickle("wmdf_closed.pkl")
    # 获取新数据
    df_em = lyystkcode.get_all_codes_dict_em()
    df_new = format_df_em(df_em)

    if "id" in wmdf.columns:
        del wmdf["id"]
    df_new.reset_index(inplace=True, drop=True)
    wmdf.reset_index(inplace=True, drop=True)
    # 合并 df_all 和 df_new
    dfall = pd.merge(wmdf, df_new, on=["code", "day"], how="left", suffixes=("", "_new"))
    # 如果当前时间早于 10 点，更新 'chonggao' 和 'tenhigh' 列

    if lyycalendar.lyytc.if_in_notfull_time(datetime.now()):
        dfall.loc[dfall["chonggao_new"].notna(), "chonggao"] = df_new["chonggao_new"]
        dfall.loc[dfall["tenhigh_new"].notna(), "tenhigh"] = df_new["tenhigh_new"]

    if debug:
        print(wmdf.tail(3))
    # dfall.set_index(['code', 'day'], inplace=True)
    # dfall = pd.concat([wmdf, df_new], keys=["code", "day"])
    if debug:
        print(dfall)
    print(".", end="")
    dfall.to_pickle("wmdf.pkl")
    time.sleep(5)
    return dfall


def format_df_em(df_all_info):
    df_all_info = df_all_info.rename(columns=column_mapping)
    df_all_info["dayint"] = lyycalendar.lyytc.东财最后数据归属日()
    df_all_info["volume"] = df_all_info["vol"]
    now_hour = datetime.now().hour

    # 计算缺少的字段： 早上10点之后，不计算chonggao和tenhigh字段。
    if now_hour < 100:
        df_all_info["chonggao"] = (df_all_info["high"] / df_all_info["昨收"]) * 100 - 100
        df_all_info["tenhigh"] = df_all_info["high"]
    else:
        df_all_info["chonggao"] = None
        df_all_info["tenhigh"] = None

    # 补充其它缺少的字段
    df_all_info["up"] = df_all_info["close"] - df_all_info["昨收"]
    df_all_info["huitoubo"] = (df_all_info["high"] / df_all_info["close"]) * 100 - 100
    df_all_info["notfull"] = now_hour
    df_all_info["day"] = df_all_info["dayint"].apply(lambda x: "-".join([str(x)[:4], str(x)[4:6], str(x)[6:8]]))
    # 提取需要的字段
    columns = ["code", "day", "open", "high", "close", "low", "volume", "up", "tenhigh", "chonggao", "huitoubo", "notfull", "dayint"]
    df_new = df_all_info[columns]
    return df_new


def update_mysql_from_wmdf(wmdf, engine=None, debug=False):
    debug = True
    if debug:
        print("enter update_mysql_from_wmdf")
    table_name = "stock_wmdf_test"
    # 从 MySQL 中读取数据

    if engine is None:

        if debug:
            print("engine is None, try to get from lyycfg")
        lyycfg.cfg.get_engine_conn()
        engine = lyycfg.cfg.engine
    if debug:
        print(f"reading max dayint from table:{table_name}")
    mysql_df_max_dayint = pd.read_sql(f"SELECT code, MAX(dayint) as max_dayint FROM {table_name} GROUP BY code", engine)

    if debug:
        print("# 获取每个 code 的 dayint 的最大值")

    max_dayint_dict = mysql_df_max_dayint.set_index("code")["max_dayint"].to_dict()
    if debug:
        print(max_dayint_dict)
    # 对 df 进行分组，然后筛选出 dayint 大于对应 code 的最大值的行

    def filter_rows(group):
        code = group.name
        return group[group["dayint"] > max_dayint_dict.get(code, -1)]

    if debug:
        print("筛选出 dayint 大于对应 code 的最大值的行")

    df_filtered = wmdf.groupby("code").apply(filter_rows)
    print("df_filtered\n")
    print(df_filtered)
    ungrouped_df = df_filtered.reset_index(drop=True)

    if debug:
        print("筛选成功，# 将结果写入到 MySQL 中")
    sql_columns = ["code", "day", "open", "high", "close", "low", "volume", "up", "tenhigh", "chonggao", "huitoubo", "notfull", "dayint"]
    df_towrite = ungrouped_df[sql_columns]
    if debug:
        print(df_towrite)
    df_towrite.to_sql(f"{table_name}", engine, if_exists="append", index=False)
    print("写入结束")


def update_cg_series(df, debug=False):
    if len(df) < 10000:
        print("dataframe<1000 line，check it")
    df_grouped = df.groupby("code")

    for code, group_rows in df_grouped:
        if debug:
            print("enter for code,group_rows in df_grouped")
        market = lyystkcode.get_market(code)
        tdx_signal_file = os.path.join(tdx_path, rf"T0002\signals\signals_user_{999}", f"{market}_{code}.dat")
        db_last_date_int = lyybinary.get_lastdate_tdx_sinal(tdx_signal_file)
        if debug:
            print(f"try to filter: group_rows['dayint'] > {db_last_date_int}")
        filtered_rows = group_rows[group_rows["dayint"] > db_last_date_int]
        if debug:
            print(filtered_rows)
        data_dict = filtered_rows.set_index("dayint")["chonggao"].to_dict()

        if debug:
            print(tdx_signal_file, db_last_date_int, "db_last_date_int type=", type(db_last_date_int))
        lyybinary.add_data_if_new_than_local(tdx_signal_file, data_dict, db_last_date_int, debug=debug)
        if debug:
            print("写入文件成功")


def update_signal_txt(df, debug=False):
    if debug:
        print("enter update_signal_txt, input para len=", len(df))
    # grouped_df = df.groupby('code').agg({'dayint':'max'}).reset_index(drop=False)
    # chonggao_dict = grouped_df['chonggao'].apply(lambda x: x.iloc[-1]).to_dict()
    # huitoubo_dict = grouped_df['huitoubo'].apply(lambda x: x.iloc[-1]).to_dict()
    if debug:
        print("get the row with max dayint")
    grouped_df = df.groupby("code").agg({"volume": "last", "huitoubo": "last", "dayint": "last"}).reset_index(drop=False)

    # print(grouped_df)
    # time.sleep(3333)
    # grouped_df = grouped_df.tail(1)
    # idx = df.groupby('code').tail(1)
    # print("idx=",idx)
    # grouped_df = df.loc[idx]

    df_reason = get_ztreason_df()
    if debug:
        print("apply code 666 to grouped_df")

    if debug:
        print(grouped_df, "----------------here is grouped df---------------")
    data_list = []
    pbar = tqdm(range(len(grouped_df)), desc="update_chonggao_huitoubo_for_signal_txt")
    for row in grouped_df.itertuples():
        pbar.update(1)
        cg_dict = {}
        ht_dict = {}
        code = row.code
        cg_dict["market"] = lyystkcode.get_market(code)
        cg_dict["code"] = row.code
        cg_dict["signal_id"] = 666
        cg_dict["text"] = ""
        cg_dict["number"] = (row.volume / 100) / dict_all_code_guben.get(code, 1)

        # print(dict_all_code_guben,"\n","row=",row,"\ncgdict=",cg_dict)

        ht_dict["market"] = lyystkcode.get_market(code)
        ht_dict["code"] = row.code
        ht_dict["signal_id"] = 665
        ht_dict["text"] = ""
        ht_dict["number"] = row.huitoubo
        # print(row.huitoubo,type(row.huitoubo))
        data_list.append(cg_dict)
        data_list.append(ht_dict)
        time.sleep(0.01)
        # print(cg_dict)

    if debug:
        print("concat df_chonggao,df_huitoubo,df_reason")
    columns = ["market", "code", "signal_id", "text", "number"]
    dtype = {"market": str, "code": str, "signal_id": int, "text": str, "number": float}
    df_merged = pd.concat([pd.DataFrame(data_list), df_reason], ignore_index=True).sort_values("signal_id", ascending=True)  # ignore_index=True, verify_integrity=False

    if debug:
        print("contact finished. Try to filter no gbk code")
    # df_merged = df_merged.dropna(subset=['code'])
    df_merged.reset_index(inplace=True, drop=True)
    # bool_series = df_merged['code'] != "0.000"
    # df_merged = df_merged[bool_series].dropna(subset=['code'])
    df_merged = df_merged.apply(lambda x: x.apply(lambda y: y.encode("gbk", errors="ignore").decode("gbk") if isinstance(y, str) else y))  # '算力+数字虚拟人+互联网营销：1、浙文投董事的务能力。虚拟人销已经实现与ch\xada\xadt\xadG\xadPT的结合及落地。'
    path = r"D:\Soft\_Stock\Tdx_202311\T0002\signals\extern_user.txt"
    df_merged.to_csv(path, index=False, header=False, sep="|", encoding="gbk")
    if debug:
        print("执行完成！df_merged=\n", df_merged)
    return df_merged


def get_ztreason_df(debug=False):
    # 从数据库中读取股票代码
    lyycfg.cfg.get_engine_conn()
    query = text("SELECT * as count FROM stock_jiucai WHERE  date > 20231001")
    query = """SELECT * FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) AS rn FROM stock_jiucai WHERE date >= DATE_SUB(CURDATE(), INTERVAL 20 DAY)) AS subquery WHERE rn = 1 """
    result = pd.read_sql(query, lyycfg.cfg.engine)
    # 获取数量
    result["code"] = result["code"].apply(lambda x: str(x).zfill(6))
    result["signal_id"] = 888
    result["number"] = 0.000
    result["text"] = result.apply(lambda row: str(row["plate_name"]) + "：" + str(row["reason"]).replace("\n", ""), axis=1)
    result["market"] = result.code.apply(lambda x: lyystkcode.get_market(x))
    return_df = result[["market", "code", "signal_id", "text", "number"]]
    if debug:
        print(return_df)
    return return_df


def 获取昨换手和回头波(item, debug=False):
    print("#查询计算相应股票代码对应的数据")
    code, server_ip = item
    api = lyywmdf.initialize_api(server_ip)
    code = str(code).zfill(6)
    market = lyystkcode.get_market(code)
    last_trade_day = lyycalendar.lyytc.最近完整收盘日()
    print("last_trade_day=", "------------------", last_trade_day)
    last_trade_day_str = str(last_trade_day)[:4] + "-" + str(last_trade_day)[4:6] + "-" + str(last_trade_day)[6:8]
    print("last_trade_day=", last_trade_day, 9, market, code)
    # df01 = api.to_df(api.get_security_bars(9, 0, "000001", 0, 1))
    # print("df01=", df01)
    K_number = 2 if datetime.now().hour < 9 else 1
    df = api.to_df(api.get_security_bars(9, market, code, 0, K_number))

    # from mootdx.quotes import Quotes

    # client = Quotes.factory(market='std')
    # df = client.bars(symbol=code, frequency=9, offset=10)
    print("dataframe=", df)
    data_dict = df.iloc[0].to_dict()

    print("r=", data_dict)

    # turn_dict = lyystkcode.get_bjs_liutongguben_dict()

    # 流通股本 = float(turn_dict[code])
    vol = data_dict["vol"] / pow(10, 6)

    # 流通市值 = round(流通股本 * data_dict['close'], 2)
    # print("流通股本=", 流通股本, "流通市值=", 流通市值)
    流通股本 = dict_all_code_guben[str(code)]
    换手 = round(vol / 流通股本, 2)

    turn_list = [market, code, 666, 换手]

    close = data_dict["close"]
    print("close=", close)
    amount = data_dict["amount"]

    high = data_dict["high"]
    print("high=", high)

    huitoubo = (close - high) / high
    print("huitoubo=", huitoubo)
    huitoubo_list = [market, code, 665, round(huitoubo, 2)]
    debug = True
    if debug:
        print("turn_list=", turn_list, ",huitoubo_list=", huitoubo_list)
    return turn_list, huitoubo_list


def read_data_from_sql(table_name="stock_wmdf_test", conn=None, debug=True):
    if conn is None:
        print("conn is None, try to connect")
        lyycfg.cfg.get_engine_conn()

    # 构建SQL查询语句
    sql_query = f"SELECT * FROM {table_name} "
    # 通过数据库连接执行SQL查询，并将结果存储到DataFrame
    df = pd.read_sql_query(sql_query, lyycfg.cfg.conn)
    return df


# todelete
def get_wmdf_and_last_date_from_cache(cache_file, q=None, debug=False):
    """
    从缓存加载最初的wmdf
    """
    if debug:
        print("enter datacenter")
    old_df = get_data_from_cache_or_func(cache_file, 3600 * 8, None, debug=True)
    old_df = pd.read_pickle(cache_file)
    if debug:
        print("try to ogg in get wmdf last date")
    grouped = old_df.groupby("code").agg({"dayint": "max"})
    last_date_dict = grouped["dayint"].to_dict()
    print("get last_date_dict, len=", len(last_date_dict))
    if q is not None:
        q.put((old_df, last_date_dict))
    else:
        return old_df, last_date_dict


def get_data_from_cache_or_func(cache_file_path, expiry_duration=3600 * 24, next_func=None, debug=False):
    # 检查文件是否存在,expiry_duration=3600意味着1小时。
    print("cache file=" + cache_file_path)
    if os.path.isfile(cache_file_path):
        if debug:
            print("in get_data_from_cache_or_func, file exists, check expiry duration. file path=" + os.getcwd() + "\\" + (cache_file_path))
        # 获取文件的最后修改时间
        last_modified_time = os.path.getmtime(cache_file_path)
        # 计算当前时间与最后修改时间的差值（秒）
        current_time = time.time()
        time_difference = current_time - last_modified_time
        if time_difference < expiry_duration:
            if debug:
                print(f"缓存{cache_file_path}在有效期内，直接读取")
            df = pd.read_pickle(cache_file_path)
            if debug:
                print(f"{cache_file_path} not expired, return it, =\n", df)
            return df
        else:
            print(f"缓存{cache_file_path}超过有效期")
    else:
        print(f"文cache_file_path:{cache_file_path}件不存在")

    # all else:
    if next_func is not None:
        return next_func()
    else:
        return None


def df_add_notfull(df, haveto_date, debug=False):
    """
    添加一列notfull。先统一设置为15，然后如果下载到了今天的数据，今天却没收盘，则把今天（也就是最大值这天）的notfull为循环最初的小时。
    """
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    # 先将'day'列转化为整数,方便匹配haveto_date
    if debug:
        print("in df_add_notfull,df=\n", df)
    df["dayint"] = df["day"].apply(lambda x: int(str(x).replace("-", "")))
    df["notfull"] = 15
    # print("dfmax == today_date_int=<"+str(df["day"].max == today_date_int)+">", today_time_hour < 15, df["day"].max == today_date_int and today_time_hour < 15)
    if df["dayint"].max() == today_date_int and now.hour < 15:
        if debug:
            print("今天 没收盘，要重点标记一下。today_time_hour=", now.hour, "today_date_int=", today_date_int)
        df.loc[df["dayint"] == today_date_int, "notfull"] = now.hour
    else:
        if debug:
            print("in df_add_notfull, 完美收盘无需牵挂", end="")
    return df


def get_and_format_wmdf_for_single_code(code, api, db_last_date_int, kline_n, debug=False):
    """
    获取单个股票差额的dataframe
    """

    if debug:
        print("get_and_format_wmdf_for_single_code：", code, api, db_last_date_int, kline_n)
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    if debug:
        print("# 初始化api连接,", code)
    # except Exception as e:
    # print("process_code_entry first error", e)
    if debug:
        print("# 获得某个代码的wmdf")

    try:
        wmdf = lyywmdf.wmdf(api, code, kline_n, debug=debug)

    except Exception as e:
        traceback.print_exc()
    if debug:
        print(wmdf.tail(1))
    wmdf["code"] = code
    if debug:
        print(f"in function get_and_format_wmdf_for_single_code,{code} wmdf = \n", wmdf)
    wmdf = df_add_notfull(wmdf, today_date_int)
    wmdf = wmdf.drop(wmdf.index[0]).reset_index(drop=True)
    if debug:
        print(wmdf.columns)
    if debug:
        print(wmdf.tail(1))
    filtered_df = wmdf[wmdf["dayint"] > db_last_date_int]
    return filtered_df

    # except Exception as e:
    #     log("process_code_entry error" + str(e))
    #     return pd.DataFrame()
    # finally:
    #     pass


def get_fenshi(api):
    pass


def get_test_df_from_wmdf_closed():
    """
    从数据目录读取日线pickle文件，第一个返回值为部分600开头股票的日线数据，第二个返回值为所有股票的日线数据。
    """
    data_dir = r"D:/UserData/resource/data"
    if not os.path.isfile(data_dir + "/df600.pkl"):
        dfall = pd.read_pickle(data_dir + "/wmdf_closed.pkl")
        df = dfall[dfall["code"].str.startswith("600")].copy()
        df.to_pickle(data_dir + "/df600.pkl")
    else:
        dfall = pd.read_pickle(data_dir + "/wmdf_closed.pkl")
        df = pd.read_pickle(data_dir + "/df600.pkl")
    return df, dfall


def get_sample_data():
    """
    获取样本数据
    """
    df = pd.read_pickle(r"D:\UserData\resource\data\df_all_info.pkl")
    return df


def get_minute_data():
    """
    获取分钟线数据
    """
    df = pd.read_pickle(r"D:\UserData\resource\data\wmdf_closed_1min.pkl")
    return df


if __name__ == "__main__":
    import lyymysql
    import lyystkcode

    lyycfg.cfg.get_engine_conn()
    instance_lyymysql = lyymysql.lyymysql_class(lyycfg.cfg.engine)
    df = lyystkcode.get_all_codes_dict_em()
    stkcode_list = df["代码"].to_list()
    if len(stkcode_list) < 5000:
        print("stkcode_list<5000,check it")
    server_list = lyywmdf.perfact_new_fast_server_list(nextfuntion=instance_lyymysql.get_tdx_server_list)
    if len(server_list) < 10:
        print("server_list<10,check it")
    df_old, last_date_dict = get_wmdf_and_last_date()
    df = update_wmdf("", stkcode_list, server_list, last_date_dict)
    print(df)
    print("start lyydata")
