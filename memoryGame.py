#!/usr/bin/env python
"""
memoryGame.py
Simple memory game for use with pfio and the RaspberryPi interface (piface)

Objective of the game: You must remember an ever increasing sequence of flashes and input them correctly*

"""
from __future__ import print_function
from time import sleep 		# for delays
import random			# for random sequence generation
import pifacedigitalio as pfio			# piface library




pfio.init()			# initialise pfio (sets up the spi transfers)

pfd = pfio.PiFaceDigital()			# create pifacedigital object

colours = ["Red","Green","Blue","Yellow","White"]		# colour names for printing to screen

def signifyTurn(turn):
	global screen_output

	sleep(0.4)
	pfd.output_port.value = 0xFF				# signify it is their turn by turning all the LEDs on then off
	sleep(0.3)
	pfd.output_port.value = 0x0

	if screen_output:
		if turn:
			print ("\nYour turn!")
		else:
			print ("\nMy turn!")

def screenOutput(i):
	global colours
	if screen_output:			# print the colour to the screen
		print (colours[i])

def nextColour():
	""" choses a random number between 0 and 3 to represent the coloured leds and their corresponding buttons"""
	return 1<< random.randint(0,3) 


first_in_sequence = nextColour()	# create the first colour in the sequence

array = [first_in_sequence]		# add the first colour to the array

game = 1				# keep track of game active (1 for active, 0 for game over)
score = 0				# keep track of player's score
screen_output = False			# choice to write colours and cues to the screen


sleep(1) # let them get their bearings

while game:						# while game in play
	
	game_round = score+1				
	
	if screen_output:				# print the round number
		print ("\nRound {}!".format(game_round))
		
	for n in array:					# for each colour in current sequence (flash the sequence)

		pfd.output_port.value = n			# turn the colour on
	
		
		screenOutput(n)
			
		sleep(0.5)				# wait to keep the colour showing 
		pfd.output_port.value = 0		# turn the colour off
		sleep(0.2)				# small break between colours
		

	signifyTurn(1)


	for i in array:						# for each colour in current sequence (check against inputted sequence)
		
		while (pfd.input_port.value!= 0):		# wait till no buttons pressed
			sleep(0.001)					# delay
				
		while (pfd.input_port.value == 0):					# wait for any input 
			sleep(0.001)
		event = pfd.input_port.value
		sleep(0.001)						# delay
		
		screenOutput(i)
		
		pfd.output_port.value = pfd.input_port.value			# light up the buttons pressed
		
		if event != i:	
			game = 0					# if any wrong buttons were pressed end the game
			break

		else:							# otherwise the correct button was pressed
			previous = event
			event = pfd.input_port.value
			
			while previous == event:				# while the button is held down, wait
				event = pfd.input_port.value
				
			pfd.output_port.value = 0			# turn the button's LED off
			
			
	signifyTurn(0)

	if game:
		next = nextColour()		# set next colour
		while next == array[-1]:	# ensure the same colour isn't chosen twice in a row
			next = nextColour()
		
		array.append(next)		# add another colour to the sequence
		score +=1			# increment the score counter
		sleep(0.4)			# small break before flashing the new extended sequence



pfd.output_port.value = 0			# if the game has been lost, set all the button leds off

print ("Your score was {}".format(score)) 	# print the players score

