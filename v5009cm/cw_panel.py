# ----- CW Panel -----
#   Contains a row of labels at the top
#   Mode Selectors
#   Frequency Spinboxes
#   Attenuation Spinboxes
#   PDN toggle button
#   Reference Source selector
#   Reference Frequency SpinBox

import tkinter as tk
from functools import partial

class CwPanel( tk.Frame ):

    # The following procedure is passed to us by our parent window
    @staticmethod
    def sendCommand():
        pass

    @staticmethod
    def setSendCommand( functionPtr ):
        CwPanel.sendCommand = functionPtr
    
    # ----- Constructor -----
    def __init__( self, parent ):
        # Call the base constructor
        super().__init__(parent)

        self.parent = parent    # parent = root
        
        self.modeBox = [ None, None ]
        self.modeActual = [ None, None ]

        self.freqBox = [ None, None ]        # Two frequency spinboxes
        self.freqActual = [ None, None ]     # Freq Actual labels

        self.attBox = [ None, None ]
        self.attActual = [ None, None ]

        self.pdnBox = [ None, None ]
        self.pdnActual = [ None, None ]

        self.refSourceBox = None
        self.refSourceActual = None
        
        self.refFreqBox = None
        self.refFreqActual = None

        self.grid()

        self[ "bg" ] = 'ivory'

        nextCol = 0
        nextRow = 0

        # ----- Header Labels -----
        headerText = [ "Main Panel", "Source 1", "Actual", "",
                                     "Source 2", "Actual"
                     ]
        for ix in range( 6 ):
            label = tk.Label( self, text=headerText[ix] )
            label.grid( column=nextCol, row=nextRow, sticky='EW' )
            if ( ix == 3 ):
                label[ 'width' ] = 1
            else:    
                label[ 'bg' ] = 'dark green'
                label[ 'fg' ] = 'white'
            nextCol += 1

        nextCol = 0
        nextRow += 1

        # ----- Mode selectors -----
        temp = tk.Label( self, text="Mode" )
        temp.grid( column=nextCol, row=nextRow, sticky='EW' )
        temp[ 'bg' ] = 'ivory'
        nextCol += 1

        for ix in range( 2 ):
            # a temporary textvariable
            value = tk.StringVar()
            # Instantiate the Mode menu
            temp = tk.OptionMenu( self, value, 'CW', 'Sweep', 'List' )
            temp.grid( column=nextCol, row=nextRow, sticky='EW' )
            nextCol += 1
                                    
            temp.name = 'Mode'
            temp.Source = ix + 1
            value.set( 'CW' )
            # Imbed the textvariable into the widget
            temp.Value = value
            temp.Text = None
            temp[ 'bg' ] = 'ivory'
            temp.Value.trace( "w", partial( self.OptionMenuEH, temp ) )

            # Store the widget in its permanent location
            self.modeBox[ ix ] = temp
            
            # Mode Actual
            temp = tk.Label( self )
            temp.grid( column=nextCol, row=nextRow )
            nextCol += 1

            temp.Text = tk.StringVar()
            temp.Text.set( 'CW' )
            temp[ "textvariable" ] = temp.Text
            temp[ "width" ] = 12
            temp[ 'bg' ] = 'ivory'
            
            self.modeActual[ ix ] = temp

            # ----- spacer -----
            if ( ix == 0 ):
                temp = tk.Label( self )
                temp[ 'width' ] = 1
                temp.grid( column=nextCol, row=nextRow )
                nextCol += 1

        nextCol = 0
        nextRow += 1

        # ----- Frequency -----
        temp = tk.Label( self, text="Frequency" )
        temp.grid( column=nextCol, row=nextRow, sticky='EW' )
        temp[ 'bg' ] = 'ivory'
        nextCol += 1

        for ix in range( 2 ):
            
            # ----- Freq Box -----
            temp = tk.Spinbox( self ) 
            temp.grid( column=nextCol, row=nextRow )
            nextCol += 1
            temp.name = "Freq" 
            temp.Source = ix + 1
            temp[ 'bg' ] = 'ivory'
            temp[ 'to' ] = 6001
            temp[ 'from_' ] = 22.9
            temp.Value = tk.DoubleVar()
            temp.Value.set( 2440 + 10 * ix )
            temp[ "textvariable" ] = temp.Value 

            #EH for the up/down arrows
            temp[ "command" ] = partial( self.SpinboxEH, temp )
            # EH for the return key
            temp.bind( "<Return>", self.spinBoxReturnEH )
            
            self.freqBox[ ix ] = temp
        
            # ----- Freq Actual -----
            
            temp = tk.Label( self )
            temp.grid( column=nextCol, row=nextRow )
            nextCol += 1

            temp.Text = tk.StringVar()
            temp.Text.set( "MHz" )
            temp[ 'textvariable' ] = temp.Text
            temp[ 'width' ] = 12
            temp[ 'bg' ] = 'ivory'
            self.freqActual[ ix ] = temp

            # ----- spacer -----
            if ( ix == 0 ):
                temp = tk.Label( self )
                temp[ 'width' ] = 1
                temp.grid( column=nextCol, row=nextRow )
                nextCol += 1
                
        nextCol = 0
        nextRow += 1

        # ----- Attenuation -----
        temp = tk.Label( self, text="Attenuation" )
        temp.grid( column=nextCol, row=nextRow, sticky='EW' )
        temp[ 'bg' ] = 'ivory'
        nextCol += 1

        for ix in range( 2 ):
            
            # ----- Attenuation Box -----
            temp = tk.Spinbox( self )
            temp.grid( column=nextCol, row=nextRow )
            nextCol += 1

            temp.name = "ATT" 
            temp.Source = ix + 1
            temp[ 'bg' ] = 'ivory'
            temp[ 'from_' ] = 0
            temp[ 'to' ] = 31.5
            temp.Value = tk.DoubleVar()
            temp.Value.set( 15.0 )
            temp[ 'textvariable' ] = temp.Value
            temp[ 'increment' ] = 0.5


            temp[ "command" ] = partial( self.SpinboxEH, temp )

            # Attach an EH to the return key
            temp.bind( "<Return>", self.spinBoxReturnEH )
            
            self.attBox[ ix ] = temp
        
            # ----- Attenuation Actual -----
            
            temp = tk.Label( self )
            temp.grid( column=nextCol, row=nextRow )
            nextCol += 1

            temp.Text = tk.StringVar()
            temp.Text.set( "dB" )
            temp[ 'textvariable' ] = temp.Text
            temp[ 'width' ] = 12
            temp[ 'bg' ] = 'ivory'
            self.attActual[ ix ] = temp

            # ----- spacer -----
            if ( ix == 0 ):
                temp = tk.Label( self )
                temp[ 'width' ] = 1
                temp.grid( column=nextCol, row=nextRow )
                nextCol += 1
                
        nextCol = 0
        nextRow += 1

        # ----- PDN Buttons -----
        temp = tk.Label( self, text="Power" )
        temp.grid( column=nextCol, row=nextRow, sticky='EW' )
        temp[ 'bg' ] = 'ivory'
        nextCol += 1

        for ix in range( 2 ):
            
            # ----- PDN Box -----
            temp = tk.Checkbutton( self )
            temp.grid( column=nextCol, row=nextRow, stick='EW' )
            nextCol += 1

            temp.name = "PDN" 

            temp.Text = tk.StringVar()
            temp.Text.set( 'On' )
            temp.Value = tk.IntVar()
            temp.Value.set( 1 )
            temp.Source = ix + 1
            temp[ 'indicatoron' ] = 0
            temp[ 'bg' ] = 'ivory'
            temp[ 'selectcolor' ] = 'palegreen'
            temp[ 'textvariable' ] = temp.Text
            temp[ 'variable' ] = temp.Value 
            temp.Value.trace( "w", partial( self.CheckbuttonEH, temp ) )
            self.pdnBox[ ix ] = temp
        
            # ----- PDN Actual -----
            
            temp = tk.Label( self )
            temp.grid( column=nextCol, row=nextRow )
            nextCol += 1

            temp.Text = tk.StringVar()
            temp.Text.set( "---" )
            temp[ 'textvariable' ] = temp.Text
            temp[ 'width' ] = 12
            temp[ 'bg' ] = 'ivory'
            self.pdnActual[ ix ] = temp

            # ----- spacer -----
            if ( ix == 0 ):
                temp = tk.Label( self )
                #temp[ 'width' ] = 1
                temp.grid( column=nextCol, row=nextRow )
                nextCol += 1
                
        nextCol = 0
        nextRow += 1

        # ----- Reference Source Selector -----
        temp = tk.Label( self, text="Reference Source" )
        temp.grid( column=nextCol, row=nextRow, columnspan=2, sticky='EW' )
        temp[ 'bg' ] = 'ivory'
        nextCol += 2

        text = tk.StringVar()
        textValues = [ 'Internal', 'External' ]
        temp = tk.OptionMenu( self, text, *textValues )
        temp.grid( column=nextCol, row=nextRow, columnspan=2, sticky='EW' )
        nextCol += 2

        temp.name = "Refs"
        temp.Source = -1
        text.set( textValues[ 0 ] )
        temp.Text = text
        temp.TextValues = textValues
        temp.Value = tk.IntVar()
        temp.Value.set( 0 )
        temp[ 'bg' ] = 'ivory'
        temp.Text.trace( "w", partial( self.OptionMenuEH, temp ) )
        self.refSourceBox = temp

        # Ref Source Actual
        temp = tk.Label( self )
        temp.grid( column=nextCol, row=nextRow )
        nextCol += 1

        temp.Text = tk.StringVar()
        temp.Text.set( 'Internal' )
        temp[ "textvariable" ] = temp.Text
        temp[ "width" ] = 12
        temp[ 'bg' ] = 'ivory'
            
        self.refSourceActual = temp

        nextCol = 0
        nextRow += 1

        # ----- Reference Frequency -----
        temp = tk.Label( self, text="Ref Freq" )
        temp.grid( column=nextCol, row=nextRow, columnspan=2, sticky='EW' )
        temp[ 'bg' ] = 'ivory'
        nextCol += 2

        # ----- Ref Freq Box -----
        temp = tk.Spinbox( self )
        temp.grid( column=nextCol, row=nextRow, columnspan=2 )
        nextCol += 2

        temp.name = "REF" 
        temp.Source = -1
        temp[ 'bg' ] = 'ivory'
        temp[ 'to' ] = 100
        temp[ 'from_' ] = 5
        temp.Value = tk.DoubleVar()
        temp.Value.set( 20 )
        temp[ 'textvariable' ] = temp.Value
        temp[ 'increment' ] = 1

        # EH for up/down arrows
        temp[ "command" ] = partial( self.SpinboxEH, temp )
        # EH for the return key
        temp.bind( "<Return>", self.spinBoxReturnEH )
        
        self.refFreqBox = temp
    
        # ----- Ref Freq Actual -----
        
        temp = tk.Label( self )
        temp.grid( column=nextCol, row=nextRow )
        nextCol += 1

        temp.Text = tk.StringVar()
        temp.Text.set( "20" )
        temp[ 'textvariable' ] = temp.Text
        #temp[ 'width' ] = 12
        temp[ 'bg' ] = 'ivory'
        self.refFreqActual = temp

        nextCol = 0
        nextRow += 1

    def OptionMenuEH( self, widget, *args ):
        
        # Some 5009 commands take text.  Others take an index.
        # Widgets for commands the take text will store text in widget.Value.
        # Widgets for commands that take an index will store text
        # in widget.Text, with the index in Widget.Value
        # Here, we turn text into an index, for commands that need one.
        if ( ( widget.Text != None ) and ( widget.TextValues != None ) ):
            text = widget.Text.get()
            widget.Value.set( widget.TextValues.index( text ) )
        self.sendCommand( widget )
        
    # Spinbox <Return> Key Event Handler
    def spinBoxReturnEH( self, event ):
        self.sendCommand( event.widget )

    def SpinboxEH( self, widget ):
        self.parent.sendCommand( widget )

    def CheckbuttonEH( self, btn, *args ):
        value = btn.Value.get()
        btn.Text.set( [ 'Off', 'On' ][ value ] )
        btn[ 'bg' ] = [ 'mistyrose', 'pale green' ][ value ]
        self.sendCommand( btn )

