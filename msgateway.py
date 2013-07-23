# -*- coding:utf-8 -*-

import contextlib
import urllib
import base64
import OpenSSL


def demo_info():
    # 接口地址
    API_URL = 'https://sandbox.99bill.com/msgateway/recvMsgatewayMerchantInfoAction.htm'
    # 接口参数列表
    API_PARAM = ['inputCharset', 'pageUrl', 'bgUrl', 'version', 'language', 'signType', 'payeeContactType', 'payeeContact', 'payerName', 'payerContactType', 'payerContact', 'payTolerance', 'orderId', 'orderAmount', 'payeeAmount', 'orderTime', 'productName', 'productNum', 'productDesc', 'ext1', 'ext2', 'payType', 'bankId', 'pid', 'sharingData', 'sharingPayFlag', 'signMsg']

    # 测试用例
    params = {
        'inputCharset'     : '1',
        'bgUrl'            : 'http://www.demo.com/callBack?orderId=DEMO901234',
        'version'          : 'v2.0',
        'language'         : '1',
        'signType'         : '4',
        'payerName'        : 'San Zhang',
        'payeeContactType' : '1',
        'payeeContact'     : '1971412292@qq.com',
        'orderId'          : 'DEMO901234',
        'orderAmount'      : '2000',
        'payeeAmount'      : '1500',
        'orderTime'        : '20130801120000',
        'productName'      : '苹果',
        'productNum'       : '1',
        'payType'          : '00',
        'sharingPayFlag'   : '1',
        'sharingData'      : '1^843004510@qq.com^500^0^test',
        'pid'              : '10012138843',
    }

    # 签名字符串输入, 参数顺序需要和接口文档中定义的顺序一致
    sign_str = '&'.join('='.join(kv) for kv in sorted(
            params.iteritems(),
            lambda x, y: cmp(API_PARAM.index(x), API_PARAM.index(y)),
            lambda x: x[0],
        ))

    # 测试帐户私钥
    with contextlib.closing(open('demo.pem')) as f:
        pk = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, f.read())
    # 私钥加密后进行Base64转码
    params['signMsg'] = base64.encodestring(OpenSSL.crypto.sign(pk, sign_str, 'sha1'))

    print 'Request URL: %s?%s' % (API_URL, urllib.urlencode(params))


if __name__ == '__main__':
    print '>>> 分账网关收款接口'
    demo_info()

