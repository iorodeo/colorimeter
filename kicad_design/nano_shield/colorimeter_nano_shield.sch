EESchema Schematic File Version 2  date Fri 10 Feb 2012 03:52:34 PM PST
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:arduino_nano
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title ""
Date "10 feb 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 3400 3150 0    60   ~ 0
GND
Wire Wire Line
	3400 3050 3400 3150
Wire Wire Line
	6000 4750 5500 4750
Wire Wire Line
	6000 4650 5500 4650
Wire Wire Line
	6000 4450 5500 4450
Wire Wire Line
	6000 4250 5500 4250
Wire Wire Line
	7700 3850 8200 3850
Wire Wire Line
	3300 4600 2750 4600
Wire Wire Line
	3300 4400 2750 4400
Wire Wire Line
	3300 4200 2750 4200
Wire Wire Line
	4100 4500 4650 4500
Wire Wire Line
	4100 4300 4650 4300
Wire Wire Line
	4100 4200 4650 4200
Wire Wire Line
	4100 4400 4650 4400
Wire Wire Line
	4100 4600 4650 4600
Wire Wire Line
	3300 4300 2750 4300
Wire Wire Line
	3300 4500 2750 4500
Wire Wire Line
	7700 3650 8200 3650
Wire Wire Line
	6000 4150 5500 4150
Wire Wire Line
	6000 4350 5500 4350
Wire Wire Line
	6000 4550 5500 4550
Wire Wire Line
	6000 4850 5500 4850
$Comp
L GND #PWR01
U 1 1 4F359796
P 3400 3150
F 0 "#PWR01" H 3400 3150 30  0001 C CNN
F 1 "GND" H 3400 3080 30  0001 C CNN
	1    3400 3150
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 4F359783
P 3400 3050
F 0 "#FLG02" H 3400 3320 30  0001 C CNN
F 1 "PWR_FLAG" H 3400 3280 30  0000 C CNN
	1    3400 3050
	1    0    0    -1  
$EndComp
Text Label 5500 4850 0    60   ~ 0
RED
Text Label 5500 4750 0    60   ~ 0
GREEN
Text Label 5500 4650 0    60   ~ 0
BLUE
Text Label 5500 4550 0    60   ~ 0
FREQ
Text Label 5500 4450 0    60   ~ 0
S3
Text Label 5500 4350 0    60   ~ 0
S2
Text Label 5500 4250 0    60   ~ 0
S1
Text Label 5500 4150 0    60   ~ 0
S0
NoConn ~ 6000 4050
NoConn ~ 6000 3950
Text Label 8200 3850 2    60   ~ 0
5V
Text Label 8200 3650 2    60   ~ 0
GND
NoConn ~ 6000 4950
NoConn ~ 7700 4950
NoConn ~ 7700 4850
NoConn ~ 7700 4750
NoConn ~ 7700 4650
NoConn ~ 7700 4550
NoConn ~ 7700 4450
NoConn ~ 7700 4350
NoConn ~ 7700 4250
NoConn ~ 7700 4150
NoConn ~ 7700 4050
NoConn ~ 7700 3950
NoConn ~ 7700 3750
NoConn ~ 7700 3550
NoConn ~ 6000 3850
NoConn ~ 6000 3750
NoConn ~ 6000 3650
NoConn ~ 6000 3550
Text Label 4650 4200 2    60   ~ 0
RED
Text Label 4650 4300 2    60   ~ 0
GREEN
Text Label 4650 4400 2    60   ~ 0
BLUE
Text Label 4650 4500 2    60   ~ 0
FREQ
Text Label 4650 4600 2    60   ~ 0
S3
Text Label 2750 4600 0    60   ~ 0
S2
Text Label 2750 4500 0    60   ~ 0
S1
Text Label 2750 4400 0    60   ~ 0
S0
Text Label 2750 4300 0    60   ~ 0
GND
Text Label 2750 4200 0    60   ~ 0
5V
$Comp
L CONN_5X2 P1
U 1 1 4F3592AD
P 3700 4400
F 0 "P1" H 3700 4700 60  0000 C CNN
F 1 "CONN_5X2" V 3700 4400 50  0000 C CNN
	1    3700 4400
	1    0    0    -1  
$EndComp
$Comp
L ARDUINO_NANO U1
U 1 1 4F359286
P 6850 4300
F 0 "U1" H 6400 5250 60  0000 C CNN
F 1 "ARDUINO_NANO" H 6850 3450 60  0000 C CNN
	1    6850 4300
	1    0    0    -1  
$EndComp
$EndSCHEMATC
