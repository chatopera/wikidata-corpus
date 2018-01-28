#! /bin/bash 
###########################################
#
###########################################

# constants
baseDir=$(cd `dirname "$0"`;pwd)
APP_HOME=$baseDir
W2V_HOME=~/git/word2vec # get word2vec from https://github.com/Samurais/word2vec
export PATH=$PATH:$W2V_HOME/src
INPUT=data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg
OUTPUT=$INPUT.w2v
OUTPUT_VOCAB=$OUTPUT.vocab

# functions

# main 
[ -z "${BASH_SOURCE[0]}" -o "${BASH_SOURCE[0]}" = "$0" ] || return
cd $baseDir
echo "train word2vec with " $INPUT
set -x
word2vec -train $INPUT \
    -output $OUTPUT \
    -threads 10 \
    -size 100 \
    -min-count 100 \
    -window 5 \
    -sample 1e-5 \
    -negative 10 \
    -hs 0 \
    -binary 1 \
    -cbow 1 \
    -iter 100 \
    -save-vocab $OUTPUT_VOCAB
