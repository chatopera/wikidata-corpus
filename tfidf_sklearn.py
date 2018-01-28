# -*- coding: utf-8 -*-
import os
curdir = os.path.dirname(os.path.abspath(__file__))
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

'''
http://blog.csdn.net/liuxuejiang158blog/article/details/31360765
https://stackoverflow.com/questions/29788047/keep-tfidf-result-for-predicting-new-content-using-scikit-for-python
http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
'''

corpus_data_path = "%s/data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg" % curdir
feature_dump_path = "%s/data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg.features" % curdir
test_dump_path = "%s/data/sklearn.test.features" % curdir


def file_len(full_path):
    """ Count number of lines in a file."""
    f = open(full_path)
    nr_of_lines = sum(1 for line in f)
    f.close()
    return nr_of_lines


def tokenizer(text):
    words = text.split(" ")
    return words


def train_model(corpus, model_path=test_dump_path):
    # train model
    # vectorizer = CountVectorizer(tokenizer=tokenizer)
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    texts = vectorizer.fit_transform(corpus)
    tfidf = transformer.fit_transform(texts)

    # save model
    pickle.dump(vectorizer.vocabulary_, open(model_path, "wb"))


def parse_tfidf_result(words, weights):
    '''
    parse results
    '''
    result = []
    for i, v in sorted(enumerate(words),
                       key=lambda item: -weights[0][item[0]]):
        if(weights[0][i] > 0):
            result.append(dict({
                "fid": i,  # feature id
                "word": v,  # word
                "score": weights[0][i]
            }))

    return result


T = None


def get_tfidf_result(model_path, text):
    '''
    get tf-idf results
    '''
    # optimize by only loading once
    global T
    if not T:
        print("init model ...")
        T = CountVectorizer(
            decode_error="replace",
            vocabulary=pickle.load(
                open(
                    model_path,
                    "rb")))

    t = TfidfTransformer()
    tfidf = t.fit_transform(
        T.transform([text]))

    words = T.get_feature_names()  # 获取词袋模型中的所有词语

    # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    weights = tfidf.toarray()

    # for j in range(len(words)):
    #     print(words[j], weights[0][j])

    return words, weights


def test_train_model():
    '''
    demo how to use sklearn tf-idf
    '''
    corpus = ["我 来到 清华大学",  # 第一类文本切词后的结果，词之间以空格隔开
              "他 来到 了 北京 杭研 大厦",  # 第二类文本的切词结果
              "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
              "我 爱 天安门"]
    train_model(corpus, model_path=test_dump_path)
    words, weights = get_tfidf_result(test_dump_path, "我 来到 了 北京 天安门")
    return parse_tfidf_result(words, weights)


def train_wikidata():
    texts = []
    with tqdm(total=file_len(corpus_data_path)) as pbar:
        pbar.set_description("Parsing texts ...")
        with open(corpus_data_path, "r") as f:
            for x in f:
                t = [y for y in x.strip().split(' ') if y]
                if len(t) > 20:
                    texts.append(' '.join(t))  # only append big text as doc
                pbar.update(1)

    train_model(texts, feature_dump_path)
    print("save model to %s" % feature_dump_path)
    print("done.")


def test_wikidata_model():
    '''
    demo how to use sklearn tf-idf
    '''
    words, weights = get_tfidf_result(
        feature_dump_path, "我们 再次 敦促 日方 以史为鉴 ，重视 国际 社会 的 关切，以 负责任 的 态度 妥善 处理 有关问题")
    print(parse_tfidf_result(words, weights))

    words, weights = get_tfidf_result(
        feature_dump_path, "我们 已多次 正告 日方 ，如果 不能 切实 正视 和 深刻 反省 历史")
    print(parse_tfidf_result(words, weights))


if __name__ == '__main__':
    # train_wikidata()
    # print(test_train_model())
    test_wikidata_model()
