from scrape import *
from gui import *

def nextPageCallback( ):
   updateStats( getNextPageString( ) )
   
def loadCallback( categorySelected, yearSelected ):
   # Find the necessary strings to assemble the url
   if categorySelected == 'Passing':
      category = 'passing'
      sortBy = 'passingyards'
   elif categorySelected == 'Rushing':
      category = 'rushing'
      sortBy = 'rushingyards'
   elif categorySelected == 'Receiving':
      category = 'receiving'
      sortBy = 'receivingreceptions'
   elif categorySelected == 'Fumbles':
      category = 'fumbles'
      sortBy = 'defensiveforcedfumble'
   elif categorySelected == 'Tackles':
      category = 'tackles'
      sortBy = 'defensivecombinetackles'
   elif categorySelected == 'Interceptions':
      category = 'interceptions'
      sortBy = 'defensiveinterceptions'
   elif categorySelected == 'Field Goals':
      category = 'field-goals'
      sortBy = 'kickingfgmade'
   elif categorySelected == 'Kickoffs':
      category = 'kickoffs'
      sortBy = 'kickofftotal'
   elif categorySelected == 'Kickoff Returns':
      category = 'kickoff-returns'
      sortBy = 'kickreturnsaverageyards'
   elif categorySelected == 'Punting':
      category = 'punts'
      sortBy = 'puntingaverageyards'
   elif categorySelected == 'Punt Returns':
      category = 'punt-returns'
      sortBy = 'puntreturnsaverageyards'
   else:
      print( f'Unsupported category {categorySelected}' )
      
   # Build the url for the request
   requestedUrl = BASE_URL + category + '/' + str( yearSelected ) + '/post/all/' + sortBy + '/desc'
   
   # Update the displayed stats
   updateStats( getStringFromURL( requestedUrl ) )

def main( ):
   # Retrieve default stats (passing 2022)
   string = getStringFromURL( QBS_URL )

   # Start GUI and pass in function pointers for buttons
   startGUI( string, placeholderCommand, nextPageCallback, loadCallback )
   
if __name__ == '__main__':
   main( )