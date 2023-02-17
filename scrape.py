import requests
from bs4 import BeautifulSoup
import csv

# CONSTANTS
# ----------------------------------------------------------------
TXT = 0
CSV = 1
XLSB = 2

MAX_NAME_LENGTH = 15
# ----------------------------------------------------------------

# Global variables
# ----------------------------------------------------------------
htmlObject = None

BASE_URL = 'https://www.nfl.com/stats/player-stats/category/'
QBS_URL = 'https://www.nfl.com/stats/player-stats/'
fumbles2018_url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2018/post/all/defensiveforcedfumble/desc'
# url = 'https://www.nfl.com/stats/player-stats/category/passing/2022/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAooAAAAAAADEAlQAQgIhBb1JRbEFFL0JUTXlNREEwWkRVMUxUVXlOamN0TURReE15MDRaRE0yTFdFMVl6Tm1aRGM0TVdGaE1GWitQeFpiSWpJd01qSWlMQ0pTUlVjaUxDSXpNakF3TkdRMU5TMDFNalkzTFRBME1UTXRPR1F6TmkxaE5XTXpabVEzT0RGaFlUQWlYUT09APB____m8H___-ZInE-gq8Tjy5XTH6-5lDzOAAQ='
# ----------------------------------------------------------------


# GET DATA FROM NEXT PAGE - Assumes 
# ----------------------------------------------------------------
def getNextPageString( ):
   return formatString( getNextPageTable( ) )

def getNextPageTable( ):
   if htmlObject == None:
      # If there is no table loaded, default to the home page
      print( 'GetNextPageTable called before there is a current page' )
      return getTableFromURL( qbscurrent_url )
   
   # Find the link of the 'Next Page' button
   footer = htmlObject.find( 'footer', 'd3-o-table__footer')
   url = footer.find_next( 'link' )[ 'href' ]
   
   # Return the table found by this url
   return getTableFromURL( url )

# SEND GET REQUEST FOR RAW DATA DOWNLOAD AND PARSING
# ----------------------------------------------------------------
def getStringFromURL( url ):
   return formatString( getTableFromURL( url ) )

def getTableFromURL( url ):
   # Retrieve data
   response = requests.get( url )
   
   return extractTableFromResponse( response )
# ----------------------------------------------------------------

# GET TABLE FROM RESPONSE
# ----------------------------------------------------------------
def extractTableFromResponse( response ): 
   # Set global variable to hold this HTML parsing object
   global htmlObject
   htmlObject = BeautifulSoup( response.text, 'html.parser' )

   # Find the outer table
   table = htmlObject.find( 'table', 'd3-o-table' )

   # Extract the headers and stats
   headers = table.find_next( 'thead' )
   stats = table.find_next( 'tbody' )

   statMatrix = [ [ ] ]
   for i, header in enumerate( headers.select( '.header' ) ):
      statMatrix[ 0 ].append( header.text )

   # Get a list of players (name + stats)
   players = stats.select( 'tr ')

   for i, player in enumerate( players ):
      # Add a new row for this player's stats
      statMatrix.append( [ ] )
      
      # Add each stat to the new row
      for index, stat in enumerate( player.find_all( 'td' ) ):

         # TEMPORARY only collect 10 attributes
         # if index < 10:
            statMatrix[ i+1 ].append( stat.text )
            
   return statMatrix
# ----------------------------------------------------------------
      
# FORMATTING
# ----------------------------------------------------------------
def formatString( statMatrix ):
   formatString = ''

   for rowIndex, row in enumerate( statMatrix ):
      # Newline if it's not the first line
      formatString = ( formatString ) + '\n' if rowIndex > 0 else formatString
      
      for col, cell in enumerate( row ):
         if col == 0 and rowIndex == 1:
            # Add space between titles and stats
            formatString += '\n'
            
         if col == 0 and rowIndex != 0:
            # Player names come with a preceding space so remove it
            cellString = str( cell )[ 1: ]
         else:
            cellString = str( cell )
            
         if col == 14:
            # Only display 13 attributes
            break
         
         if col == 0 and len( cellString ) < MAX_NAME_LENGTH:
            succeedingWhitespace = ( ' ' * ( MAX_NAME_LENGTH - len( cellString ) ) ) + '\t'
         else:
            succeedingWhitespace = '\t'
            
         formatString += ( cellString + succeedingWhitespace )
      
   return formatString
# ----------------------------------------------------------------


# FILE WRITING
# ----------------------------------------------------------------
def writeToFile( fileType, string ):
   if fileType == TXT:
      with open( 'stats.txt', 'w' ) as file:
         file.write( string )
         file.write( '\n' )
         file.close( )
   elif fileType == CSV:
      print( 'Not yet implemented' )
   elif fileType == XLSB:
      print( 'Not yet implemented' )
   else:
      print( f'Invalid file type {fileType}' )
# ----------------------------------------------------------------