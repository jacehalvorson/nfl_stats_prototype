# NFL Stats Available for Display and Download


## Instructions
This application requires Python version 3.0 or later along with the **customtkinter** extension. The extensions can be downloaded with the following commands:

### Linux/MacOS
```
pip install customtkinter
```

### Windows
```
pip3 install customtkinter
```

To run the program, clone this repository or download the files. In a directory with all of the *.py files, run:
```
python3 main.py
```

## Features

> Stat Viewing

Browse through pages of NFL data from every player with nonzero season stats in the selected category and year. Data can be requested and sorted by any of the following categories going back to 1993.
- Passing
- Rushing
- Receiving
- Fumbles
- Tackles
- Interceptions
- Field Goals
- Kickoffs
- Kickoff Returns
- Punting
- Punt Returns

> Data Export

Download a full table of the selected stats including every page that could be displayed. This data can be formatted to any of the following file formats.
- *.txt*
- *.csv*

## Potential improvements

> Alternating row colors

Rows should alternate color so lining up stats with players is easier

> Data Export to .xlsb

Only .txt and .csv are currently supported. The framework to check for the pyxll package is implemented but the file I/O is not

> Improved layout

Considering placing buttons above and below the stats instead of on the left side.

> Bugs with fixed table width

Too many attributes with wide enough names extends beyond the end of the window

> Different data source

Collecting data drom a different source would allow a full data download instead of loading one page at a time, which would significantly improve load times.