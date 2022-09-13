import requests
import json
import urllib.request
from prettytable import PrettyTable


#this function is used to check internet connectivity
def check_connect(host):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


#login function
def login():
    if check_connect('http://qldt.hanu.vn'):

        global access_token

        url = "http://qldt.hanu.vn/api/auth/login"

        headers = {"Host": "qldt.hanu.vn",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                   "Cookie": "ASP.NET_SessionId=mlqxi0uf4zggqs5lnmo0hfuy",
                   "Content-Length": "57"}
        # payload = {"username=2101040061&password=06062003&grant_type=password"}
        # 2101040061   06062003
        username = input("Nhập tên đăng nhập:\n")
        password = input("Nhập mật khẩu đăng nhập:\n")
        payload = {"username": username, "password": password, "grant_type": "password"}
        x = requests.post(url, data=payload, headers=headers)

        if x.status_code == 200:
            print("Đăng nhập thành công!")
            access_token = json.loads(json.dumps(x.json()))['access_token']
            get_student_info(access_token)
        else:
            print("Đăng nhập thất bại!\nHãy kiểm tra lại thông tin đăng nhập")
            login()
            # print(x.content)
    else:
        print("Could not connect to http://qldt.hanu.vn\nEither the server is down or check your internet connection")



# this function will get student information
def get_student_info(access_token):

    url = "http://qldt.hanu.vn/api/dkmh/w-locsinhvieninfo"

    auth = "Bearer " + access_token

    headers = {"Host": "qldt.hanu.vn",
               "Content-Length": "0",
               "Authorization": auth,
               "Cookie": "ASP.NET_SessionId=mlqxi0uf4zggqs5lnmo0hfuy"}

    info = requests.post(url, headers=headers)

    global infor_dict

    if info.status_code == 200:
        infor_dict = json.loads(json.dumps(info.json()))
        welcome_message()
    else:
        print("Could not retrieve student information")


# print welcome messages
def welcome_message():
    x = infor_dict['data']
    print("Welcome to qldt.hanu.vn")
    print("Chào mừng " + x['ten_day_du'])
    print("Giới tính: " + x['gioi_tinh'])
    print("Năm sinh: " + x['ngay_sinh'])
    print("Quê quán: " + x['noi_sinh'])
    print("Email: " + x['email'] + ", số điện thoại: " + x['dien_thoai'])
    print("Mã sinh viên: " + x['ma_sv'])
    print("Khoa: " + x['khoa'])
    print("Lớp: " + x['lop'] + ", niên khoá: " + x['nien_khoa'])
    print("Cố vấn học tập: " + x['ho_ten_cvht'] + ", sdt: " + x['dien_thoai_cvht'] + ", email: " + x['email_cvht'])




# get subject
def get_subject(access_token):
    url = "http://qldt.hanu.vn/api/dkmh/w-locdsnhomto"

    auth = "Bearer " + access_token

    headers = {"Host": "qldt.hanu.vn",
               "Content-Length": "332", "Accept": "application/json, text/plain, */*",
               "Authorization": auth, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
               "Content-Type": "application/json", "Origin": "https://qldt.hanu.vn", "Referer": "https://qldt.hanu.vn", "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", "Cookie": "ASP.NET_SessionId=mlqxi0uf4zggqs5lnmo0hfuy", "Connection": "close"}

    payload = json.loads('{"is_CVHT":false,"additional":{"paging":{"limit":8000,"page":1},"ordering":[{"name":"","order_type":""}]}}')

    subject = requests.post(url, json=payload, headers=headers)

    if subject.status_code == 200:
        print("Lấy môn học thành công!")
        with open('subject.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(subject.json(), ensure_ascii=False, indent=4))
        print_to_file()
        print("Kiểm tra file ds_nhom_to.txt trong folder.")
    else:
        print(subject.status_code)
        print("Failed")
        print(subject.content)

def print_to_file():
    data = json.load(open('subject.json'))
    ds_nhom_to = data['data']['ds_nhom_to']
    ds_mon_hoc = data['data']['ds_mon_hoc']

    nhom_to = PrettyTable(['Mã môn', 'Tên môn học', 'Nhóm', 'Tổ', 'Số tín chỉ', 'Lớp', 'ID Môn'])
    nhom_to.title = 'Danh sách môn học'
    # nhom_to.align['Tên môn học'] = "l"
    # nhom_to.align['Mã môn'] = "l"
    nhom_to.padding_width = 1


    for t in ds_nhom_to:
        for x in ds_mon_hoc:
            if t['ma_mon'] == x['ma']:
                ten_mon_hoc = x['ten']
        nhom_to.add_row([t['ma_mon'], ten_mon_hoc, t['nhom_to'], t['to'], t['so_tc'], t['lop'], t['id_to_hoc']])

    print(nhom_to)

    # with open('ds_nhom_to.txt', 'w') as f:
    #     f.write(str(nhom_to))


def search_nhom_to():
    data = json.load(open('subject.json'))
    ds_nhom_to = data['data']['ds_nhom_to']
    ds_mon_hoc = data['data']['ds_mon_hoc']

    nhom_to = PrettyTable(['Mã môn', 'Tên môn học', 'Nhóm', 'Tổ', 'Số tín chỉ', 'Lớp', 'ID Môn'])
    nhom_to.title = "Kết quả tìm kiếm"
    # nhom_to.align['Tên môn học'] = "l"
    # nhom_to.align['Mã môn'] = "l"
    nhom_to.padding_width = 2

    search = input('Nhập mã môn học để tìm kiếm: ')

    for t in ds_nhom_to:
        if search in t['ma_mon']:
            for x in ds_mon_hoc:
                if t['ma_mon'] == x['ma']:
                    ten_mon_hoc = x['ten']
            nhom_to.add_row([t['ma_mon'], ten_mon_hoc, t['nhom_to'], t['to'], t['so_tc'], t['lop'], t['id_to_hoc']])

    if len(list(nhom_to)) != 0:
        print(nhom_to)
    else:
        nhom_to.add_row(['', 'Không tìm thấy môn học trùng với từ khoá!', '', '', '', '', ''])
        print(nhom_to)


def test_dk_tin(access_token):

    url = "http://qldt.hanu.vn/api/dkmh/w-xulydkmhsinhvien"

    auth = "Bearer " + access_token

    payload = {"filter":{
                "id_to_hoc":"temp",
                "is_checked":"true"}
            }

    headers = {"Host": "qldt.hanu.vn",
               "Content-Length": "65",
                "Authorization": auth, "Content-Type": "application/json",
               "Cookie": "ASP.NET_SessionId = mlqxi0uf4zggqs5lnmo0hfuy",
               "Connection": "close"
               }

    result_dk = requests.post(url, data=json.dumps(payload), headers=headers)

    if result_dk.status_code == 200:
        if result_dk.json()['data']['is_thanh_cong']:
            print("Đăng ký thành công!")
        else:
            print("Đăng ký không thành công!")
    else:
        print("Failed")
        print(result_dk.status_code)
    # print(response.content)





if __name__ == '__main__':
    # login()
    # test_dk_tin(access_token)
    # get_subject(access_token)
    # search_nhom_to()
    print_to_file()