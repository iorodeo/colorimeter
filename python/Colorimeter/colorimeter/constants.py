import os

# Development
DEVEL_FAKE_MEASURE = False 
#DEVEL_FAKE_MEASURE = True 

# Serial ports
DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 
DFLT_PORT_DARWIN = '/dev/tty.usbmodem'

# LEDs
LED_NUMBERS = range(4)

## Standard rgb mode
#STD_NUMBER_OF_LEDS = 4 
#STD_DFLT_LED_COLOR = 'red'
#STD_LED_COLORS = ['red', 'green', 'blue', 'white']
#STD_LED_NUM_TO_COLOR = dict([(k,v) for k,v in zip(LED_NUMBERS,STD_LED_COLORS)])
#STD_LED_COLOR_TO_NUM = dict([(v,k) for k,v in STD_LED_NUM_TO_COLOR.iteritems()])
#
## Custom LED VerB mode
#VERB_NUMBER_OF_LEDS = 1
#VERB_LED_TEXT = 'D1'
#VERB_LED_DEVICE_COLOR = 'blue' # legacy 'device color' specifies which dio to use
#
## Custom LED VerC mode
#VERC_DFLT_LED = 'D1'
#VERC_NUMBER_OF_LEDS = 2
#VERC_LED_NUM_TO_VISIBLE = {0:True, 1:True, 2:False, 3:False}
#VERC_LED_NUM_TO_TEXT = {0:'D1', 1:'D2', 2:'', 3:''}
#VERC_LED_NUM_TO_DEVICE_COLOR = {0:'blue',1:'green',2:None,3:None}  # legacy 'device color' specifies which dio to use.

MODE_CONFIG = {}
MODE_CONFIG['StandardRGBLED'] = {
        'LED' : { 
            0 : { 
                'text'     : 'red', 
                'visible'  : True, 
                'devColor' : 'red' 
                },
            1 : {
                'text'     : 'green',
                'visible'  : True,
                'devColor' : 'green',
                },
            2 : {
                'text'     : 'blue',
                'visible'  : True,
                'devColor' : 'blue',
                },
            3 : {
                'text'     : 'white',
                'visible'  : True,
                'devColor' : 'white',
                },
            },
        'colorMode'       : 'specific',
        'LEDLabelVisible' : True,
        }


MODE_CONFIG['CustomLEDVerB'] = {
        'LED' : { 
            0 : { 
                'text'     : '', 
                'visible'  : False, 
                'devColor' : 'blue', 
                },
            },
        'colorMode'       : 'independent',
        'LEDLabelVisible' : False,
        }

MODE_CONFIG['CustomLEDVerC'] = {
        'LED' : { 
            0 : {
                'text'     : 'D1',
                'visible'  : True,
                'devColor'  : 'blue',
                },
            1 : {
                'text'     : 'D2',
                'visible'  : True,
                'devColor' : 'green',
                }, 
            },
        'colorMode'       : 'colorIndependent',
        'LEDLabelVisible' : True,
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
PLOT_COLOR_DICT = {'red':'r','green':'g','blue':'b','white': 'w','D1':'r','D2':'b'} 
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

# Significant Digits
SIGNIFICANT_DIGITS_LIST = [1,2,3,4] 
DEFAULT_SIGNIFICANT_DIGIT_INDEX = 2


