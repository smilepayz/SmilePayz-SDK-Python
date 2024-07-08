import json
import time

import requests

from v2 import Tool_Sign
from bean.AddressReq import AddressReq
from bean.AreaEnum import AreaEnum
from bean.AreaEnum import CurrencyEnum
from bean.ItemDetailReq import ItemDetailReq
from bean.MerchantReq import MerchantReq
from bean.MoneyReq import MoneyReq
from bean.PayerReq import PayerReq
from bean.ReceiverReq import ReceiverReq
from bean.TradeAdditionReq import TradeAdditionReq
from bean.TradePayoutReq import TradePayoutReq
from bean.Constants import Constants


def pay_out_request_demo(env="sandbox"):
    if env == "pro":
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
    merchant_order_no = merchant_id.replace("sandbox-", "S") + Tool_Sign.generate_32bit_uuid()
    purpose = "Purpose For Transaction from python SDK"

    payment_method = "YES"  # bank code  for india
    cashAccount = "1234566778"  # cah account for Yes bank
    # moneyReq
    money_req = MoneyReq(CurrencyEnum.INR.name, 200)
    # merchantReq
    merchant_req = MerchantReq(merchant_id, None, None)

    # payerReq optional
    payer_req = PayerReq("Jef-fer", "jef.gt@gmail.com", "82-3473829260",
                         "Jalan Pantai Mutiara TG6, Pluit, Jakarta", None)
    # receiverReq optional
    receiver_req = ReceiverReq("Viva in", "Viva@mir.com", "82-3473233732",
                               "Jl. Pluit Karang Ayu 1 No.B1 Pluit", None)
    # itemDetailReq optional
    item_detail_req = ItemDetailReq("mac A1", 1, 10000)
    item_detail_req_list = [item_detail_req]

    # billingAddress optional
    billing_address = AddressReq("Jl. Pluit Karang Ayu 1 No.B1 Pluit", "jakarta",
                                 "14450", "82-3473233732", "Indonesia")
    # shippingAddress optional
    shipping_address = AddressReq("Jl. Pluit Karang Ayu 1 No.B1 Pluit", "jakarta",
                                  "14450", "82-3473233732", "Indonesia")
    addition_req = TradeAdditionReq("YES000001", None, None);
    # payInReq,  None fields are optional
    pay_in_req = TradePayoutReq(payment_method, None, None, cashAccount, merchant_order_no[:32], purpose,
                                None,
                                addition_req,
                                None, None, None, money_req, merchant_req, None,
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