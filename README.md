# checkmk-webhook-notify

Truy cập vào máy chủ Checkmmk.

Chuyển user sang site cần cần cài đặt webhook, ví dụ site có tên là `mon`:
```
root@checkmk:~# su mon
```

Khi truy cập vào site thì sẽ có thư mục sau:
```
OMD[mon]:~$ ll
total 12
lrwxrwxrwx  1 mon mon   11 Mar 26 09:20 bin -> version/bin/
drwxr-x--x 20 mon mon 4096 Mar 26 09:23 etc/
lrwxrwxrwx  1 mon mon   15 Mar 26 09:20 include -> version/include/
lrwxrwxrwx  1 mon mon   11 Mar 26 09:20 lib -> version/lib/
drwxr-x---  5 mon mon 4096 Mar 26 09:20 local/
lrwxrwxrwx  1 mon mon   13 Mar 26 09:20 share -> version/share/
drwxr-x--x 11 mon mon  280 Mar 26 14:08 tmp/
drwxr-x--- 14 mon mon 4096 Mar 26 10:38 var/
lrwxrwxrwx  1 mon mon   27 Mar 26 09:20 version -> ../../versions/2.3.0p29.cre/
```

Truy cập vào thư mục cài notifications

```
cd local/share/check_mk/notifications/
```

1 - Tải file cài & thêm quyền thực thi khi dùng với webhook.site:
```
wget https://raw.githubusercontent.com/huydv398/checkmk-webhook-notify/refs/heads/main/webhook.py
chmod +x webhook.py
```

2 - Tải file cài & thêm quyền thực thi khi dùng với discord webhook:
```
wget https://raw.githubusercontent.com/huydv398/checkmk-webhook-notify/refs/heads/main/discord-webhook.py
chmod +x discord-webhook.py
```
Kiểm tra lại `Add notification rule` => `Notification Method`.
