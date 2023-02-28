import importlib.util

checkPackageInstalled = 'customtkinter'
if importlib.util.find_spec( checkPackageInstalled ) is None:
   print( f'You need to install {checkPackageInstalled} to start the GUI. See README.md for more details or run this command to install it:\npip install {checkPackageInstalled}' )
   exit( )
else:
   import customtkinter

from scrape import *
from export import *
from sort import *
from math import floor


# Constants
screenWidth = 1200
screenHeight = 750
buttonWidth = 120
rowsDisplayed = 20

# Page tracker variables
currentStats = None
currentPage = 1
numberOfPages = 1
buttonsActive = False

# Sort tracker variables
DESCENDING = 0
ASCENDING = 1
currentSortCol = 1 # Default to sort by first stat (0 is player name)
currentSortOrder = DESCENDING

# GUI elements
tableEntries = [ ]
columnFrames = [ ]
statsFrameColor = 'gray90'

# Dropdown options
# ----------------------------------------------------------------
fileTypes = [
   '.csv',
   '.txt'
]
fileTypeSelected = fileTypes[ 0 ]

years = [ str( 2022 - i ) for i in range( 30 ) ]
yearSelected = years[ 0 ]

categories = [
   'Passing',
   'Rushing',
   'Receiving',
   'Fumbles',
   'Tackles',
   'Interceptions',
   'Field Goals',
   'Kickoffs',
   'Kickoff Returns',
   'Punting',
   'Punt Returns'
]
categorySelected = categories[ 0 ]
# ----------------------------------------------------------------
   
def fileTypeDropdownCallback( choice ):
   global fileTypeSelected
   fileTypeSelected = choice

def yearDropdownCallback( choice ):
   global yearSelected
   yearSelected = choice

def categoryDropdownCallback( choice ):
   global categorySelected
   categorySelected = choice

def pageChangeCallback( pageChange ):
   global currentPage
   global currentStats
   global numberOfPages
   
   if buttonsActive == False:
      return
   
   newPage = currentPage + pageChange
   if newPage < 1 or newPage > numberOfPages:
      # Can't go outside of 1 and max page
      return
   
   currentPage += pageChange
   pageDisplay.configure( text=( str( currentPage ) + ' of ' + str( numberOfPages ) ) )

   updateStats( currentStats, currentPage )

def loadCallback( categorySelected, yearSelected, window ):
   if buttonsActive == False:
      return
   
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
   
   displayPage( getPageFromURL( requestedUrl ) )
   window.after( 750, loadPages )

def downloadCallback( fileNameEntry ):
   global fileTypeSelected
   global currentStats

   if buttonsActive == False or fileTypeSelected not in fileTypes:
      return
   
   print( f'Downloading {fileNameSelected.get( )}{fileTypeSelected}' )
   
   if writeToFile( fileTypeSelected, fileNameSelected.get( ), currentStats ) == True:
      print( 'Download succeeded' )
   else:
      print( 'Download failed' )

def sortCallback( sortByCol ):
   global currentStats
   global currentSortCol
   global currentSortOrder
   
   if buttonsActive == False:
      return
      
   if sortByCol == currentSortCol:
      # Table is already sorted by this column, reverse order
      currentSortOrder = ASCENDING if currentSortOrder == DESCENDING else DESCENDING
   else:
      # Update global variables, default to descending order
      currentSortCol = sortByCol
      currentSortOrder = DESCENDING
      
   # newTable will be built to replace currentStats, first put labels in
   newTable = [ currentStats[ 0 ] ]
   
   # Get the sorted data to newTable (don't include labels when sorting)
   stats = mergeSort( currentStats[ 1: ], sortByCol, 0 )
   if currentSortOrder == DESCENDING:
      stats.reverse( )
   newTable.extend( stats )

   # Update the screen
   currentStats = newTable
   updateStats( currentStats, currentPage )

def displayPage( firstPage ):
   global currentStats
   global currentPage
   global buttonsActive
   global currentSortCol
   global currentSortOrder
   
   # Disable buttons while data laods
   buttonsActive = False
   
   currentPage = 1
   currentSortCol = 1
   currentSortOrder = DESCENDING
   updateStats( firstPage, currentPage )

   pageDisplay.configure( text='1 of 1' )
   fileNameSelected.set( categorySelected + str( yearSelected ) )
   
   currentStats = firstPage
   
def loadPages( ):
   global currentStats
   global numberOfPages
   global rowsDisplayed
   global buttonsActive
   
   # Load the rest of the data
   nextPageURL = getNextPage( False )
   if nextPageURL != None:
      currentStats = extendTableWithoutFirstRow( currentStats, getTableFromURL( nextPageURL ) )
      
      numberOfPages = int( floor( len( currentStats ) / rowsDisplayed ) )
      pageDisplay.configure( text=( '1 of ' + str( numberOfPages ) ) )
         
   # Re-enable buttons now that pages are loaded
   buttonsActive = True

