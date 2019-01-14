def response(status_code=200, headers=None, body=None, is_base_64_encoded=False):
    json_response = {
        'isBase64Encoded': is_base_64_encoded,
        'statusCode': status_code,
        'body': body
    }

    if headers:
        json_response['headers'] = headers

    return json_response
