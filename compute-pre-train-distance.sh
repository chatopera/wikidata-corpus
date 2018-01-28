#! /bin/bash 
###########################################
#
###########################################

# constants
baseDir=$(cd `dirname "$0"`;pwd)
V=$baseDir/pre-trained/zhwiki-latest-pages-articles.0620/chs.normalized.wordseg.w2v.vocab
M=$baseDir/pre-trained/zhwiki-latest-pages-articles.0620/chs.normalized.wordseg.w2v
# functions

# main 
[ -z "${BASH_SOURCE[0]}" -o "${BASH_SOURCE[0]}" = "$0" ] || return
cd $baseDir
while IFS= read -r var
do
  for x in $var; do
    echo $x | distance $M
    echo "\n"
    break
  done
done < "$V"