def resizeWindow( ):
   global screenHeight
   global screenWidth
   global root
   global statsFrame
   global selectionFrame
   
   # Set screen width and height to fit the frame
   screenWidth = statsFrame.winfo_width( ) + selectionFrame.winfo_width( ) + 30
   screenHeight = statsFrame.winfo_height( ) + 24
   root.geometry( str( screenWidth ) + 'x' + str( screenHeight ) )

def initStatsFrame( table, statsFrame ):
   global currentSortCol
   global tableEntries
   global columnFrames
   global rowNumbers
   global statsFrameColor
   statsFrameColor = statsFrame.cget( 'fg_color' )
   
   # Initialize lists for the objects
   columnFrames = [ ]
   tableEntries = [ ]
   for rowIndex in range( len( table ) ):
      tableEntries.append( [ ] )
   
   # Make objects and put them on the screen
   # Make a frame for the first column
   columnFrame = customtkinter.CTkFrame( master=statsFrame, width=30, fg_color=statsFrameColor )
   columnFrame.grid( row=0, column=0, pady=( 40, 0 ), padx=4 )
   rowNumbers = [ ]
   for rowIndex in range( 1, rowsDisplayed+1 ):
      if rowIndex % 2 == 0:
         foregroundColor = 'gray80'
      else:
         foregroundColor = statsFrameColor
      number = customtkinter.CTkLabel( master=columnFrame, text=rowIndex, font=( 'Arial', 12 ), fg_color=foregroundColor )
      number.grid( row=rowIndex+1, column=0 )
      rowNumbers.append( number )
   
   for colIndex in range( len( table[ 0 ] ) ):      
      # Make a frame for this column
      columnFrame = customtkinter.CTkFrame( master=statsFrame )
      columnFrame.grid( row=0, column=colIndex+1 )

      # Add it to the global list so the color can be changed later
      columnFrames.append( columnFrame )
      
      # Put the attribute label at the top of the column
      tableEntry = customtkinter.CTkButton( master=columnFrame, width=30, text=table[ 0 ][ colIndex ], command=lambda sortByCol=colIndex : sortCallback( sortByCol ) )
      tableEntry.grid( row=0, column=0, padx=8, pady=6 )
      tableEntries[ 0 ].append( tableEntry )
      
      # Fill the rest of the column frame with stats
      numRows = min( rowsDisplayed+1, len( table ) )
      for rowIndex in range( 1, numRows ):
         if rowIndex % 2 == 0:
            # Even rows have darker color
            tableEntry = customtkinter.CTkLabel( master=columnFrame, text=table[ rowIndex ][ colIndex ], font=( 'Arial', 16, 'bold' ), fg_color='gray80' )
         else:
            # Odd rows have no color (fits in with background)
            tableEntry = customtkinter.CTkLabel( master=columnFrame, text=table[ rowIndex ][ colIndex ], font=( 'Arial', 16, 'bold' ) )
         
         tableEntry.grid( row=rowIndex, column=0, padx=0 )
         tableEntries[ rowIndex ].append( tableEntry )
   # end of for colIndex in range( len( table[ 0 ] ) )
   
   button = customtkinter.CTkButton( master=statsFrame, text='Previous Page', width=buttonWidth, command=lambda:pageChangeCallback( -1 ) )
   button.place( relx=0.02, rely=0.98, anchor=customtkinter.SW )
   
   button = customtkinter.CTkButton( master=statsFrame, text='Next Page', width=buttonWidth, command=lambda:pageChangeCallback( 1 ) )
   button.place( relx=0.98, rely=0.98, anchor=customtkinter.SE )

   global pageDisplay
   pageDisplay = customtkinter.CTkLabel( master=statsFrame, text='1 of 1', width=10 )
   pageDisplay.place( relx=0.5, rely=0.985, anchor=customtkinter.S )          
               
