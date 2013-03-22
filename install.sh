#!/bin/zsh

PACKAGE_DIR="$HOME/Library/Application Support/Sublime Text 3/Packages/AutoCopyright"

rm *.pyc
[[ -d $PACKAGE_DIR ]] && rm -rf $PACKAGE_DIR
mkdir $PACKAGE_DIR
cp * $PACKAGE_DIR
