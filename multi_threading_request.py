from multiprocessing.dummy import Pool as ThreadPool
import itertools
import concurrent.futures
import json
import time
import requests
from prettytable import PrettyTable


id_to_hoc = ["-4876368189337256838", "-8897043996427631220",
                 "-6531752470926280013", "-7703973204741067629",
                 "-7582847182110048548", "-6092972359370660665"]


def login():
    url_login = "http://qldt.hanu.vn/api/auth/login"

    payload = {"username": "2101040061", "password": "06062003", "grant_type": "password"}

    headers_login = {"Host": "qldt.hanu.vn",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                     "Cookie": "ASP.NET_SessionId=mlqxi0uf4zggqs5lnmo0hfuy",
                     "Content-Length": "57"}
    login = requests.post(url_login, data=payload, headers=headers_login)

    if login.status_code == 200:
        print("Đăng nhập thành công!")
        return json.loads(json.dumps(login.json()))['access_token']
    else:
        print("Đăng nhập thất bại!\nHãy kiểm tra lại thông tin đăng nhập")
        print(login.content)
        exit()



def multithread_request(data, access_token):

    url_reg = "http://qldt.hanu.vn/api/dkmh/w-xulydkmhsinhvien"

    auth = "Bearer " + access_token

    headers_reg = {"Host": "qldt.hanu.vn",
               "Content-Length": "65",
                "Authorization": auth, "Content-Type": "application/json",
               "Cookie": "ASP.NET_SessionId = mlqxi0uf4zggqs5lnmo0hfuy",
               "Connection": "close"
               }

    global result_json

    result = requests.post(url_reg, data=json.dumps(data), headers=headers_reg)
    result_json = json.loads(json.dumps(result.json()))


    return result.status_code


def search_nhom_to(search):
    data = json.load(open('subject.json'))
    ds_nhom_to = data['data']['ds_nhom_to']
    ds_mon_hoc = data['data']['ds_mon_hoc']

    for t in ds_nhom_to:
        if search == t['id_to_hoc']:
            for x in ds_mon_hoc:
                if t['ma_mon'] == x['ma']:
                    return x['ten']





if __name__ == '__main__':

    access_token = login()



    #use concurrent.futures for multithreading
    #if a thread is not return with 200 status code, it will be resbmitted

    payload_reg = {"filter":{
                    "id_to_hoc": "temp",
                    "is_checked": "true",}
                    }

    dk_result = PrettyTable(['Tên môn học', 'Trạng thái đăng ký', 'Lý do lỗi (nếu có)'])
    dk_result._title = 'Kết quả'
    dk_result.align['Tên môn học'] = "l"
    dk_result.align['Lý do'] = "l"
    dk_result.padding_width = 1


    payload_reg_dict = {}

    #nest the payload_reg into a list and set id_to_hoc to each element
    #then use itertools to cycle through the list
    for i in id_to_hoc:
        payload_reg['filter']['id_to_hoc'] = i
        payload_reg_dict[i] = payload_reg


    #use multiprocessing.dummy.Pool and spawn one thread for each request
    #if a thread is not return with 200 status code, it will be resbmitted
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(multithread_request, data, access_token): data for data in payload_reg_dict}
        #check if all the threads are return with 200 status code
        #if not, resubmit the request
        for future in concurrent.futures.as_completed(future_to_url):
            if future.result() == 200:
                if result_json['data']['is_thanh_cong'] == False:
                    # print(future_to_url[future], type(future_to_url[future]))
                    dk_result.add_row([search_nhom_to(future_to_url[future]), 'Thất bại!', result_json['data']['thong_bao_loi']])
                    # print("Môn học", search_nhom_to(future_to_url[future]), "đăng ký thất bại!")
                    # print("Lỗi:", result_json['data']['thong_bao_loi'])
                else:
                    dk_result.add_row([search_nhom_to(future_to_url[future]), 'Thành công!', 'Hãy kiểm lại trên trang QLDT!'])
            else:
                future_to_url[future] = multithread_request(future_to_url[future], access_token)
                print("Resubmitted request: ", future_to_url[future])


    print(dk_result)






