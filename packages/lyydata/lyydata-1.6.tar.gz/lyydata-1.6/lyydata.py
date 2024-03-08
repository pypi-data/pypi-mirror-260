import traceback
import os
import pandas as pd
import time
from pytdx.hq import TdxHq_API
import pandas as pd
import lyywmdf
from lyylog import log
from datetime import datetime
from sqlalchemy import text
import lyytools
import lyycalendar
from tqdm import tqdm
import lyybinary
import lyystkcode
import queue
from tqdm import tqdm

ins_lyycalendar = lyycalendar.lyytc
api_dict = {}
signal_id_dict = {"昨日换手": 777, "昨日回头波": 776}  # ,"涨停原因":888
column_mapping = {"时间": "datetime", "代码": "code", "名称": "name", "开盘": "open", "今开": "open", "收盘": "close", "最新价": "close", "最高": "high", "最低": "low", "涨跌幅": "change_rate", "涨跌额": "change_amount", "成交量": "vol", "成交额": "amount", "振幅": "amplitude", "换手率": "turnover_rate"}

df_all_cache_file = r"D:\UserData\resource\data\df_all_info.pkl"
now = datetime.now()


if now.hour > 15:
    df_all_info = lyystkcode.get_all_codes_dict_em().rename(columns=column_mapping)
    df_all_info.to_pickle(df_all_cache_file)
else:
    print("非工作时间，从缓存加载东财股本字典")
    df_all_info = pd.read_pickle(df_all_cache_file)
dict_all_code_guben = df_all_info.set_index("code")["流通股本亿"].to_dict()


def format_df_em(df_all_info):
    df_all_info = df_all_info.rename(columns=column_mapping)
    df_all_info["dayint"] = ins_lyycalendar.东财最后数据归属日()
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


def update_mysql_from_wmdf(df, engine=None, debug=False):
    debug = True
    if debug:
        print("enter update_mysql_from_wmdf")
    table_name = "stock_wmdf_test"
    # 从 MySQL 中读取数据
    if engine is None:
        import lyycfg

        if debug:
            print("engine is None, try to get from lyycfg")
        engine, conn, _ = lyycfg.con_aliyun_sqlalchemy()
    if debug:
        print(f"reading table from table:{table_name}")
    df_mysql = pd.read_sql(f"SELECT * FROM {table_name}", engine)

    if debug:
        print("# 获取每个 code 的 dayint 的最大值")

    max_dayint_dict = df_mysql.groupby("code")["dayint"].max().to_dict()
    if debug:
        print(max_dayint_dict)
    # 对 df 进行分组，然后筛选出 dayint 大于对应 code 的最大值的行

    def filter_rows(group):
        code = group.name
        return group[group["dayint"] > max_dayint_dict.get(code, -1)]

    if debug:
        print("筛选出 dayint 大于对应 code 的最大值的行")
    df_filtered = df.groupby("code").apply(filter_rows)
    ungrouped_df = df_filtered.reset_index(drop=True)

    if debug:
        print("筛选成功，# 将结果写入到 MySQL 中")
    sql_columns = ["code", "day", "open", "high", "close", "low", "volume", "up", "tenhigh", "chonggao", "huitoubo", "notfull", "dayint"]
    df_towrite = ungrouped_df[sql_columns]
    if debug:
        print(df_towrite)
    df_towrite.to_sql(f"{table_name}", engine, if_exists="append", index=False)


