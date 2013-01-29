# Auto Copyright

A [Sublime Text 2](http://www.sublimetext.com/) plugin to automate adding the appropriate copyright text at the top of every file.

# Compatibility

AutoCopyright is only compatible with Sublime Text 2 at this time.  We have plans for upgrading it to support Sublime Text 3 when possible.

# Installation

## Package Control

The awesome Package Control package is a great way to easily install and manage Sublime Text 2 packages.

1. Install [Package Control](http://wbond.net/sublime_packages/package_control)
1. Press Control/Command+Shift+P to bring up the command palette
1. Type PCIP (for Package Control: Install Package) and press Return
1. Type AutoCopyright and press Return

## Manual installation

Go to the "Packages" directory (`Preferences` / `Browse Packages...`).  Then clone this repository:

    git clone git://github.com/lifted-studios/AutoCopyright

# Options

Edit the settings file (it should open automatically the first time you use an Auto Copyright command):

*   `"copyright message": "Copyright (c) %y by %o.  All Rights Reserved."`

    This is the copyright message the plugin will use.  `%y` is replaced by the year or year range.  `%o` is replaced by the selected owner text.

*   `"languages use line comments": ["Ruby"]`

    This is the list of languages that will use line comments for the copyright comment block even though block comments are available in the language.

*   `"owner": [""]`

    You need to enter the text you want to show up as the primary copyright owner.  If you have multiple copyright owners, then enter them as an array.

*   `"padding": 1`

    This is the amount of padding around the line that contains the copyright.  The default is one line above and below the copyright line.

# Usage

Two functions will show up in the Command Palette under "Auto Copyright".  Additionally, the Update Copyright command will automatically be called just before any file is saved.

## Insert Copyright

Adds the copyright text to the beginning of the file.  It will add itself after a [shebang line](http://en.wikipedia.org/wiki/Shebang), if any.  When the command is triggered, if there are multiple copyright owners configured in settings, it will pop up a list and ask which one to use.

## Update Copyright

Updates the copyright text already present in the file, but only if the text matches, including the copyright owner name except for the year.  It will update the copyright year to include all years between the original year and this one.  The command will update the copyright text for any of the configured owner texts.

# Information

Source: https://github.com/lifted-studios/AutoCopyright

Authors: [Lee Dohm](https://github.com/lee-dohm/), [Lifted Studios](https://github.com/lifted-studios/)
