import json

import requests

from bean.AddressReq import AddressReq
from bean.AreaEnum import AreaEnum
from bean.AreaEnum import CurrencyEnum
from bean.Constants import Constants
from bean.ItemDetailReq import ItemDetailReq
from bean.MerchantReq import MerchantReq
from bean.MoneyReq import MoneyReq
from bean.PayerReq import PayerReq
from bean.ReceiverReq import ReceiverReq
from bean.TradePayInReq import TradePayInReq
from bean.TradeAdditionReq import  TradeAdditionReq
from v2 import Tool_Sign


def transaction_pay_in(env="sandbox"):
    global merchant_id, merchant_secret, request_path
    print("=====> PayIn transaction")
    if env == "sandbox":
         # sandbox
        merchant_id = Constants.merchantIdSandBox
        merchant_secret = Constants.merchantSecretSandBox
        request_path = Constants.baseUrlSandbox + "/v2.0/transaction/pay-in"
    if env == "production":
        # production
        merchant_id = Constants.merchantId
        merchant_secret = Constants.merchantSecret
        request_path = Constants.baseUrl + "/v2.0/transaction/pay-in"



    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # partner_id
    merchant_order_no = merchant_id.replace("sandbox-", "S") + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    # demo for INDONESIA, replace CurrencyEnum,payment_method to you what need
    payment_method = "W_DANA"
    # moneyReq
    money_req = MoneyReq(CurrencyEnum.IDR.name, 10000)

    # merchantReq
    merchant_req = MerchantReq(merchant_id, "your merchant name", None)

    addition_param = TradeAdditionReq("","","payer account no")

    # payerReq optional
    payer_req = PayerReq("abc", "abc.gt@gmail.com", "82-3473829260",
                         "abc, Jakarta", None)
    # receiverReq optional
    receiver_req = ReceiverReq("abc", "abc@mir.com", "82-3473233732",
                               "abc No.B1 Pluit", None)
    # itemDetailReq optional
    item_detail_req = ItemDetailReq("mac A1", 1, 10000)
    item_detail_req_list = [item_detail_req]

    # billingAddress optional
    billing_address = AddressReq("abc dasssss", "jakarta",
                                 "14450", "82-1234567789", "Indonesia")
    # shippingAddress optional
    shipping_address = AddressReq(" No.B1 Pluit", "jakarta",
                                  "14450", "82-1234567789", "Indonesia")


    # payInReq demo for INDONESIA, replace AreaEnum to you what need
    pay_in_req = TradePayInReq(payment_method, None, None, None, merchant_order_no[:32], purpose,
                               None,
                               addition_param,
                               None, None, None, money_req, merchant_req, "your notify url",
                               "redirect utl", AreaEnum.INDONESIA.code)

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
    print("response result =", result)


# run
transaction_pay_in("production")