def update_cg_series(df, debug=False):
    if len(df) < 10000:
        print("dataframe<1000 line，check it")
    debug = True
    df_grouped = df.groupby("code")

    for code, group_rows in df_grouped:
        if debug:
            print("enter for code,group_rows in df_grouped")
        market = lyystkcode.get_market(code)
        tdx_signal_file = os.path.join(r"D:\SOFT\_Stock\Tdx_202311", rf"T0002\signals\signals_user_{999}", f"{market}_{code}.dat")
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

    df_reason = get_ztreason_df()
    if debug:
        print("apply code 666 to grouped_df")

    if debug:
        print(grouped_df, "----------------here is grouped df---------------")
    data_list = []

    pbar = tqdm(range(len(grouped_df)), desc="update_cg_huitoubo", bar_format="{l_bar}{bar} [{nfmt}]")
    for row in tqdm(grouped_df.itertuples()):
        cg_dict = {}
        ht_dict = {}
        code = row.code
        cg_dict["market"] = lyystkcode.get_market(code)
        cg_dict["code"] = row.code
        cg_dict["signal_id"] = 666
        cg_dict["text"] = ""
        cg_dict["number"] = (row.volume / 100) / dict_all_code_guben.get(code, 1)
        ht_dict["market"] = lyystkcode.get_market(code)
        ht_dict["code"] = row.code
        ht_dict["signal_id"] = 665
        ht_dict["text"] = ""
        ht_dict["number"] = row.huitoubo
        data_list.append(cg_dict)
        data_list.append(ht_dict)
        pbar.update(1)

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
    import lyycfg

    engine, conn, session = lyycfg.con_aliyun_sqlalchemy()
    query = text("SELECT * as count FROM stock_jiucai WHERE  date > 20231001")
    query = """SELECT * FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) AS rn FROM stock_jiucai WHERE date >= DATE_SUB(CURDATE(), INTERVAL 20 DAY)) AS subquery WHERE rn = 1 """
    result = pd.read_sql(query, engine)
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
    last_trade_day = ins_lyycalendar.最近完整收盘日(0)
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


def update_wmdf(wmdf, stkcode_list, server_list, last_date_dict, debug=False):
    """
    根据last_date_dict计算wmdf补充的日期，遍历代码，获取需要的数据，最后一次性合并。
    """
    df_to_concat_list = [wmdf]
    code_server_dict = lyytools.assign(stkcode_list, server_list)
    if debug:
        print("code_server_dict=", code_server_dict)
    pbar = tqdm(range(100))

    # 遍历所有代码，获取单个wmdf，添加到df_list中，以供后续合并。
    for index, (code, server_ip) in enumerate(code_server_dict.items()):
        # print("code=", code, type(code))
        # print(last_date_dict.keys())
        # for i in (last_date_dict.keys()):
        #     print(i, type(i))
        db_last_date_int, 相差天数, kline_n = lyywmdf.calc_lastdate_kline_number(code, last_date_dict)
        if 相差天数 == 0:
            if debug:
                print("相差天数为0，已经最新了。所以 直接跳过返回。")
            continue

        try:
            if debug:
                print("code=", code, ",server_ip=", server_ip, ",last_date=", db_last_date_int, "相差天数=", 相差天数, "kline_n=", kline_n)
            # (code, server_ip, kline_n, db_last_date_int, debug=False):
            df_single = get_and_format_wmdf_for_single_code(code, server_ip, db_last_date_int, kline_n, debug=False)
            if debug:
                print(df_single, "df_single")
        except Exception as e:
            traceback.print_exc()
        if debug:
            print("finish codd=", code)
        if len(df_single) > 0:
            df_single = df_single.rename(columns={"day": "dayint"})
            df_single["day"] = df_single["dayint"].apply(lambda x: str(x)[0:4] + "-" + str(x)[4:6] + "-" + str(x)[6:8])
            df_to_concat_list.append(df_single)
        else:  # raise Exception("df_single is empty")
            if debug:
                log(f"{code}@{server_ip} df_single is empty")
        if index % 53 == 0:
            pbar.update(1)

    wmdf = pd.concat(df_to_concat_list)
    if debug:
        print(wmdf)
    pbar.close()

    return wmdf


def read_data_from_sql(table_name="stock_wmdf_test", conn=None, debug=True):
    if conn is None:
        print("conn is None, try to connect")
        from sqlalchemy import create_engine, text
        import lyycfg

        engine = create_engine(f"mysql+pymysql://{lyycfg.mysql_username}:{lyycfg.mysql_password}@rm-7xvcw05tn97onu88s7o.mysql.rds.aliyuncs.com:3306/fpdb?charset=utf8")
        conn = engine.connect()
    # 构建SQL查询语句
    sql_query = f"SELECT * FROM {table_name} "
    # 通过数据库连接执行SQL查询，并将结果存储到DataFrame
    df = pd.read_sql_query(sql_query, conn)
    return df


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


