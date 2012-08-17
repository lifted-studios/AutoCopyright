#!/bin/zsh

PACKAGE_DIR="$HOME/Library/Application Support/Sublime Text 2/Packages/AutoCopyright"

[[ -d $PACKAGE_DIR ]] && rm -rf $PACKAGE_DIR
mkdir $PACKAGE_DIR
cp * $PACKAGE_DIR
