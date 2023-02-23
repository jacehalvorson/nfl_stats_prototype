import csv

MAX_NAME_LENGTH = 15

# FORMATTING TO STRING
# ----------------------------------------------------------------
def formatString( statMatrix ):
   if statMatrix == None:
      print( 'None' )
      return None
   
   formatString = ''

   for rowIndex, row in enumerate( statMatrix ):
      # Newline if it's not the first line
      formatString = ( formatString ) + '\n' if rowIndex > 0 else formatString
      
      for col, cell in enumerate( row ):
         if col == 0 and rowIndex == 1:
            # Add space between titles and stats
            formatString += '\n'
            
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
def writeToFile( fileType, fileName, table ):
   if fileName == ' ':
      return False
   
   with open( fileName + fileType, 'w' ) as file:
      if fileType == '.txt':
         file.write( formatString( table ) )
         file.write( '\n' )
      elif fileType == '.csv':
         writer = csv.writer( file )
         writer.writerows( table )
      elif fileType == '.xlsb':
         print( 'Not implemented' )
      else:
         print( f'Invalid file type {fileType}' )
         return
   
      file.close( )
      return True
   
   return False
# ----------------------------------------------------------------