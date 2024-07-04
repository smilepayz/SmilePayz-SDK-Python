import json

import requests

import Tool_Sign
from bean.BalanceInquiryReq import BalanceInquiryReq
from bean.Constants import Constants


def balance_inquiry():
    print("=====> balance_inquiry")

    # production
    # merchant_id = Constants.merchantId
    # merchant_secret = Constants.merchantSecret
    # request_path = Constants.baseUrl + "/v2.0/inquiry-balance"

    # sandbox
    merchant_id = Constants.merchantIdSandBox
    merchant_secret = Constants.merchantSecretSandBox
    request_path = Constants.baseUrlSandbox + "/v2.0/inquiry-balance"


    # transaction time
    timestamp = Tool_Sign.get_formatted_datetime('Asia/Bangkok')
    print("timestamp:" + timestamp)

    # payInReq,  None fields are optional
    balance_inquiry = BalanceInquiryReq(Tool_Sign.generate_32bit_uuid(), "21220030202403071031", ["balance"])

    # jsonStr by json then minify
    json_data_minify = json.dumps(balance_inquiry, default=lambda o: o.__dict__, separators=(',', ':'))
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
    print(result)


# run
balance_inquiry()
