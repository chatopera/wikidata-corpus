from gensim import models, corpora
import os
curdir = os.path.dirname(os.path.abspath(__file__))

model_c_format_path = "%s/data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg.w2v"
model_c_format_vocab = "%s/data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg.w2v.vocab.gensim.bak"


def load_word2vec_model(path, binary=False):
    # Load Google's pre-trained Word2Vec model.
    # model's api
    # https://radimrehurek.com/gensim/models/keyedvectors.html
    model = models.KeyedVectors.load_word2vec_format(path, binary=binary)
    print("Model %s loaded." % path)
    return model


def load_dictionary(vocab_path):
    '''
    FIXME 推测这种方式并不正确，c format的文件，zhwiki-latest-pages-articles.0620.chs.normalized.wordseg.w2v.vocab
    里面的频率，统计的是每个词出现在语料中的次数，而不是出现在了多少个文档中。
    也就是从 word2vec_c_format_build_dict.sh 生成的字典，不是gensim需要的格式。
    '''
    vocabulary = {}  # TODO, read vocab from vocab_path
    dictionary = corpora.Dictionary.load_from_text(vocab_path)
    return dictionary


def load_tfidf_model():
    dictionary = load_dictionary(model_c_format_vocab % curdir)
    tfidf_model = models.tfidfmodel.TfidfModel(dictionary=dictionary)
    return tfidf_model


def test_tfidf_model():
    tfidf_model = load_tfidf_model()
    some_doc = "周冬雨 凭借 在 影片 《七月与安生》 中 的 精湛 演技 ， 获封 本届 电影节 熊猫奖 最佳女主角 称号 。 “ 感谢 金砖电影节 ，给 我们 这么多 跨国 交流 和 学习 的 机会 。 ” 手捧 奖杯 的 周冬雨 说 ， 她 希望 能 带来 更多 中国 好电影 给 观众"
    print(tfidf_model[(1, 2), (2, 1)])


if __name__ == '__main__':
    word_vectors = load_word2vec_model(model_c_format_path % curdir)
    print(word_vectors.similarity('北京', '哈尔滨'))
