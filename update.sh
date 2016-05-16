#!/bin/bash
# Download updated vim documentation and faq
set -e

echo Getting vim
if [[ -d vim ]]; then
    ( cd vim; git pull )
else
    git clone https://github.com/vim/vim
fi

echo Getting vim_faq
if [[ -d vim_faq ]]; then
    ( cd vim_faq; git pull )
else
    git clone https://github.com/chrisbra/vim_faq
fi

if ! [[ -d doc ]]; then
    echo making doc directory
    mkdir doc
fi

echo Copying files into doc directory
cp vim/runtime/doc/tags vim/runtime/doc/*.txt vim_faq/doc/vim_faq.txt doc

echo Writing tags.txt
awk 'BEGIN { ORS=" " } { print $1 }' doc/tags | fold -sw 78 > doc/tags.txt
