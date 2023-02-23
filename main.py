from gui import *

def main( ):
   # Retrieve default stats (passing 2022)
   table = getPageFromURL( QBS_URL )
   # table = [ ['A', 'B', 'C', 'D'], \
   #           [0, 1, 2, 3], \
   #           [1, 2, 3, 4], \
   #           [2, 3, 4, 0], \
   #           [3, 4, 0, 1], ]

   # Start GUI and pass in function pointers for buttons
   startGUI( table )
   
if __name__ == '__main__':
   main( )