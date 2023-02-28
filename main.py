from gui import startGUI
from export import writeToFile
from scrape import getPageFromURL, QBS_URL

def main( ):
   # Retrieve default stats (passing 2022)
   table = getPageFromURL( QBS_URL )
   
   # table = readFromCSV( 'Passing2022.csv' )

   # table = [
   #          [0, 0, 0, 0,],
   #          [1, 1, 1, 1,],
   #          [2, 2, 2, 2,],
   #          [3, 3, 3, 3,],
   #          [4, 4, 4, 4,],
   #          [5, 5, 5, 5,],
   #          [6, 6, 6, 6,],
   #          [7, 7, 7, 7,],
   #         ]

   # Start GUI and pass in function pointers for buttons
   startGUI( table )
   
if __name__ == '__main__':
   main( )