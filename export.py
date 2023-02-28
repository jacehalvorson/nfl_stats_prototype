import csv
import importlib.util

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
   if fileName == '' or len( table ) == 0:
      return False
   
   with open( fileName + fileType, 'w' ) as file:
      if fileType == '.txt':
         file.write( formatString( table ) )
         file.write( '\n' )
         
      elif fileType == '.csv':
         writer = csv.writer( file )
         writer.writerows( table )
         
      elif fileType == '.xlsx':
         # Make sure the xlsxwrite package is installed, otherwise return error
         checkPackageInstalled = 'xlsxwriter'
         if importlib.util.find_spec( checkPackageInstalled ) is None:
            print( f'You need to install {checkPackageInstalled} to write to .xlsx files. See README.md for more details or run this command to install it:\npip install {checkPackageInstalled}' )
            return False

         print( 'Writing to Excel' )
         import xlsxwriter         
         workbook = xlsxwriter.Workbook( fileName + fileType )
         
         worksheet = workbook.add_worksheet( )
         
         for rowIndex, row in enumerate( table ):
            for colIndex in range( len( row ) ):
               worksheet.write( rowIndex, colIndex, row[ colIndex ] )
         
         workbook.close( )

      else:
         print( f'Invalid file type {fileType}' )
         return
   
      file.close( )
      return True
   
   return False
# ----------------------------------------------------------------

def readFromCSV( filename ):
   with open( filename, 'r' ) as file:
      reader = csv.reader( file )
      table = [ ]
      
      for row in reader:
         table.append( row )
      
   return table