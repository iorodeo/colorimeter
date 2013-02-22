EESchema Schematic File Version 2  date Thu 03 Jan 2013 03:06:48 PM PST
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
LIBS:rgb_multiled
LIBS:rgb_led_board-cache
EELAYER 25  0
EELAYER END
$Descr A4 11693 8268
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
Text Label 7000 3150 2    60   ~ 0
red
Text Label 7000 2950 2    60   ~ 0
green
Wire Wire Line
	6550 3150 7000 3150
Wire Wire Line
	6550 2750 7000 2750
Wire Wire Line
	9300 3000 8700 3000
Wire Wire Line
	9300 2800 8700 2800
Wire Wire Line
	4800 3800 4800 2750
Wire Wire Line
	4800 2750 5650 2750
Wire Wire Line
	4800 4300 4800 4500
Wire Wire Line
	5300 4300 5300 4500
Wire Wire Line
	2700 1900 2700 2200
Wire Wire Line
	5650 3150 5300 3150
Wire Wire Line
	5300 3150 5300 3800
Wire Wire Line
	5050 4300 5050 4500
Wire Wire Line
	5650 2950 5050 2950
Wire Wire Line
	5050 2950 5050 3800
Wire Wire Line
	9300 2700 8700 2700
Wire Wire Line
	9300 2900 8700 2900
Wire Wire Line
	8700 3000 8700 3400
Wire Wire Line
	6550 2950 7000 2950
Text Label 7000 2750 2    60   ~ 0
blue
Text Label 8700 2900 0    60   ~ 0
red
Text Label 8700 2800 0    60   ~ 0
green
Text Label 8700 2700 0    60   ~ 0
blue
$Comp
L CONN_4 P1
U 1 1 4F345F7F
P 9650 2850
F 0 "P1" V 9600 2850 50  0000 C CNN
F 1 "CONN_4" V 9700 2850 50  0000 C CNN
	1    9650 2850
	1    0    0    -1  
$EndComp
Text Label 4800 4500 0    60   ~ 0
GND
Text Label 5050 4500 0    60   ~ 0
GND
Text Label 5300 4500 0    60   ~ 0
GND
Text Label 8700 3400 0    60   ~ 0
GND
Text Label 2700 2200 0    60   ~ 0
GND
$Comp
L RGB_MULTILED U1
U 1 1 4F035E14
P 6100 2950
F 0 "U1" H 6050 3350 60  0000 C CNN
F 1 "RGB_MULTILED" H 6100 2550 60  0000 C CNN
	1    6100 2950
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 4F035CD1
P 5300 4050
F 0 "R3" V 5380 4050 50  0000 C CNN
F 1 "150" V 5300 4050 50  0000 C CNN
	1    5300 4050
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 4F035CCF
P 5050 4050
F 0 "R2" V 5130 4050 50  0000 C CNN
F 1 "90" V 5050 4050 50  0000 C CNN
	1    5050 4050
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 4F035CCA
P 4800 4050
F 0 "R1" V 4880 4050 50  0000 C CNN
F 1 "90" V 4800 4050 50  0000 C CNN
	1    4800 4050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 4F035C98
P 4800 4500
F 0 "#PWR01" H 4800 4500 30  0001 C CNN
F 1 "GND" H 4800 4430 30  0001 C CNN
	1    4800 4500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 4F035C96
P 5300 4500
F 0 "#PWR02" H 5300 4500 30  0001 C CNN
F 1 "GND" H 5300 4430 30  0001 C CNN
	1    5300 4500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 4F035C94
P 5050 4500
F 0 "#PWR03" H 5050 4500 30  0001 C CNN
F 1 "GND" H 5050 4430 30  0001 C CNN
	1    5050 4500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 4F035C8B
P 8700 3400
F 0 "#PWR04" H 8700 3400 30  0001 C CNN
F 1 "GND" H 8700 3330 30  0001 C CNN
	1    8700 3400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 4F035C86
P 2700 2200
F 0 "#PWR05" H 2700 2200 30  0001 C CNN
F 1 "GND" H 2700 2130 30  0001 C CNN
	1    2700 2200
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG06
U 1 1 4F035C7F
P 2700 1900
F 0 "#FLG06" H 2700 2170 30  0001 C CNN
F 1 "PWR_FLAG" H 2700 2130 30  0000 C CNN
	1    2700 1900
	1    0    0    -1  
$EndComp
$EndSCHEMATC
