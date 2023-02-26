from gui import startGUI
from export import writeToFile
from scrape import getPageFromURL, QBS_URL

def main( ):
   # Retrieve default stats (passing 2022)
   table = getPageFromURL( QBS_URL )
   
   # table = readFromCSV( 'Passing2022.csv' )

   # Start GUI and pass in function pointers for buttons
   startGUI( table )
   
if __name__ == '__main__':
   main( )