def get_data_from_cache_or_func(cache_file_path, expiry_duration, next_func=None, debug=False):
    # 检查文件是否存在,expiry_duration=3600意味着1小时。
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
                print("缓存在有效期内，直接读取")
            df = pd.read_pickle(cache_file_path)
            if debug:
                print(f"{cache_file_path} not expired, return it, =\n", df)
            return df
        else:
            print("缓存超过有效期")
    else:
        print("文cache_file_path件不存在")
        raise Exception("cache_file_path文件不存在")
        return
    # all else:
    if next_func is not None:
        return next_func()
    else:
        return None


def df_add_notfull(df, haveto_date):
    """
    添加一列notfull。先统一设置为15，然后如果下载到了今天的数据，今天却没收盘，则把今天（也就是最大值这天）的notfull为循环最初的小时。
    """
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    # 先将'day'列转化为整数,方便匹配haveto_date
    df.loc[:, "day"] = df["day"].apply(lambda x: int(str(x).replace("-", "")))
    df["notfull"] = 15
    # print("dfmax == today_date_int=<"+str(df["day"].max == today_date_int)+">", today_time_hour < 15, df["day"].max == today_date_int and today_time_hour < 15)
    if df["day"].max() == today_date_int and now.hour < 15:
        print("今天 没收盘，要重点标记一下。today_time_hour=", now.hour, "today_date_int=", today_date_int)
        df.loc[df["day"] == today_date_int, "notfull"] = now.hour
    else:
        print("完美收盘无需牵挂", end="")
    return df


def get_and_format_wmdf_for_single_code(code, server_ip, db_last_date_int, kline_n, debug=False):
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    if debug:
        print("# 初始化api连接,", code)
    # except Exception as e:
    # print("process_code_entry first error", e)
    global api_dict
    if server_ip not in api_dict.keys():
        if debug:
            print("server_ip not in api_dict, connect it")
        api = TdxHq_API(multithread=False, heartbeat=False, auto_retry=True)
        api_dict[server_ip] = api
        api_dict[server_ip].connect(server_ip, 7709)
        # api = initialize_api(server_ip)
    else:
        api = api_dict[server_ip]
        if debug:
            print("tdx api already in dict.")
    # api = api_dict[server_ip]
    if debug:
        print("initserverip", server_ip)
    if debug:
        print("# 获得某个代码的wmdf")
    try:
        wmdf = lyywmdf.wmdf(api, code, kline_n, server_ip=server_ip, debug=debug)
    except Exception as e:
        traceback.print_exc()
    if wmdf is None:
        raise Exception("wmdf is None")
    wmdf["code"] = code
    wmdf = df_add_notfull(wmdf, today_date_int)
    wmdf = wmdf.drop(wmdf.index[0]).reset_index(drop=True)
    print(wmdf.columns)
    print(wmdf.tail(1))

    filtered_df = wmdf[wmdf["day"] > db_last_date_int].copy()

    return filtered_df

    # except Exception as e:
    #     log("process_code_entry error" + str(e))
    #     return pd.DataFrame()
    # finally:
    #     pass


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


if __name__ == "__main__":
    import lyymysql
    import lyycfg
    import lyystkcode

    engine, conn, _ = lyycfg.con_aliyun_sqlalchemy()
    instance_lyymysql = lyymysql.lyymysql_class(engine)
    df = lyystkcode.get_all_codes_dict_em()
    stkcode_list = df["代码"].to_list()
    if len(stkcode_list) < 5000:
        print("stkcode_list<5000,check it")
    server_list = lyywmdf.perfact_new_fast_server_list(nextfuntion=instance_lyymysql.get_tdx_server_list)
    if len(server_list) < 10:
        print("server_list<10,check it")
    df = update_wmdf("", stkcode_list, server_list, last_date_dict)
    print(df)
    print("start lyydata")
