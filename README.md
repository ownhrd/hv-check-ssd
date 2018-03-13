# hv-check-ssd
Парсинг почтовых сообщений от Intel® Rapid Storage Technology enterprise на предмет деградации локальных дисковых массивов и отправка трапов в Zabbix. 

# Crontask:

**hv_check_ssd**
```
# start check vulners hourly
* * * * * root python /usr/local/bin/hv_check_ssd.py &> /var/log/hv_check_ssd
```
