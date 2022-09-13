import json
from prettytable import PrettyTable

data = json.load(open('subject.json'))
ds_nhom_to = data['data']['ds_nhom_to']
ds_mon_hoc = data['data']['ds_mon_hoc']

mon_hoc = PrettyTable(['Mã môn', 'Tên môn'])
nhom_to = PrettyTable(['Mã môn', 'Tên môn học', 'Nhóm', 'Tổ', 'Số tín chỉ', 'Lớp', 'ID Môn'])
nhom_to.align['Tên môn học'] = "l"
nhom_to.align['Mã môn'] = "l"
nhom_to.padding_width = 1

# for x in ds_mon_hoc:
#     mon_hoc.add_row([x['ma'], x['ten']])

# print(mon_hoc)

for t in ds_nhom_to:
    for x in ds_mon_hoc:
        if t['ma_mon'] == x['ma']:
            ten_mon_hoc = x['ten']
    nhom_to.add_row([t['ma_mon'], ten_mon_hoc, t['nhom_to'], t['to'], t['so_tc'], t['lop'], t['id_mon']])

# print(nhom_to)

with open('ds_nhom_to.txt', 'w') as f:
    f.write(str(nhom_to))

# with open('ds_mon_hoc.txt', 'w') as w:
#     w.write(str(t))
    # print("Mã khoá: " + x['ma'])
    # print("Tên khoá: " + x['ten'])

# print(data['data']['ds_khoa'])
# print(data['data']['ds_khoa'][0])