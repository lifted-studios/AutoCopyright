# Auto Copyright

A [Sublime Text 2](http://www.sublimetext.com/) plugin to automate adding the appropriate copyright text at the top of every file.

# Installation

## Manual installation

Go to the "Packages" directory (`Preferences` / `Browse Packages...`).  Then clone this repository:

    git clone git://github.com/lifted-studios/AutoCopyright

# Options

Edit the settings file (it should open automatically the first time you use an Auto Copyright command):

*   `"owner": ""`

    You need to enter the text you want to show up as the copyright owner.

# Usage

Two functions will show up in the Command Palette under "Auto Copyright".  Additionally, the Update Copyright command will be called just before any file is saved.

## Insert Copyright

Adds the copyright text to the beginning of the file.  It will add itself after a shebang line, if any.

## Update Copyright

Updates the copyright text already present in the file, but only if the text matches, including the copyright owner name except for the year.  It will update the copyright year to include all years between the original year and this one.

# Information

Source: https://github.com/lifted-studios/AutoCopyright

Authors: [Lee Dohm](https://github.com/lee-dohm/), [Lifted Studios](https://github.com/lifted-studios/)
