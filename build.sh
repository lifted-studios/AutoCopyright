#!/bin/zsh

package_dir="$HOME/Library/Application Support/Sublime Text 2/Packages/SublimeCopyright" 
[ -d $package_dir ] || mkdir $package_dir
cp *.py $package_dir
