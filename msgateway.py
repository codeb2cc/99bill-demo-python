# -*- coding:utf-8 -*-

import contextlib
import datetime
import urllib, urllib2
import base64
import OpenSSL


def demo_info():
    # 接口测试地址
    API_URL = 'https://sandbox.99bill.com/msgateway/recvMsgatewayMerchantInfoAction.htm'
    # 参数列表, 按接口文档中的定义排序
    API_PARAM = [
        'inputCharset', 'pageUrl', 'bgUrl', 'version', 'language', 'signType',
        'payeeContactType', 'payeeContact', 'payerName', 'payerContactType', 'payerContact',
        'payTolerance', 'orderId', 'orderAmount', 'payeeAmount', 'orderTime', 'productName',
        'productNum', 'productDesc', 'ext1', 'ext2', 'payType', 'bankId', 'pid', 'sharingData',
        'sharingPayFlag',
    ]

    # 测试用例
    params = {
        'inputCharset'     : '1',
        'bgUrl'            : 'http://codeb2cc.com/callBack?orderId=DEMO901234',
        'version'          : 'v2.0',
        'language'         : '1',
        'signType'         : '4',
        'payerName'        : 'San Zhang',
        'payeeContactType' : '1',
        'payeeContact'     : '1971412292@qq.com',
        'orderId'          : 'DEMO' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'orderAmount'      : '2000',
        'payeeAmount'      : '1500',
        'orderTime'        : datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'productName'      : '苹果',
        'productNum'       : '1',
        'payType'          : '00',
        'sharingPayFlag'   : '1',
        'sharingData'      : '1^843004510@qq.com^500^0^test',
        'pid'              : '10012138843',
    }

    # 签名字符串输入, 参数顺序需要和接口文档中定义的顺序一致
    # IMPORTANT: 参数值不能进行转义, 空值参数不加入签名字符串
    sign_str = '&'.join('='.join(kv) for kv in sorted(
            params.iteritems(),
            lambda x, y: cmp(API_PARAM.index(x), API_PARAM.index(y)),
            lambda x: x[0],
        ))

    # 测试帐户私钥
    with contextlib.closing(open('demo.pem')) as f:
        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, f.read())
    # 私钥加密后进行Base64转码
    params['signMsg'] = base64.encodestring(OpenSSL.crypto.sign(private_key, sign_str, 'sha1'))

    print '  Request URL: %s?%s' % (API_URL, urllib.urlencode(params))


def demo_callback():
    CALLBACK_PARAM = [
        'version', 'language', 'signType', 'payType', 'bankId', 'pid', 'orderId',
        'orderTime', 'orderAmount', 'dealId', 'bankDealId', 'dealTime', 'payAmount', 'fee',
        'payeeContactType', 'payeeContact', 'payeeAmount', 'ext1', 'ext2', 'payResult',
        'sharingResult', 'errCode',
    ]

    # 支付成功回调例子
    CALLBACK_QUERY = 'orderId=DEMO901234&version=v2.0&language=1&signType=4' \
        '&payType=10&bankId=UPOP&pid=10012138843&orderId=DEMO20130723151339' \
        '&orderTime=20130723151339&orderAmount=2000&dealId=25753688&bankDealId=130723105705' \
        '&dealTime=20130723151354&payAmount=2000&fee=2&payeeContactType=1' \
        '&payeeContact=1971412292%40qq.com&payeeAmount=1498&ext1=&ext2=&payResult=10' \
        '&sharingResult=1%5E843004510%40qq.com%5E500%5E0%5Etest%5E500%7C&errCode=' \
        '&signMsg=naWPSHiH3cJjClMJThsAphz2WWJPj5k8QQUUjiyAYUPr4%2F9qsjSKSmole%2B%2FID1obfbih1IfQpn2Xs2ObQ2NkZs8hqxLnEcu1CjWML1y9ezsNcx8VZFmxYODabXxnmKVJoJs%2Fm78sR8hKsxwXdFSQy48MiT6oD1B4nR%2BQJIwOHqw%3D' \
        '&orderVersion=msgatewayv2.0&merchantAcctId=10012138843'

    print '  Callback Query: %s' % CALLBACK_QUERY

    params = dict(urllib2.urlparse.parse_qsl(CALLBACK_QUERY))

    # 移除签名参数列表外的参数
    sign_params = params.copy()
    for k in params:
        if not k in CALLBACK_PARAM:
            sign_params.pop(k)

    sign_str = '&'.join('='.join(kv) for kv in sorted(
            sign_params.iteritems(),
            lambda x, y: cmp(CALLBACK_PARAM.index(x), CALLBACK_PARAM.index(y)),
            lambda x: x[0],
        ))

    with contextlib.closing(open('99bill.cert.rsa.20140803.cer')) as f:
        certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())
        public_key = certificate.get_pubkey()

        print '  Signature Algorithm: %s' % certificate.get_signature_algorithm()
        print '  Public Key Type: %d' % public_key.type()
        print '  Public Key Bits: %d' % public_key.bits()

    OpenSSL.crypto.verify(certificate, base64.decodestring(params['signMsg']), sign_str, 'sha1')


def demo_refund():
    API_URL = 'https://sandbox.99bill.com/msgateway/recvMerchantRefundAction.htm'
    API_PARAM = [
        'inputCharset', 'version', 'signType', 'orderId', 'pid', 'seqId', 'returnAllAmou',
        'nt', 'getTolerance', 'returnTime', 'ext1', 'ext2', 'returnDetail', 'returnSharingDetail',
        'assignAcct', 'refundFlag', 'shareRefundFeeFlag',
    ]

    params = {
        'inputCharset'               : '1',
        'version'                    : 'v2.0',
        'signType'                   : '4',
        'orderId'                    : 'DEMO' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'pid'                        : '10012138843',
        'seqId'                      : 'S' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'returnAllAmou'              : '600',
        'returnTime'                 : datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'returnDetail'               : '1^843004510@qq.com^100|1^1971412292@qq.com^500^1',
        'shareRefundFeeFlag'         : '0',
    }

    sign_str = '&'.join('='.join(kv) for kv in sorted(
            params.iteritems(),
            lambda x, y: cmp(API_PARAM.index(x), API_PARAM.index(y)),
            lambda x: x[0],
        ))

    with contextlib.closing(open('demo.pem')) as f:
        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, f.read())
    params['signMsg'] = base64.encodestring(OpenSSL.crypto.sign(private_key, sign_str, 'sha1'))

    print '  Request URL: %s?%s' % (API_URL, urllib.urlencode(params))


if __name__ == '__main__':
    print '>>> 分账网关收款接口'
    demo_info()

    print '>>> 分账网关收款回调'
    demo_callback()

    print '>>> 分账网关退款接口'
    demo_refund()


