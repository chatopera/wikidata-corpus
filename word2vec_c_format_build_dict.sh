#! /bin/bash 
###########################################
#
###########################################

# constants
baseDir=$(cd `dirname "$0"`;pwd)
vocab_path=data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg.w2v.vocab
output=$vocab_path.gensim

# functions
function write_to_dict(){
    echo -e "$1\t$2\t$3" >> $output
}

# main 
[ -z "${BASH_SOURCE[0]}" -o "${BASH_SOURCE[0]}" = "$0" ] || return
index=1
while IFS='\t' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"
    word=`echo $line | awk '{ print $1}'`
    freq=`echo $line | awk '{ print $2}'`
    
    echo "word id:" $index ", word:" $word ", freq:" $freq
    write_to_dict $index $word $freq

    index=$((index+1))
    # break; # for test
done < "$vocab_path"
