# wikidata
wikidata.org

## Download
```
STORE_PATH=data
DATA_URL=http://download.wikipedia.com/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2

cd $STORE_PATH
wget $DATA_URL
```

## Extract articles
```
WikiExtractor.py -b 5000M \
    -o data/zhwiki-latest-pages-articles.extracted \
    data/zhwiki-latest-pages-articles.xml.bz2
```

## 繁体转简体
```
opencc -i data/zhwiki-latest-pages-articles.extracted/AA/wiki_00  \
    -o data/zhwiki-latest-pages-articles.0620.chs \
    -c t2s.json
```

Download [t2s.json](https://raw.githubusercontent.com/BYVoid/OpenCC/master/data/config/t2s.json).

到此为止，已经完成了大部分繁简转换工作。


## 其他情况处理

1) 维基百科使用的繁简转换方法是以词表为准，外加人工修正。人工修正之后的文字是这种格式，多数是为了解决各地术语名称不同的问题：

> 他的主要成就包括Emacs及後來的GNU Emacs，GNU C 編譯器及-{zh-hant:GNU 除錯器;zh-hans:GDB 调试器}-。

对付这种可以简单的使用正则表达式来解决。一般简体中文的限定词是zh-hans或zh-cn。

2) 由于Wikipedia Extractor抽取正文时，会将有特殊标记的外文直接剔除，最后形成类似这样的正文：

> 西方语言中“数学”（；）一词源自于古希腊语的（）

虽然上面这句话是读不通的，但鉴于这种句子对我要处理的问题影响不大，就暂且忽略了。最后再将「」『』这些符号替换成引号，顺便删除空括号。


```
python2 fix_special_symbols.py data/zhwiki-latest-pages-articles.0620.chs
```

程序执行结束，输出: **data/zhwiki-latest-pages-articles.0620.chs.normalized**。

## 浏览文件

```
head data/zhwiki-latest-pages-articles.0620.chs.normalized
```

## 分词

* 执行脚本

```
export PYTHONIOENCODING="UTF-8"
python3 wordseg.py > data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg
```

## word2vec
[word2vec](https://code.google.com/archive/p/word2vec)官方的实现。
```
./word2vec_c_format_train.sh
```

### Usage of word2vec model

* word2vec cli

```
distance, compute-accuracy, word-analogy
```

* python

```
python3 word2vec_gensim_similarity.py
```

## TF-IDF

* plain code

train

```python
python3 tfidf_plain.py
```

After running, dump **words**, **weights** and **idf** into pickle file.

* adv version in [sklearn](http://scikit-learn.org/)

现在会有稀疏矩阵的问题，解决方案是使用限定的词汇表。

```python
python3 tfidf_sklearn.py
```

## 关联项目

### [Synonyms](https://github.com/huyingxi/Synonyms)
中文近义词库，Synonyms使用wikidata-corpus训练的词向量生成近义词表。

## references
http://licstar.net/archives/328
http://licstar.net/archives/tag/wikipedia-extractor
