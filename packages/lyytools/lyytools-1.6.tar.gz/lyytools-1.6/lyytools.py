# pip install --no-index --find-links=https://pypi.org/simple/ lyysdk
# https://pypi.org/project/lyysdk/#description
# pip install lyypy -i https://pypi.org/simple/ --trusted-host pypi.org --upgrade
"""
python setup.py sdist bdist_wheel
twine upload dist/*
pip install --upgrade lyysdk -i https://pypi.org/simple/ --trusted-host pypi.org
"""
import time
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import re, os, sys
import pandas as pd
import colorama
import pickle


def is_running_as_exe():
    if getattr(sys, "frozen", False):
        # 运行为独立可执行文件
        return True
    elif hasattr(sys, "gettrace"):
        # 运行时使用调试器
        return False
    else:
        # 未知运行状态
        return False


colorama.init()
from colorama import Fore, Back, Style

#  创建一个字典，将普通颜色名称转换为colorama颜色
color_map = {"red": Fore.RED, "green": Fore.GREEN, "blue": Fore.BLUE, "yellow": Fore.YELLOW, "white": Fore.WHITE, "black": Fore.BLACK, "cyan": Fore.CYAN, "magenta": Fore.MAGENTA, "light_green": Fore.GREEN + Style.BRIGHT, "light_blue": Fore.BLUE + Style.BRIGHT, "light_yellow": Fore.YELLOW + Style.BRIGHT, "light_white": Fore.WHITE + Style.BRIGHT, "light_black": Fore.BLACK + Style.BRIGHT}


def print_color(text, color="red", bg="white", style=Style.NORMAL):
    """
    print_color("hello world", color="yellow")
    """

    color = color_map[color]
    # print_color("hello world", bg=Back.BLACK)
    print(color + style + text)


def cache_list_to_disk(lst, filename):
    with open(filename, "wb") as f:
        pickle.dump(lst, f)


def load_list_from_disk(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def get_data_from_cache_or_func(cache_file_path, expiry_duration, next_func=None, debug=False):
    # 检查文件是否存在,expiry_duration=3600意味着1小时。
    def read_cache(expiry_duration):
        if os.path.isfile(cache_file_path):
            if debug:
                print("file exists, check expiry duration")
            # 获取文件的最后修改时间
            last_modified_time = os.path.getmtime(cache_file_path)
            # 计算当前时间与最后修改时间的差值（秒）
            current_time = time.time()
            time_difference = current_time - last_modified_time
            if time_difference < expiry_duration:
                df = pd.read_pickle(cache_file_path)
                if debug:
                    print(f"{cache_file_path} not expired, return it, df=\n", df)
                return df

    # all else:
    df = read_cache(expiry_duration)

    if df is not None:
        return df
    elif next_func is not None:
        if debug:
            print(f"enter next_func={next_func}")
        df = next_func()
        df.to_pickle(cache_file_path)
        return df
    else:
        if debug:
            print(f"cache expired, and no next_func specified, expiry_duration*10, return expied cache")
        df = read_cache(expiry_duration * 10)
        return df


def assign(list1, list2):
    """
    把服务器列表依次、循环分配到股票代码，让每个代码拥有专属服务器
    """
    dict_result = {}
    iter_list2 = iter(list2)
    for idx, val in enumerate(list1):
        try:
            dict_result[val] = next(iter_list2)
        except StopIteration:
            iter_list2 = iter(list2)
            dict_result[val] = next(iter_list2)
    dict_result = {k: v for k, v in dict_result.items() if v is not None}
    return dict_result


def 万能股票代码(原始股票代码, 需要的示例):
    """
    示例随便啥股票代码，关键是样式。比如 万能股票代码('sh600001','000003.sz')就会变成sz.000003
    就是这么神奇
    """
    if len(str(原始股票代码)) < 6:
        原始股票代码 = str(原始股票代码).zfill(6)
    需要的点的下标 = 原始股票代码.find(".")
    szsh位置 = max(原始股票代码.find("sz"), 原始股票代码.find("sh"))

    strPattern = "[6|3|0][0-9]{5}"
    result = re.findall(strPattern, 原始股票代码)
    数字代码 = result[0]

    市场 = "sh" if str(数字代码)[:1] == "6" else "sz"
    # print("市场=",市场)
    目标代码替代数字 = re.sub(r"[6|3|0][0-9]{5}", str(数字代码), str(需要的示例))

    目标代码 = re.sub(r"[shz]{2}", 市场, 目标代码替代数字)
    return 目标代码


def lyydebug(debug, text):
    get_fun_name_cmd_text = "fun_name=str(sys._getframe().f_code.co_name)"
    fun_name = ""
    try:
        eval(get_fun_name_cmd_text)
    except Exception as e:
        print(e)
    out_txt = "[" + fun_name + "]:" + text
    print(out_txt)
    return out_txt


def divide_list(lst, n):
    quotient = len(lst) // n
    remainder = len(lst) % n
    result = []
    start = 0
    for i in range(n):
        if i < remainder:
            end = start + quotient + 1
        else:
            end = start + quotient
        result.append(lst[start:end])
        start = end
    return result


def get_time(f):
    def inner(*args, **kwargs):
        s_time = time.time()
        res = f(*args, **kwargs)
        e_time = time.time()
        duration = round(e_time - s_time, 2)
        print("\n<" + f.__name__ + "> 耗时：" + str(duration) + " 秒")
        return res

    return inner


def 测速(开始时间, 额外说明):
    spend = datetime.now() - 开始时间
    print("\n<-" + 额外说明 + "-> 耗时: {}秒".format(spend))
    return spend


def speed_test(start_time, comment):
    """测试运行时间

    Args:
        start_time (time): 开始时间
        comment (str): 函数名或者其它说明，

    Returns:
        float: 运行时间秒数
    """
    debug = False
    end_time = time.time()
    run_time = end_time - start_time
    print(f"{comment} runtime: {run_time:.2f} seconds")

    rounded_run_time = round(run_time, 2)  # 保留2位小数
    return rounded_run_time


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def lyyf_logger(log_filename_prefix, message, if_print=False):
    """
    可以每次调用，都会自动创建当天的日志文件，日志文件名为lyylog_前缀_日期.log
    比如lyylog_lyymsg_svc_log_2023-08-24.log
    不再被占用，可以实时删除
    基本完美了
    Args:
        log_filename_prefix (_type_): _description_
        message (_type_): _description_
    """

    if if_print:
        print(message)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = None

    if handler is None:
        today = datetime.now().strftime("%Y-%m-%d")
        handler = CustomTimedRotatingFileHandler(f"lyylog_{log_filename_prefix}_{today}.log", when="midnight", interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    with handler:
        logger.info(message)


if __name__ == "__main__":
    print(is_running_as_exe())
    pass
