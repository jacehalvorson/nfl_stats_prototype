import customtkinter
from scrape import *
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

# Dropdown options
# ----------------------------------------------------------------
fileTypes = [
   '.txt',
   '.csv',
   '.xlsb'
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

def placeholderCommand( ):
   print( 'Button pressed' )
   
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
   
   displayPage( getPageFromURL( requestedUrl )  )
   window.after( 1000, loadPages )

def downloadCallback( ):
   if buttonsActive == False:
      return
   
   print( 'Download not implemented' )

def sortCallback( ):
   if buttonsActive == False:
      return

   print( 'Sort not implemented' )

def displayPage( firstPage ):
   global currentStats
   global currentPage
   global buttonsActive
   
   # Disable buttons while data laods
   buttonsActive = False
   
   currentPage = 1
   updateStats( firstPage, currentPage )

   pageDisplay.configure( text='1 of 1' )
   
   currentStats = firstPage
   
def loadPages( ):
   global currentStats
   global currentPage
   global numberOfPages
   global rowsDisplayed
   global buttonsActive
   
   # Load the rest of the data
   nextPageURL = getNextPage( False )
   currentStats = extendTableWithoutFirstRow( currentStats, getTableFromURL( nextPageURL ) )
   
   numberOfPages = int( floor( len( currentStats ) / rowsDisplayed ) )
   pageDisplay.configure( text=( '1 of ' + str( numberOfPages ) ) )
   
   # Set screen width and height to fit the frame
   # screenWidth = statsFrame.winfo_width( ) + selectionFrame.winfo_width( ) + 30
   # screenHeight = statsFrame.winfo_height( ) + 24
   # root.geometry( str( screenWidth ) + 'x' + str( screenHeight ) )
   
   buttonsActive = True

def initTable( table, statsFrame ):
   global tableEntries
   tableEntries = [ ]
   
   for rowIndex in range( rowsDisplayed+1 ):
      # Initialize a list for this row of entries
      tableEntries.append( [ ] )
      
      for colIndex in range( len( table[ 0 ] ) ):
         if rowIndex == 0:
            # Place a button in the first row
            tableEntry = customtkinter.CTkButton( master=statsFrame, width=30, text=str( table[ rowIndex ][ colIndex ] ), command=sortCallback )
         else:
            # Place a stat in the table
            tableEntry = customtkinter.CTkLabel( master=statsFrame, width=20, text=str( table[ rowIndex ][ colIndex ] ), font=( 'Arial', 16, 'bold' ) )
         
         tableEntries[ rowIndex ].append( tableEntry )
         
         # Place the entry on the GUI
         if rowIndex == 0:
            # Add vertical padding on the first row
            tableEntry.grid( row=rowIndex, column=colIndex, padx=8, pady=8 )
         if rowIndex == rowsDisplayed:
            # Add vertical padding on the bottom for last row
            tableEntry.grid( row=rowIndex, column=colIndex, padx=8, pady=( 0, 50 ) )
         else:
            # Don't add padding
            tableEntry.grid( row=rowIndex, column=colIndex, padx=8 )
               
def updateStats( table, currentPage ):
   global tableEntries
   
   if table == None:
      print( 'Attempt to update stats with empty table' )
      return
   
   firstRowDisplayed = ( currentPage - 1 ) * rowsDisplayed
   
   for rowIndex in range( 1, rowsDisplayed + 1 ):
      for colIndex in range( len( table[ 0 ] ) ):
         tableRowIndex = rowIndex + firstRowDisplayed
         if tableRowIndex >= len( table ):
            print( formatString( table ) )
            return
         
         tableEntries[ rowIndex ][ colIndex ].configure( text=str( table[ tableRowIndex ][ colIndex ] ) )
         
def startGUI( defaultStats ):
   global currentStats
   global screenHeight
   global screenWidth
   currentStats = defaultStats
   
   customtkinter.set_appearance_mode( 'light' )
   customtkinter.set_default_color_theme( 'green' )

   root = customtkinter.CTk( )
   root.title( 'Download NFL Stats' )
   root.geometry( str( screenWidth ) + 'x' + str( screenHeight ) )
   
   # Set up groups of buttons
   selectionFrame = customtkinter.CTkFrame( master=root )
   selectionFrame.grid( row=0, column=0, padx=( 10, 0 ), pady=12, sticky=customtkinter.NW )
   
   downloadFrame = customtkinter.CTkFrame( master=root )
   downloadFrame.grid( row=9, column=0, padx=( 10, 0 ), pady=12, sticky=customtkinter.SW )
   
   statsFrame = customtkinter.CTkFrame( master=root, width=( screenWidth - 175), height=650 )
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
   dropdown = customtkinter.CTkOptionMenu( master=downloadFrame, width=buttonWidth, values=fileTypes, command=fileTypeDropdownCallback )
   dropdown.pack( padx=10, pady=( 12, 0 ) )
   
   button = customtkinter.CTkButton( master=downloadFrame, width=buttonWidth, text='Download', command=downloadCallback )
   button.pack( padx=10, pady=12 )
   
   # Fill the stats frame
   initTable( defaultStats, statsFrame )
   
   button = customtkinter.CTkButton( master=statsFrame, text='Previous Page', width=buttonWidth, command=lambda:pageChangeCallback( -1 ) )
   button.place( relx=0.02, rely=0.98, anchor=customtkinter.SW )
   # button.grid( row=len( defaultStats ), column=0 )
   
   button = customtkinter.CTkButton( master=statsFrame, text='Next Page', width=buttonWidth, command=lambda:pageChangeCallback( 1 ) )
   button.place( relx=0.98, rely=0.98, anchor=customtkinter.SE )
   # button.grid( row=len( defaultStats ), column=len( defaultStats[ 0 ] )-1 )

   global pageDisplay
   pageDisplay = customtkinter.CTkLabel( master=statsFrame, text='1 of 1', width=10 )
   pageDisplay.place( relx=0.5, rely=0.985, anchor=customtkinter.S )
   
   displayPage( defaultStats )
   
   root.after( 1000, loadPages )
   root.mainloop( )
   