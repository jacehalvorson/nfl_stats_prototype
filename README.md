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

Browse through pages of NFL data from every player with nonzero season stats in the selected category and year. Data can be requested back to 1993 from any of the following  categories.
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

> Data Export *NOT YET IMPLEMENTED*

Download a full table of the selected stats including every page that could be displayed. This data can be formatted to any of the following file formats.
- *.txt*
- *.csv*
- *.xlsb*

## Planned improvements

> Sorting by attribute
Each attribute is displayed as a button so it can be clicked to sort players from all pages based on a single stat and remain on the same page. If the current page is past the new number of pages, the last page should be selected.

> Load speed
Currently all pages load at once allowing for quick page swapping. This slows down load times and it can be avoided by displaying the first page as soon as it's ready and then loading in the rest of the data. The following buttons should be disabled while the rest of the pages load.
- Previous page
- Next page
- Load
- Download
- Sorting

> Data Export
There is an implementation for writing to .txt files but it hasn't been implemented in an accessible way. Also need to write to .csv and .xlsb files.