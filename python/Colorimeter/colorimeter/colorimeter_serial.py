from __future__ import print_function
import serial
import time

RESET_SLEEP_T = 2.0

CMD_CALIBRATE = 0
CMD_GET_MEASUREMENT = 1
CMD_SET_NUM_SAMPLES = 2
CMD_GET_NUM_SAMPLES = 3
CMD_GET_CALIBRATION = 4

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
        
    def calibrate(self):
        """
        Calibrate the colorimeter.
        """
        cmd = '[{0}]'.format(CMD_CALIBRATE) 
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

    def getMeasurement(self):
        """
        Get a measurement from the device. 
        """
        cmd = '[{0}]'.format(CMD_GET_MEASUREMENT)
        rsp = self.sendCmd(cmd)
        freq = tuple(rsp[1:5])
        trans = tuple(rsp[5:9])
        absorb = tuple(rsp[9:])
        return freq, trans, absorb

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







    
        
