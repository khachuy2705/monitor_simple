Cài đặt python3, và các gói cần thiết
yum install epel-release -y & yum install python36 python36-pip.noarch -y && pip3 install requests

Cách chạy app, sau khi thay cấu hình trong file config.py
cd <đường dẫn thư mục app>
python3 monitor_simple.py

Cách thiết lập chạy mỗi phút 1 lần:
crontab -l
Thêm vào dòng sau:
* * * * * /usr/bin/python3 <đường dẫn file monitor_simple.py>