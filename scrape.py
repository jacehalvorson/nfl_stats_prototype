import requests
from bs4 import BeautifulSoup

# Global variables
# ----------------------------------------------------------------
htmlObject = None

BASE_URL = 'https://www.nfl.com/stats/player-stats/category/'
QBS_URL = 'https://www.nfl.com/stats/player-stats/'
# ----------------------------------------------------------------


# GET DATA FROM NEXT PAGE
# ----------------------------------------------------------------
# isTableRequested == True - Send a request to the next page and retrieve the stats
# isTableRequested == False - Just return the url of the next page
def getNextPage( isTableRequested ):
   global htmlObject
   
   if htmlObject == None:
      # If there is no table loaded, return error
      print( 'getNextPage called with no current page' )
      return None
   
   # Find the link of the 'Next Page' button
   footer = htmlObject.find( 'footer', 'd3-o-table__footer')
   if footer == None:
      return None
   url = footer.find_next( 'link' )[ 'href' ]
   if url == None:
      return None
   
   if isTableRequested == True:
      # Return the table found by this url
      return getPageFromURL( url )
   else:
      return url

# Appends the rows of the second table to the first table
def extendTableWithoutFirstRow( firstTable, secondTable ):
   firstTable.extend( secondTable[ 1: ] )
      
   return firstTable
# ----------------------------------------------------------------

# SEND GET REQUEST FOR RAW DATA DOWNLOAD AND PARSING
# ----------------------------------------------------------------
def getTableFromURL( url ):
   table = getPageFromURL( url )
   
   # Add on stats from all pages
   nextPageTable = getNextPage( True )
   while nextPageTable != None:
      if float( nextPageTable[ 1 ][ 1 ] ) > 0:
         table = extendTableWithoutFirstRow( table, nextPageTable )
         nextPageTable = getNextPage( True )
      else:
         # Unnecessary stats where the first row has 0
         break
   
   return table
   
def getPageFromURL( url ):
   # Retrieve data
   response = requests.get( url )
   
   global htmlObject
   htmlObject = BeautifulSoup( response.text, 'html.parser' )

   # Find the outer table
   table = htmlObject.find( 'table', 'd3-o-table' )

   # Extract the headers and stats
   headers = table.find_next( 'thead' )
   stats = table.find_next( 'tbody' )

   pageTable = [ [ ] ]
   for header in headers.select( '.header' ):
      pageTable[ 0 ].append( header.text )

   # Get a list of players (name + stats)
   players = stats.select( 'tr' )

   for rowIndex, player in enumerate( players ):
      # Add a new row for this player's stats
      pageTable.append( [ ] )
      
      # Add each stat to the new row
      for colIndex, stat in enumerate( player.find_all( 'td' ) ):
         if colIndex == 0:
            pageTable[ rowIndex+1 ].append( stat.text[ 1:-1 ] )
         else:
            pageTable[ rowIndex+1 ].append( stat.text )

   return pageTable
# ----------------------------------------------------------------