#coding:utf-8

# 导入hashlib包，用来生成md5
import hashlib
import datetime
import json

# 初始化list变量passwd_num_list，用于列表存储md5串内的数字串
passwd_num_list = []
passwd_letter_list = []
# 输入明文密码字符串
clear_passwd = 'input your password here.'

# 调用hashlib包，生成md5字符串，并赋值给md5_passwd
# 注意：这里的temp_passwd只是一个md5 HASH object，并不是真正的md5字符串
temp_passwd = hashlib.md5(clear_passwd)
md5_passwd = temp_passwd.hexdigest()

# 使用filter提取md5字符串里的数字和字母
passwd_num = filter(str.isdigit,md5_passwd)
passwd_letter = filter(str.isalpha,md5_passwd)

# 把passwd_num转换成整形存储进passwd_num_list内
for i in passwd_num:
    passwd_num_list.append(int(i))
# 把passwd_letter转换成整形存储进passwd_letter_list内
for i in passwd_letter:
    passwd_letter_list.append(str(i))

# 定义gen_port()函数，用抽取md5串的前6个数字字符进行运算生成随机端口
def gen_port(list_input):
    # 使用datetime生成4位日期串
    date_4 = datetime.datetime.now().strftime("%m%d")
    # 初始化临时list变量
    temp_time_list = []
    temp_list = [0,0,0,0,0,0]
    temp_3 = [0,0,0]
    for i in range(0,3):
        temp_list[i] = list_input[i]
    for i in range(3,6):
        temp_3[i-3] = list_input[i]
    i = 0
    while i <= len(temp_3)+1:
        temp_list[i+3] = temp_3.pop(-1)
        i = i+1
    # 现在temp_list内存储的是经过处理的6位md5数字字符串
    # 把date_4内的日期串处理并存储成list
    for i in date_4:
        temp_time_list.append(int(i))
    port_num = (temp_list[0]+temp_list[1]+temp_list[2]+temp_time_list[0])*1500+(temp_list[3]+temp_time_list[1])*180+(temp_list[4]+temp_time_list[1])*60+temp_list[5]+temp_time_list[1]
    return port_num

def gen_passwd(letter_list_input,num_list_input):
    passwd = ''
    temp_time_list = []
    temp_list = []
    temp_letter_list = [0,0,0,0,0,0,0,0]
    passwd_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # 使用datime生成8位日期串
    date_8 = datetime.datetime.now().strftime("%Y%m%d")
    for i in date_8:
        temp_time_list.append(int(i))
    for i in range(0,8):
        temp_list.append(num_list_input[-i])
    # 逐位相加，取个位数
    for i in range(0,8):
        temp = (temp_list[i]+temp_time_list[i])%10
        temp_list[i] = temp
    # 为了弥补字母串很大可能不够8位，从反向开始取字母串
    for i in range(0,8):
        temp_letter_list[i] = letter_list_input[-len(letter_list_input)+i]
    for i in range(0,14,2):
        passwd_list[i] = temp_list.pop()
    for i in range(1,15,2):
        passwd_list[i] = temp_letter_list.pop()
    for i in range(0,15):
        passwd = passwd + str(passwd_list[i])
    return passwd

# 用于更新ss配置文件的函数，把生成的端口和密码更新进/etc/shadowsocks.json
def update_json_config(password,port):
    json_file = "/etc/shadowsocks.json"#服务器端的配置文件
    json_config = json.loads(open(json_file, 'r').read())
    json_config["server_port"] = port
    json_config["password"] = password
    json_file_update = json.dumps(json_config, indent=4)
    update_oper = open(json_file,'w')
    update_oper.truncate()
    update_oper.write(json_file_update)

# 转换passwd编码到utf-8
encrypt_passwd = (gen_passwd(passwd_letter_list,passwd_num_list)).encode("utf-8")
encrypt_port = gen_port(passwd_num_list)

# 更新ss配置文件/etc/shadowsocks.json
update_json_config(encrypt_passwd,encrypt_port)
