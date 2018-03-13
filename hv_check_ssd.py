#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Igor Sidorenko"
__email__ = "neither89@gmail.com"
__status__ = "Production"


import imaplib
import email
import re
from pyzabbix import ZabbixMetric, ZabbixSender

def zbx_send(packet):
    ZabbixSender('127.0.0.1').send(packet)

mail = imaplib.IMAP4_SSL('mail.example.com')
mail.login('USER', 'PASSWORD')
mail.list()
mail.select("INBOX") # connect to inbox.

result, data = mail.search(None, "UNSEEN")

ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string

d = {}
d = dict()

for id in id_list:

    result, data = mail.fetch(id, "(RFC822)")
    raw_email = data[0][1] # here's the body, which is raw text of the whole email
# including headers and alternate payloads

    msg = email.message_from_string(raw_email)

    hv_result = re.search(r'HV\d{2}\b', msg.get_payload(decode=True))
    if hv_result:
        hv = (hv_result.group(0).lower() + ".example.com") #HOSTNAME: HV21 = hv21..example.com (hostname in Zabbix)

    hv_result = re.search(r'HV\d{3}\b', msg.get_payload(decode=True))
    if hv_result:
        hv = (hv_result.group(0).lower() + ".company.ru") #HOSTNAME: HV111 = hv111.company.ru (hostname in Zabbix)

    degraded = re.search(r'Degraded', msg.get_payload(decode=True))
    if degraded:
        d.update({hv: 2})

    rebuild_progress = re.search(r'Rebuilding in progress', msg.get_payload(decode=True))
    if rebuild_progress:
        d.update({hv: 1})

    rebuild_complete = re.search(r'Rebuilding complete', msg.get_payload(decode=True))
    if rebuild_complete:
        d.update({hv: 0})

    mail.store(id, '+FLAGS', '\\Seen')

for key, value in d.iteritems():
    packet = [ZabbixMetric(key, 'ssd.status', value)]
    zbx_send(packet)
d.clear()
