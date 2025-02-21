import json

import requests

from v2 import Tool_Sign
from v2.brazil.bean.AreaEnum import AreaEnum
from v2.brazil.bean.AreaEnum import CurrencyEnum
from v2.brazil.bean.Constants import Constants
from v2.brazil.bean.MerchantReq import MerchantReq
from v2.brazil.bean.MoneyReq import MoneyReq
from v2.brazil.bean.ReceiverReq import ReceiverReq
from v2.brazil.bean.TradePayoutReq import TradePayoutReq


def pay_out_request_demo(env="sandbox"):
    global merchant_id, merchant_secret, request_path
    if env == "production":
        # production
        merchant_id = Constants.merchantId
        merchant_secret = Constants.merchantSecret
        request_path = Constants.baseUrl + "/v2.0/disbursement/pay-out"
    if env == "sandbox":
        # sandbox
        merchant_id = Constants.merchantIdSandBox
        merchant_secret = Constants.merchantSecretSandBox
        request_path = Constants.baseUrlSandbox + "/v2.0/disbursement/pay-out"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)
    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    payment_method = "YES"
    cashAccount = "12345678909"
    ifscCode = "YES001022222"
    # moneyReq
    money_req = MoneyReq(CurrencyEnum.INR.name, 200)
    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)

    # payInReq
    pay_in_req = TradePayoutReq(payment_method, None, None, ifscCode, cashAccount, merchant_order_no[:32], purpose,
                                None,
                                None,
                                None, None, None, money_req, merchant_req, "notify url",
                                None, AreaEnum.INDIA.code)

    # jsonStr by json then minify
    json_data_minify = json.dumps(pay_in_req, default=lambda o: o.__dict__, separators=(',', ':'))
    print("json_data_minify=", json_data_minify)

    # build
    string_to_sign = timestamp + "|" + merchant_secret + "|" + json_data_minify
    print("string_to_sign=", string_to_sign)
    print("request_path=", request_path)

    # signature
    signature = Tool_Sign.sha256RsaSignature(Constants.privateKeyStr, string_to_sign)
    print("signature=", signature)

    # post
    # header
    headers = {
        'Content-Type': 'application/json',
        'X-TIMESTAMP': timestamp,
        'X-SIGNATURE': signature,
        'X-PARTNER-ID': merchant_id,

    }
    # POST request
    response = requests.post(request_path, data=json_data_minify, headers=headers)
    # Get response result
    result = response.json()
    print("response result=", result)


# run
pay_out_request_demo("sandbox")
