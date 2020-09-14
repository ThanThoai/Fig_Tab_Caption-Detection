# Figure, Table vs Caption Detection


## Install 

+ Make env 
+ chmod 777 ./install.sh
+ ./install.sh


## Model:
link: https://www.dropbox.com/s/vh9jynbeihpwpoc/model_final.pth?dl=0
Tải model về rồi tạo thư mục model và cho model vào trong thư mục đó.
Nếu máy không có gpu thì chỉnh sửa cuda thành cpu trong file config.yml
## Train: 

download dataset (link trong document) về rồi giải nén ảnh  và file data.json vào  các thư mục tương ứng .
chạy lệnh: python train.py