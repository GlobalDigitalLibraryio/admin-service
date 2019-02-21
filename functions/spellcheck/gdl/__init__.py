def response(status_code=200, headers=None, body=None, is_base_64_encoded=False):
    json_response = {
        'isBase64Encoded': is_base_64_encoded,
        'statusCode': status_code,
        'body': body
    }

    if headers:
        json_response['headers'] = headers

    return json_response

class SpellReport:
    def __init__(self, original):
        self.__original = original
        self.__suggestion = None
        self.__corrections = []

    @property
    def corrections(self):
        return self.__corrections

    @property
    def suggestion(self):
        return self.__suggestion if self.__suggestion else self.__original

    def contains_corrections(self):
        return not not self.__corrections

    def add_word_correction(self, original, correction):
        self.__corrections.append({
            'original': original,
            'correction': correction
        })

    def set_corrections(self, corrections):
        self.__corrections = corrections

    def add_suggestion(self, suggestion):
        self.__suggestion = suggestion