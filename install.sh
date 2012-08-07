#!/bin/bash

# 
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
# 

PACKAGE_DIR="$HOME/Library/Application Support/Sublime Text 2/Packages/SublimeCopyright" 
[[ -d "$PACKAGE_DIR" ]] || mkdir "$PACKAGE_DIR"
cp *.py "$PACKAGE_DIR"
cp *.sublime-* "$PACKAGE_DIR"
