import customtkinter

# Constants
screenWidth = 1010
screenHeight = 545
buttonWidth = 100

# GUI elements
# stats = None

# Dropdown options
# ----------------------------------------------------------------
fileTypes = [
   '.txt',
   '.csv',
   '.xlsb'
]
fileTypeSelected = fileTypes[ 0 ]

years = [ str( 2022 - i ) for i in range( 10 ) ]
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
   
def updateStats( newString ):
   global stats
   stats.configure( text=newString )
   
def startGUI( defaultStats, prevPageCallback, nextPageCallback, loadCallback ):
   customtkinter.set_appearance_mode( 'dark' )
   customtkinter.set_default_color_theme( 'dark-blue' )

   root = customtkinter.CTk( )
   root.geometry( str( screenWidth ) + 'x' + str( screenHeight ) )
   root.title( 'Download NFL Stats' )
   
   # Set up groups of buttons
   selectionFrame = customtkinter.CTkFrame( master=root )
   selectionFrame.grid( row=0, column=0, padx=( 10, 0 ), pady=12, sticky=customtkinter.NW )
   
   downloadFrame = customtkinter.CTkFrame( master=root )
   downloadFrame.grid( row=9, column=0, padx=( 10, 0 ), pady=12, sticky=customtkinter.SW )
   
   statsFrame = customtkinter.CTkFrame( master=root )
   statsFrame.grid( row=0, column=1, rowspan=10, padx=10, pady=12, sticky=customtkinter.NW )
   
   # Fill the selection frame
   categoryDropdown = customtkinter.CTkOptionMenu( master=selectionFrame, width=buttonWidth, values=categories, command=categoryDropdownCallback )
   categoryDropdown.pack( pady=( 12, 0 ), padx=10 )
   
   yearDropdown = customtkinter.CTkOptionMenu( master=selectionFrame, width=buttonWidth, values=years, command=yearDropdownCallback )
   yearDropdown.pack( pady=( 12, 0 ), padx=10 )
   
   button = customtkinter.CTkButton( master=selectionFrame, width=buttonWidth, text='Load', command=lambda: loadCallback( categorySelected, yearSelected ) )
   button.pack( pady=( 12, 12 ), padx=10 )
   
   # Fill the download frame
   dropdown = customtkinter.CTkOptionMenu( master=downloadFrame, width=buttonWidth, values=fileTypes, command=fileTypeDropdownCallback )
   dropdown.pack( padx=10, pady=( 12, 0 ) )
   
   button = customtkinter.CTkButton( master=downloadFrame, width=buttonWidth, text='Download', command=placeholderCommand )
   button.pack( padx=10, pady=12 )
   
   # Fill the stats frame
   global stats
   stats = customtkinter.CTkLabel( master=statsFrame, text=defaultStats )
   stats.pack( pady=( 12, 50 ), padx=10, side=customtkinter.LEFT )
   
   button = customtkinter.CTkButton( master=statsFrame, text='Previous Page', width=buttonWidth, command=prevPageCallback )
   button.place( relx=0.02, rely=0.98, anchor=customtkinter.SW )
   
   button = customtkinter.CTkButton( master=statsFrame, text='Next Page', width=buttonWidth, command=nextPageCallback )
   button.place( relx=0.98, rely=0.98, anchor=customtkinter.SE )
   root.mainloop( )