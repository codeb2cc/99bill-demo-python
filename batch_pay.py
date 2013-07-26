# -*- coding:utf-8 -*-

import os
import datetime
import md5

import suds


def simple_pay(client):
    request_bean = client.factory.create('ns0:SimpleRequestBean')

    request_bean.amount = 100
    request_bean.creditName.set(u'李梦丽')
    request_bean.creditContact.set(u'1971412292@qq.com')
    request_bean.currencyCode.set(u'1')
    request_bean.description.set(u'付款接口测试')
    request_bean.correctName.set(u'n')
    request_bean.tempAccount.set(u'n')
    request_bean.orderId.set('ORDER' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    merchant_key = 'YKB4WI4GS6UDNZXN'
    merchant_id = '10012138842'
    merchant_ip = '192.168.8.1'

    m = md5.md5()
    m.update(request_bean.creditContact.get())
    m.update(request_bean.currencyCode.get())
    m.update('%d' % request_bean.amount)
    m.update(request_bean.orderId.get())
    m.update(merchant_key)

    request_bean.mac = m.hexdigest()

    response_bean = client.service.simplePay([request_bean, ], merchant_id, merchant_ip)

    return response_bean[0]


def bank_pay(client):
    request_bean = client.factory.create('ns0:BankRequestBean')

    request_bean.province_city.set(u'北京')
    request_bean.bankName.set(u'工商银行')
    request_bean.kaihuhang.set(u'南京支行')
    request_bean.creditName.set(u'张三')
    request_bean.bankCardNumber.set(u'6225881256252189')
    request_bean.amount = 2.8
    request_bean.description.set(u'Demo Test')
    request_bean.orderId.set('ORDER' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    merchant_key = 'YKB4WI4GS6UDNZXN'
    merchant_id = '10012138842'
    merchant_ip = '222.190.107.178'

    m = md5.md5()
    m.update(request_bean.bankCardNumber.get())
    m.update('%d' % request_bean.amount)
    m.update(request_bean.orderId.get())
    m.update(merchant_key)

    request_bean.mac = m.hexdigest()

    response_bean = client.service.bankPay([request_bean, ], merchant_id, merchant_ip)

    return response_bean[0]


def deal_query(client):
    request_bean = client.factory.create('ns0:QueryRequestBean')

    request_bean.dealId.set(u'1')
    request_bean.dealBeginDate.set(datetime.datetime(2013, 6, 1).strftime('%Y-%m-%d %H:%M:%S'))
    request_bean.dealEndDate.set(datetime.datetime(2013, 7, 1).strftime('%Y-%m-%d %H:%M:%S'))
    request_bean.queryType.set(u'simplePay')
    request_bean.orderId.set(u'')

    merchant_id = '10012138842'
    merchant_ip = '222.190.107.178'

    response_bean = client.service.queryDeal([request_bean, ], merchant_id, merchant_ip)

    return response_bean[0]


if __name__ == '__main__':
    wsdl_file = os.path.join(os.getcwd(), 'BatchPayWS.xml')
    client = suds.client.Client('file://' + wsdl_file)

    rb = simple_pay(client)

    print 'Simple Pay Response'
    print '  Order ID: %s' % response_bean[0].orderId
    print '  Deal ID: %s' % response_bean[0].dealId
    print '  Status: %s' % response_bean[0].resultFlag

    rb = bank_pay(client)
    print 'Bank Pay Response'
    print '  Order ID: %s' % response_bean[0].orderId
    print '  Deal ID: %s' % response_bean[0].dealId
    print '  Status: %s' % response_bean[0].resultFlag

