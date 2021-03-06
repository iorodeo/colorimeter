EESchema Schematic File Version 2  date Thu 15 May 2014 10:00:42 AM PDT
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
LIBS:led_5050
LIBS:led_ver_B-cache
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title ""
Date "15 may 2014"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	6100 3650 6970 3650
Wire Wire Line
	6970 3650 6970 3440
Wire Wire Line
	6970 2350 6970 3040
Wire Wire Line
	4700 4550 4700 4750
Wire Wire Line
	4740 2380 4740 2680
Wire Wire Line
	7170 2750 7170 2350
Wire Wire Line
	4700 4050 4700 3650
Wire Wire Line
	4700 3650 5300 3650
Wire Wire Line
	6670 3240 6470 3240
Wire Wire Line
	6470 3240 6470 2650
Wire Wire Line
	6470 2650 6870 2650
Wire Wire Line
	6870 2650 6870 2350
Text Label 6970 2350 3    60   ~ 0
9V
NoConn ~ 7070 2350
$Comp
L NPN Q1
U 1 1 537445AC
P 6870 3240
F 0 "Q1" H 6870 3090 50  0000 R CNN
F 1 "NPN" H 6870 3390 50  0000 R CNN
	1    6870 3240
	1    0    0    -1  
$EndComp
NoConn ~ 5300 3790
NoConn ~ 6100 3790
NoConn ~ 6100 3510
NoConn ~ 5300 3510
$Comp
L LED_5050 D1
U 1 1 537440C2
P 5700 3650
F 0 "D1" H 5695 3960 60  0000 C CNN
F 1 "LED_5050" H 5705 3345 60  0000 C CNN
	1    5700 3650
	1    0    0    -1  
$EndComp
Text Label 6870 2350 3    60   ~ 0
Blue
$Comp
L CONN_4 P1
U 1 1 4F345F7F
P 7020 2000
F 0 "P1" V 6970 2000 50  0000 C CNN
F 1 "CONN_4" V 7070 2000 50  0000 C CNN
	1    7020 2000
	0    -1   -1   0   
$EndComp
Text Label 7170 2750 0    60   ~ 0
GND
Text Label 4740 2680 0    60   ~ 0
GND
$Comp
L R R1
U 1 1 4F035CCA
P 4700 4300
F 0 "R1" V 4780 4300 50  0000 C CNN
F 1 "R" V 4700 4300 50  0000 C CNN
	1    4700 4300
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR01
U 1 1 4F035C98
P 4700 4750
F 0 "#PWR01" H 4700 4750 30  0001 C CNN
F 1 "GND" H 4700 4680 30  0001 C CNN
	1    4700 4750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 4F035C8B
P 7170 2750
F 0 "#PWR02" H 7170 2750 30  0001 C CNN
F 1 "GND" H 7170 2680 30  0001 C CNN
	1    7170 2750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 4F035C86
P 4740 2680
F 0 "#PWR03" H 4740 2680 30  0001 C CNN
F 1 "GND" H 4740 2610 30  0001 C CNN
	1    4740 2680
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG04
U 1 1 4F035C7F
P 4740 2380
F 0 "#FLG04" H 4740 2650 30  0001 C CNN
F 1 "PWR_FLAG" H 4740 2610 30  0000 C CNN
	1    4740 2380
	1    0    0    -1  
$EndComp
Text Label 4700 4750 0    60   ~ 0
GND
$EndSCHEMATC
