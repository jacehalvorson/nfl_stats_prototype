from gui import *

def main( ):
   # Retrieve default stats (passing 2022)
   table = getTableFromURL( QBS_URL )

   # Start GUI and pass in function pointers for buttons
   startGUI( table )
   
if __name__ == '__main__':
   main( )