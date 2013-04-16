import os

# Development
#DEVEL_FAKE_MEASURE = False 
DEVEL_FAKE_MEASURE = True 

# Serial ports
DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 
DFLT_PORT_DARWIN = '/dev/tty.usbmodem'

# LEDs
DFLT_LED_COLOR = 'red'
COLOR2LED_DICT = {
        'red'   : 0,
        'green' : 1,
        'blue'  : 2,
        'white' : 3,
        } 

# Data table
TABLE_MIN_ROW_COUNT = 4 
TABLE_COL_COUNT = 2 

# Data fit type
LINEAR_FIT_TYPE = 'force_zero'

# Plotting
PLOT_FIGURE_NUM = 1
PLOT_BAR_WIDTH = 0.8
PLOT_TEXT_Y_OFFSET = 0.01
PLOT_YLIM_ADJUST = 1.15
PLOT_FIT_NUM_PTS = 500
PLOT_SLOPE_TEXT_POS = 0.15,0.84
PLOT_COLOR_DICT = {
        'red'   : 'r',
        'green' : 'g',
        'blue'  : 'b',
        'white' : 'w',
        }

# No value symbols
NO_VALUE_SYMBOL_LABEL = '_nv_'
NO_VALUE_SYMBOL_NUMBER = 'nan'

# User configuration and data directories 
USER_CONF_DIR = '.colorimeter'
USER_DATA_DIR = os.path.join(USER_CONF_DIR,'data')

# Window start positoin
START_POS_X = 75 
START_POS_Y = 75 

# About text messages
ABOUT_TEXT_COMMON = 'IO Rodeo Inc.'
BASIC_ABOUT_TEXT = 'Colorimieter Basic 0.1'
PLOT_ABOUT_TEXT = 'Colorimieter Plot 0.1'
MEASURE_ABOUT_TEXT = 'Colorimieter Measure 0.1'