def updateStats( table, currentPage ):
   global tableEntries
   global columnFrames
   global rowNumbers
   global statsFrameColor
   
   if table == None:
      print( 'Attempt to update stats with empty table' )
      return
   if currentPage <= 0 or currentPage > numberOfPages:
      print( f'Invalid page number {currentPage} with {numberOfPages} pages total' )
      return
   
   # Change the labels to the new attributes
   for colIndex in range( len( tableEntries[ 0 ] ) ):
      if colIndex < len( table[ 0 ] ):
         # Make sure this button is visible
         tableEntries[ 0 ][ colIndex ].grid( )
         # Use the text from the table
         tableEntries[ 0 ][ colIndex ].configure( text=table[ 0 ][ colIndex ] )
      else:
         # No more attributes, display empty buttons
         tableEntries[ 0 ][ colIndex ].grid_remove( )
   
   firstRowDisplayed = ( currentPage - 1 ) * rowsDisplayed
   
   # Fill the stats
   numRows = min( rowsDisplayed+1, len( table ) )
   for rowIndex in range( 1, numRows ) :
      tableRowIndex = rowIndex + firstRowDisplayed
      rowNumbers[ rowIndex-1 ].configure( text=str( tableRowIndex ) )

      for colIndex in range( len( tableEntries[ 0 ] ) ):  
         if tableRowIndex < len( table ) and colIndex < len( table[ 0 ] ):
            # Stat here, display it
            tableEntries[ rowIndex ][ colIndex ].configure( text=str( table[ tableRowIndex ][ colIndex ] ) )
         else:
            # Nothing in this column
            tableEntries[ rowIndex ][ colIndex ].configure( text='' )
            
   updateColumnColors( )
            
def updateColumnColors( ):
   global columnFrames
   global statsFrameColor
   global currentSortCol
   
   # Update the background color of the columns in case it has changed
   for colIndex, columnFrame in enumerate( columnFrames ):
      if colIndex == currentSortCol:
         columnFrame.configure( fg_color='gray76' )
      else:
         columnFrame.configure( fg_color=statsFrameColor )
         
def startGUI( defaultStats ):
   global currentStats
   global screenHeight
   global screenWidth
   currentStats = defaultStats
   
   checkPackageInstalled = 'customtkinter'
   if importlib.util.find_spec( checkPackageInstalled ) is None:
      return
   
   customtkinter.set_appearance_mode( 'light' )
   customtkinter.set_default_color_theme( 'green' )

   global root
   root = customtkinter.CTk( )
   root.title( 'Download NFL Stats' )
   root.geometry( str( screenWidth ) + 'x' + str( screenHeight ) )
   
   # Set up groups of buttons
   global selectionFrame
   selectionFrame = customtkinter.CTkFrame( master=root )
   selectionFrame.grid( row=0, column=0, padx=( 10, 0 ), pady=12, sticky=customtkinter.NW )
   
   downloadFrame = customtkinter.CTkFrame( master=root )
   downloadFrame.grid( row=9, column=0, padx=( 10, 0 ), pady=12, sticky=customtkinter.SW )
   
   global statsFrame
   statsFrame = customtkinter.CTkFrame( master=root, width=( screenWidth - 175 ), height=650 )
   statsFrame.grid( row=0, column=1, rowspan=10, padx=10, pady=12, sticky=customtkinter.NW )
   statsFrame.grid_propagate( 0 )
   
   # Fill the selection frame
   categoryDropdown = customtkinter.CTkOptionMenu( master=selectionFrame, width=buttonWidth, values=categories, command=categoryDropdownCallback )
   categoryDropdown.pack( pady=( 12, 0 ), padx=10 )
   
   yearDropdown = customtkinter.CTkOptionMenu( master=selectionFrame, width=buttonWidth, values=years, command=yearDropdownCallback )
   yearDropdown.pack( pady=( 12, 0 ), padx=10 )
   
   button = customtkinter.CTkButton( master=selectionFrame, width=buttonWidth, text='Load', command=lambda: loadCallback( categorySelected, yearSelected, root ) )
   button.pack( pady=( 12, 12 ), padx=10 )
   
   # Fill the download frame
   global fileNameSelected
   fileNameSelected = customtkinter.StringVar( master=downloadFrame, value=( categorySelected + str( yearSelected ) ) )
   fileNameEntry = customtkinter.CTkEntry( master=downloadFrame, width=buttonWidth, textvariable=fileNameSelected )
   fileNameEntry.pack( padx=10, pady=( 12, 0 ) )
   
   dropdown = customtkinter.CTkOptionMenu( master=downloadFrame, width=buttonWidth, values=fileTypes, command=fileTypeDropdownCallback )
   dropdown.pack( padx=10, pady=( 12, 0 ) )
   
   button = customtkinter.CTkButton( master=downloadFrame, width=buttonWidth, text='Download', command=lambda:downloadCallback( fileNameEntry ) )
   button.pack( padx=10, pady=12 )
   
   # Fill the stats frame
   initStatsFrame( defaultStats, statsFrame )
   # Display the first page and the rest will load after the window opens
   displayPage( defaultStats )
   
   # Display GUI and load extra after 750 ms
   root.after( 50, resizeWindow )
   root.after( 750, loadPages )
   root.mainloop( )