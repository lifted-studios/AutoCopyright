#!/bin/zsh

# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

package_dir="$HOME/Library/Application Support/Sublime Text 2/Packages/SublimeCopyright" 
[ -d $package_dir ] || mkdir $package_dir
cp *.py $package_dir
cp *.sublime-* $package_dir
