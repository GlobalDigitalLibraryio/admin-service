from gdl.spellcheck import Spellcheck


spellcheck = Spellcheck()


def is_warmup(event):
    return event.get('source', '') == "serverless-plugin-warmup"


def main(event, context):
    if is_warmup(event):
        return "Warm"

    return spellcheck.main(event)

