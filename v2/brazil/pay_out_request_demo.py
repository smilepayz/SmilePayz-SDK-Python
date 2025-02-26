import json

import requests

from v2.brazil import Tool_Sign
from v2.brazil.bean.AreaEnum import AreaEnum
from v2.brazil.bean.AreaEnum import CurrencyEnum
from v2.brazil.bean.Constants import Constants
from v2.brazil.bean.MerchantReq import MerchantReq
from v2.brazil.bean.MoneyReq import MoneyReq
from v2.brazil.bean.ReceiverReq import ReceiverReq
from v2.brazil.bean.TradePayoutReq import TradePayoutReq


def pay_out_request_demo(env, merchant_id, merchant_secret, private_key, payment_method, amount, cash_account,
                         tax_number):
    global request_path
    if env == "production":
        # production
        request_path = Constants.baseUrl + "/v2.0/disbursement/pay-out"
    if env == "sandbox":
        # sandbox
        request_path = Constants.baseUrlSandbox + "/v2.0/disbursement/pay-out"

    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)
    # partner_id
    merchant_order_no = merchant_id + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # moneyReq
    money_req = MoneyReq(CurrencyEnum.BRL.name, amount)
    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)

    # receiverReq
    receiver_req = ReceiverReq("abc", None, None,
                               tax_number)

    # payInReq
    pay_in_req = TradePayoutReq(payment_method, None, receiver_req, cash_account, merchant_order_no[:32], purpose,
                                None,
                                None,
                                None, None, None, money_req, merchant_req, "notify url",
                                None, AreaEnum.BRAZIL.code)

    # jsonStr by json then minify
    json_data_minify = json.dumps(pay_in_req, default=lambda o: o.__dict__, separators=(',', ':'))
    print("json_data_minify=", json_data_minify)

    # build
    string_to_sign = timestamp + "|" + merchant_secret + "|" + json_data_minify
    print("string_to_sign=", string_to_sign)
    print("request_path=", request_path)

    # signature
    signature = Tool_Sign.sha256RsaSignature(private_key, string_to_sign)
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
pay_out_request_demo("sandbox", "", "", "", "CPF",
                     100, "", "12345678909")
