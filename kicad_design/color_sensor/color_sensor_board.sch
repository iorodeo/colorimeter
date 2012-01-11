EESchema Schematic File Version 2  date Tue 10 Jan 2012 01:09:11 PM PST
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
Date "10 jan 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 5250 4050 2    60   ~ 0
RED
Text Label 5250 4150 2    60   ~ 0
GREEN
Text Label 5250 4250 2    60   ~ 0
BLUE
Text Label 5250 4350 2    60   ~ 0
FREQ
Text Label 5250 4450 2    60   ~ 0
S3
Text Label 3750 4450 0    60   ~ 0
S2
Text Label 3750 4350 0    60   ~ 0
S1
Text Label 3750 4250 0    60   ~ 0
S0
Text Label 3750 4150 0    60   ~ 0
GND
Text Label 3750 4050 0    60   ~ 0
5V
Wire Wire Line
	4100 4450 3750 4450
Wire Wire Line
	4100 4250 3750 4250
Wire Wire Line
	4100 4050 3750 4050
Wire Wire Line
	4900 4350 5250 4350
Wire Wire Line
	4900 4150 5250 4150
Wire Wire Line
	6250 3950 5950 3950
Wire Wire Line
	3650 2550 3650 2650
Wire Wire Line
	8900 4400 9400 4400
Wire Wire Line
	7550 4400 7800 4400
Wire Wire Line
	7800 4250 7550 4250
Wire Wire Line
	8900 3950 9400 3950
Wire Wire Line
	9200 4950 9200 5250
Wire Wire Line
	7800 3950 7300 3950
Wire Wire Line
	8900 4250 9400 4250
Wire Wire Line
	9200 4550 9200 4400
Connection ~ 9200 4400
Wire Wire Line
	7800 4100 7300 4100
Wire Wire Line
	8900 4100 9400 4100
Wire Wire Line
	7550 4250 7550 4800
Connection ~ 7550 4400
Wire Wire Line
	5950 4300 6250 4300
Wire Wire Line
	6250 4500 5950 4500
Wire Wire Line
	6250 4150 5950 4150
Wire Wire Line
	4900 4050 5250 4050
Wire Wire Line
	4900 4250 5250 4250
Wire Wire Line
	4900 4450 5250 4450
Wire Wire Line
	4100 4150 3750 4150
Wire Wire Line
	4100 4350 3750 4350
$Comp
L CONN_5X2 P1
U 1 1 4F0CA3A1
P 4500 4250
F 0 "P1" H 4500 4550 60  0000 C CNN
F 1 "CONN_5X2" V 4500 4250 50  0000 C CNN
	1    4500 4250
	1    0    0    -1  
$EndComp
Text Label 5950 4150 0    60   ~ 0
GREEN
Text Label 5950 3950 0    60   ~ 0
BLUE
$Comp
L CONN_2 P3
U 1 1 4EA0C6DF
P 6600 4050
F 0 "P3" V 6550 4050 40  0000 C CNN
F 1 "CONN_2" V 6650 4050 40  0000 C CNN
	1    6600 4050
	1    0    0    -1  
$EndComp
Text Label 5950 4300 0    60   ~ 0
RED
Text Label 5950 4500 0    60   ~ 0
GND
$Comp
L CONN_2 P2
U 1 1 4E9F77B0
P 6600 4400
F 0 "P2" V 6550 4400 40  0000 C CNN
F 1 "CONN_2" V 6650 4400 40  0000 C CNN
	1    6600 4400
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
Text Label 7300 3950 0    60   ~ 0
S0
Text Label 7300 4100 0    60   ~ 0
S1
Text Label 9400 3950 2    60   ~ 0
S3
Text Label 9400 4100 2    60   ~ 0
S2
Text Label 7550 4800 2    60   ~ 0
GND
$Comp
L GND #PWR03
U 1 1 4E9F2B4B
P 7550 4800
F 0 "#PWR03" H 7550 4800 30  0001 C CNN
F 1 "GND" H 7550 4730 30  0001 C CNN
	1    7550 4800
	1    0    0    -1  
$EndComp
Text Label 9200 5200 0    60   ~ 0
GND
$Comp
L GND #PWR04
U 1 1 4E9F2A66
P 9200 5250
F 0 "#PWR04" H 9200 5250 30  0001 C CNN
F 1 "GND" H 9200 5180 30  0001 C CNN
	1    9200 5250
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 4E9F2A04
P 9200 4750
F 0 "C1" H 9250 4850 50  0000 L CNN
F 1 "0.1 uF" H 9250 4650 50  0000 L CNN
	1    9200 4750
	1    0    0    -1  
$EndComp
Text Label 9400 4250 2    60   ~ 0
FREQ
Text Label 9400 4400 2    60   ~ 0
5V
$Comp
L TCS3200 U1
U 1 1 4E9F1F08
P 7750 5050
F 0 "U1" H 8300 6350 60  0000 C CNN
F 1 "TCS3200" V 8350 5950 60  0000 C CNN
	1    7750 5050
	1    0    0    -1  
$EndComp
$EndSCHEMATC
