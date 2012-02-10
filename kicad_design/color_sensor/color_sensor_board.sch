EESchema Schematic File Version 2  date Thu 09 Feb 2012 05:50:30 PM PST
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
LIBS:tcs3200
LIBS:ping_breakout-cache
LIBS:color_sensor_board-cache
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
Text Label 5000 3300 0    60   ~ 0
GND
Text Label 5000 3200 0    60   ~ 0
red
Text Label 5000 3100 0    60   ~ 0
green
Text Label 5000 3000 0    60   ~ 0
blue
Wire Wire Line
	5450 3300 5000 3300
Wire Wire Line
	5450 3100 5000 3100
Wire Wire Line
	5350 2500 5000 2500
Wire Wire Line
	5350 2300 5000 2300
Wire Wire Line
	5350 2100 5000 2100
Wire Wire Line
	6150 2400 6500 2400
Wire Wire Line
	6150 2200 6500 2200
Wire Wire Line
	3650 2550 3650 2650
Wire Wire Line
	9000 3350 9500 3350
Wire Wire Line
	7650 3350 7900 3350
Wire Wire Line
	7900 3200 7650 3200
Wire Wire Line
	9000 2900 9500 2900
Wire Wire Line
	9300 3900 9300 4200
Wire Wire Line
	7900 2900 7400 2900
Wire Wire Line
	9000 3200 9500 3200
Wire Wire Line
	9300 3500 9300 3350
Connection ~ 9300 3350
Wire Wire Line
	7900 3050 7400 3050
Wire Wire Line
	9000 3050 9500 3050
Wire Wire Line
	7650 3200 7650 3750
Connection ~ 7650 3350
Wire Wire Line
	6150 2100 6500 2100
Wire Wire Line
	6150 2300 6500 2300
Wire Wire Line
	6150 2500 6500 2500
Wire Wire Line
	5350 2200 5000 2200
Wire Wire Line
	5350 2400 5000 2400
Wire Wire Line
	5450 3000 5000 3000
Wire Wire Line
	5450 3200 5000 3200
$Comp
L CONN_4 P2
U 1 1 4F347703
P 5800 3150
F 0 "P2" V 5750 3150 50  0000 C CNN
F 1 "CONN_4" V 5850 3150 50  0000 C CNN
	1    5800 3150
	1    0    0    -1  
$EndComp
Text Label 6500 2100 2    60   ~ 0
red
Text Label 6500 2200 2    60   ~ 0
green
Text Label 6500 2300 2    60   ~ 0
blue
Text Label 6500 2400 2    60   ~ 0
FREQ
Text Label 6500 2500 2    60   ~ 0
S3
Text Label 5000 2500 0    60   ~ 0
S2
Text Label 5000 2400 0    60   ~ 0
S1
Text Label 5000 2300 0    60   ~ 0
S0
Text Label 5000 2200 0    60   ~ 0
GND
Text Label 5000 2100 0    60   ~ 0
5V
$Comp
L CONN_5X2 P1
U 1 1 4F0CA3A1
P 5750 2300
F 0 "P1" H 5750 2600 60  0000 C CNN
F 1 "CONN_5X2" V 5750 2300 50  0000 C CNN
	1    5750 2300
	1    0    0    -1  
$EndComp
Text Label 3650 2650 2    60   ~ 0
GND
$Comp
L GND #PWR01
U 1 1 4E9F32BE
P 3650 2650
F 0 "#PWR01" H 3650 2650 30  0001 C CNN
F 1 "GND" H 3650 2580 30  0001 C CNN
	1    3650 2650
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 4E9F32AB
P 3650 2550
F 0 "#FLG02" H 3650 2820 30  0001 C CNN
F 1 "PWR_FLAG" H 3650 2780 30  0000 C CNN
	1    3650 2550
	1    0    0    -1  
$EndComp
Text Label 7400 2900 0    60   ~ 0
S0
Text Label 7400 3050 0    60   ~ 0
S1
Text Label 9500 2900 2    60   ~ 0
S3
Text Label 9500 3050 2    60   ~ 0
S2
Text Label 7650 3750 2    60   ~ 0
GND
$Comp
L GND #PWR03
U 1 1 4E9F2B4B
P 7650 3750
F 0 "#PWR03" H 7650 3750 30  0001 C CNN
F 1 "GND" H 7650 3680 30  0001 C CNN
	1    7650 3750
	1    0    0    -1  
$EndComp
Text Label 9300 4150 0    60   ~ 0
GND
$Comp
L GND #PWR04
U 1 1 4E9F2A66
P 9300 4200
F 0 "#PWR04" H 9300 4200 30  0001 C CNN
F 1 "GND" H 9300 4130 30  0001 C CNN
	1    9300 4200
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 4E9F2A04
P 9300 3700
F 0 "C1" H 9350 3800 50  0000 L CNN
F 1 "0.1 uF" H 9350 3600 50  0000 L CNN
	1    9300 3700
	1    0    0    -1  
$EndComp
Text Label 9500 3200 2    60   ~ 0
FREQ
Text Label 9500 3350 2    60   ~ 0
5V
$Comp
L TCS3200 U1
U 1 1 4E9F1F08
P 7850 4000
F 0 "U1" H 8400 5300 60  0000 C CNN
F 1 "TCS3200" V 8450 4900 60  0000 C CNN
	1    7850 4000
	1    0    0    -1  
$EndComp
$EndSCHEMATC
