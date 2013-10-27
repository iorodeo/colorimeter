from __future__ import print_function
import serial
import time

RESET_SLEEP_T = 2.0

CMD_CALIBRATE = 0
CMD_GET_MEASUREMENT = 1
CMD_SET_NUM_SAMPLES = 2
CMD_GET_NUM_SAMPLES = 3
CMD_GET_CALIBRATION = 4

CMD_CALIBRATE_RED = 5 
CMD_CALIBRATE_GREEN = 6
CMD_CALIBRATE_BLUE = 7
CMD_CALIBRATE_WHITE = 8

CMD_GET_MEASUREMENT_RED = 9
CMD_GET_MEASUREMENT_GREEN = 10
CMD_GET_MEASUREMENT_BLUE = 11
CMD_GET_MEASUREMENT_WHITE = 12

CMD_SET_MODE_COLOR_SPECIFIC = 13
CMD_SET_MODE_COLOR_INDEPENDENT = 14
CMD_GET_SENSOR_MODE = 15

SENSOR_MODE_COLOR_SPECIFIC = 0
SENSOR_MODE_COLOR_INDEPENDENT = 1

LED_COLOR_LIST = 'red', 'green', 'blue', 'white'

RSP_ERROR = 0
RSP_SUCCESS = 1

class Colorimeter(serial.Serial):

    def __init__(self, port, timeout=10.0, debug=False):
        params = {'baudrate': 9600, 'timeout': timeout}
        super(Colorimeter,self).__init__(port,**params)
        time.sleep(RESET_SLEEP_T)
        self.debug=debug
        self.clearBuffer()

    def clearBuffer(self):
        time.sleep(0.1)
        while self.inWaiting() > 0:
            self.read(self.inWaiting())
            time.sleep(0.1)

    def sendCmd(self,cmd):
        """
        Send command to colorimeter and receiver response.
        """
        self.write('{0}\n'.format(cmd))
        rsp = self.readline()
        self.clearBuffer()
        if self.debug:
            print('cmd: ', cmd)
            print('rsp: ', rsp)

        if len(rsp) < 2:
            raise IOError, 'response from device is too short'

        if rsp[1] == str(RSP_ERROR):
            raise IOError, 'RSP_ERROR: {0}'.format(rsp)

        try:
            rsp = eval(rsp.strip())
        except Exception:
            raise IOError, 'bad response unable to parse result'

        return rsp
        
    def calibrate(self,color=None):
        """
        Calibrate the colorimeter (all channels).
        """
        if color is None:
            cmd = '[{0}]'.format(CMD_CALIBRATE) 
            rsp = self.sendCmd(cmd)
        else:
            color = color.lower()
            if not color in LED_COLOR_LIST:
                raise ValueError, 'unknown device color {0}'.format(color)
            calFunc = getattr(self,'calibrate{0}'.format(color.title()))
            rsp = calFunc()

    def calibrateRed(self):
        """
        Calibrate the red channel of the colorimeter
        """
        cmd = '[{0}]'.format(CMD_CALIBRATE_RED)
        rsp = self.sendCmd(cmd)

    def calibrateGreen(self):
        """
        Calibrate the green channel of the colorimeter
        """
        cmd = '[{0}]'.format(CMD_CALIBRATE_GREEN)
        rsp = self.sendCmd(cmd)

    def calibrateBlue(self):
        """
        Calibrate the blue channe of the colorimeter
        """
        cmd = '[{0}]'.format(CMD_CALIBRATE_BLUE)
        rsp = self.sendCmd(cmd)

    def calibrateWhite(self):
        """
        Calibrate the white channel of the colorimeter
        """
        cmd = '[{0}]'.format(CMD_CALIBRATE_WHITE)
        rsp = self.sendCmd(cmd)

    def getCalibration(self):
        """
        Get the current calibration freqeuncy values.

        Returns the calibration freqeuncies for red, green, blue and white
        light.
        """
        cmd = '[{0}]'.format(CMD_GET_CALIBRATION)
        rsp = self.sendCmd(cmd)
        return rsp[1:5] 

    def getMeasurement(self,color='all'):
        """
        Get a measurement from the device. 
        """
        if color == 'all':
            cmd = '[{0}]'.format(CMD_GET_MEASUREMENT)
            rsp = self.sendCmd(cmd)
            freq = tuple(rsp[1:5])
            tran = tuple(rsp[5:9])
            abso = tuple(rsp[9:])
        elif color in ('red', 'green', 'blue', 'white'):
            measureFunc = getattr(self,'getMeasurement{0}'.format(color.title()))
            freq, tran, abso = measureFunc()
        else:
            raise ValueError, 'unknown color {0}'.format(color)
        return freq, tran, abso

    def getMeasurementRed(self):
        """
        Get a measurement from the red channel
        """
        cmd = '[{0}]'.format(CMD_GET_MEASUREMENT_RED)
        rsp = self.sendCmd(cmd)
        freq, tran, abso = rsp[1:4]
        return freq, tran, abso

    def getMeasurementGreen(self):
        """
        Get a measurement from the green channel
        """
        cmd = '[{0}]'.format(CMD_GET_MEASUREMENT_GREEN)
        rsp = self.sendCmd(cmd)
        freq, tran, abso = rsp[1:4]
        return freq, tran, abso

    def getMeasurementBlue(self):
        """
        Get a measurement from the blue channel
        """
        cmd = '[{0}]'.format(CMD_GET_MEASUREMENT_BLUE)
        rsp = self.sendCmd(cmd)
        freq, tran, abso = rsp[1:4]
        return freq, tran, abso

    def getMeasurementWhite(self):
        """
        Get a measurement from the white channel
        """
        cmd = '[{0}]'.format(CMD_GET_MEASUREMENT_WHITE)
        rsp = self.sendCmd(cmd)
        freq, tran, abso = rsp[1:4]
        return freq, tran, abso

    def setNumSamples(self,value):
        """
        Set the number of samples aquired per measurement.
        """
        if value <= 0 or value > (2**16-1):
            raise ValueError, 'numSamples must be > 0 or < 2**16 -1'
        cmd = '[{0}, {1}]'.format(CMD_SET_NUM_SAMPLES,value)
        rsp = self.sendCmd(cmd)

    def getNumSamples(self):
        """
        Get the current value set for the number of samples per measurement.
        """
        cmd = '[{0}]'.format(CMD_GET_NUM_SAMPLES) 
        rsp = self.sendCmd(cmd)
        numSamples = rsp[1]
        return numSamples

    def setSensorModeColorSpecific(self):
        """
        Set the sensor to color specific mode. In this mode it will use the 
        red/green/blue/clear color channel of the sensor when using the 
        red/green/blue/white led.
        """
        cmd = '[{0}]'.format(CMD_SET_MODE_COLOR_SPECIFIC)
        rsp = self.sendCmd(cmd)

    def setSensorModeColorIndependent(self):
        """
        Set the sensor to color independent mode. In this mode the clear
        (unfiltered) channel of the light sensor is used regardless of the led
        selected.
        """
        cmd = '[{0}]'.format(CMD_SET_MODE_COLOR_INDEPENDENT)
        rsp = self.sendCmd(cmd)

    def getSensorMode(self):
        """
        Returns the current color sensor mode setting.
        """
        cmd = '[{0}]'.format(CMD_GET_SENSOR_MODE)
        rsp = self.sendCmd(cmd)
        sensorMode = rsp[1]
        return sensorMode

    def printMeasurement(self):
        """
        Test function. Gets a measurement and pretty prints it.
        """
        f, t, a = self.getMeasurement()

        print('Frequency:')
        print('  red:    {0:1.2f}'.format(f[0]))
        print('  green:  {0:1.2f}'.format(f[1]))
        print('  blue:   {0:1.2f}'.format(f[2]))
        print('  white:  {0:1.2f}'.format(f[3]))

        print('Transmission:')
        print('  red:    {0:1.2f}'.format(t[0]))
        print('  green:  {0:1.2f}'.format(t[1]))
        print('  blue:   {0:1.2f}'.format(t[2]))
        print('  white:  {0:1.2f}'.format(t[3]))

        print('Absorbance:')
        print('  red:    {0:1.2f}'.format(a[0]))
        print('  green:  {0:1.2f}'.format(a[1]))
        print('  blue:   {0:1.2f}'.format(a[2]))
        print('  white:  {0:1.2f}'.format(a[3]))

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    dev = Colorimeter('/dev/ttyACM0')
    dev.printMeasurement()







    
        
