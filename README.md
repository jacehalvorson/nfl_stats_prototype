# NFL Stats Available for Display and Download


## Instructions
This application requires Python version 3.0 or later along with extensions **tkinter** and **customtkinter**. The extensions can be downloaded with the following commands:

### Linux/MacOS
```
pip install tk
pip install customtkinter
```

### Windows
```
pip3 install tk
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

> Sorting by attribute backwards
Once sorted by a particular attribute, one should be able to click the button again to reverse the order. Also ties should be resolved by player name

> Data Export to .xlsb
Only .txt and .csv are currently supported. This addition may require more packages to run the program.

> Improved layout
Considering placing buttons above and below the stats instead of on the left side.

> Different data source
Collecting data drom a different source would allow a full data download instead of loading one page at a time, which would significantly improve load times.