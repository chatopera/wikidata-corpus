# encoding: utf-8

import requests
import json
import os
curdir = os.path.dirname(os.path.abspath(__file__))

# config
URL = 'http://corsair:3007/api/v1'
SEGWORD_TYPE = "nostopword"
INPUT_DATA = "%s/data/zhwiki-latest-pages-articles.0620.chs.normalized" % curdir


def rest_post(endpoint, data):
    headers = {"Accept": "application/json",
               "Content-Type": "application/json"}
    # call get service with headers and params
    response = requests.post(
        '%s%s' %
        (URL, endpoint), data=json.dumps(data), headers=headers)

    return response.json()


def segment_sentence(sentence, type=SEGWORD_TYPE):
    result = rest_post('/tokenizer', data=dict({
        "type": type,
        "content": sentence
    }))
    concat = []
    if(result["status"] == "success"):
        [concat.append(data["word"]) for data in result["data"]]
    else:
        raise "fail to get response"

    return " ".join(concat)


def load_all_data():
    with open(INPUT_DATA, "r", encoding="utf-8") as infile:
        for line in infile:
            yield line


if __name__ == "__main__":
    for x in load_all_data():
        try:
            print(segment_sentence(x))
        except BaseException:
            pass
