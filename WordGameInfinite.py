#!/usr/env python3
#Ben King
#Shoutout 3B1B for the word lists.
import random
import os
import string

user_input = input("5 or 6 letter game?: 5/6 ")
if user_input == str(5) or str(6):
    LENGTH_OF_WORD = int(user_input)
else:
    print("Bad input.")
NUMBER_OF_GUESSES=6

#Initialize alphabet list object
alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string)

#Used for colorful output of letters
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Create allowed guess list
if LENGTH_OF_WORD == 5:
    f = open("allow.txt", "r")
elif LENGTH_OF_WORD == 6:
    f = open("6allow.txt", "r")
allowed_words = f.read().splitlines()
f.close()

#Generates a random word from guesslist.
def select_word(fiveorsix):
    if fiveorsix == 5:
        f = open("possible.txt", "r")
    elif fiveorsix == 6:
        f = open("6possible.txt", "r")
    guesslist = f.read().splitlines()
    f.close()
    guessword = guesslist[random.randint(0, len(guesslist))]
    return(guessword)

#Main Game Function
def play_wordle(true_word, alphabet_dict):

    remaining_guesses = NUMBER_OF_GUESSES

    while remaining_guesses > 0:
        # Create Colorful 'Keyboard'
        row1,row2,row3 = qwerty(alphabet_dict)

        guess_number = NUMBER_OF_GUESSES - (remaining_guesses - 1)
        #Ensure guess is a valid 5-letter word
        bad_input = 1
        while bad_input == 1:
            print("=====================")
            print(" " + row1)
            print("  " + row2)
            print("   " + row3)
            print("=====================")
            #Prompt user for a guess
            guess_word = input(str(remaining_guesses) + " guesses left. Enter your guess: \n").upper()
            if guess_word.lower() in allowed_words:
                bad_input = 0
            else:
                print("Not a valid guess. Try again.")
            print("\n")
        if guess_word.lower() == true_word:
            print("WINNER! Word was " + true_word.upper())
            remaining_guesses = remaining_guesses + 1
            return(1)
        else:
            #Determine correct letters, position, update tracking dict
            alphabet_dict = analyze_guess(true_word.upper(), guess_word.upper(), alphabet_dict, guess_number)

            #Show colorful history of guesses
            print("      =======")
            show_guess_board()
            print("      =======")
            print("\n")
        #Holy workaround batman
        if remaining_guesses == 1:
            print("Close one! No more guesses. The word was: " + true_word.upper())
            remaining_guesses = remaining_guesses - 1
        else:
            remaining_guesses = remaining_guesses - 1
    return(0)
        
#Set up qwerty keyboard from alphabet
def qwerty(alphabet_dict):
    row1 = "QWERTYUIOP"
    row1out = qwertyhelper(row1, alphabet_dict)
    row2 = "ASDFGHJKL"
    row2out = qwertyhelper(row2, alphabet_dict)
    row3 = "ZXCVBNM"
    row3out = qwertyhelper(row3, alphabet_dict)
    return(row1out, row2out, row3out)

#Helper function to color in qwerty keyboard
def qwertyhelper(row_raw, alphabet_dict):
    rowoutput = ""
    for letter in row_raw:
        if alphabet_dict[letter] == 3:
            rowoutput = rowoutput + bcolors.OKGREEN + letter + bcolors.ENDC + " "
        elif alphabet_dict[letter] == 2:
            rowoutput = rowoutput + bcolors.OKCYAN + letter + bcolors.ENDC + " "
        elif alphabet_dict[letter] == 1:
            rowoutput = rowoutput + bcolors.FAIL + letter + bcolors.ENDC + " "
        else:
            rowoutput = rowoutput + bcolors.WARNING + letter + bcolors.ENDC + " "
    return(rowoutput)

#Helper function to output guess_board dict
def show_guess_board():
    for item in range(1, (len(guess_board.keys())+1)):
        print("      |" + guess_board[item] + "|")
#Takes target word, guessed word, compares with helper function, updates dict, returns
def analyze_guess(true_word, guess_word, alphabet_dict, guess_no):
    letter_pos = 0
    guess_board[guess_no] = ""
    while letter_pos < LENGTH_OF_WORD:
        alphabet_dict = guess_helper(true_word, guess_word, letter_pos, alphabet_dict, guess_no)
        letter_pos = letter_pos + 1
    return(alphabet_dict)

#Does the bulk of comparing words, updating tracking dict
def guess_helper(true_word, guess_word, letter_pos, alphabet_dict, guess_no):
    curr_letter = guess_word[letter_pos]
    
    #Green, exact match
    if curr_letter == true_word[letter_pos]:
        alphabet_dict[curr_letter] = 3
        guess_board[guess_no] = guess_board[guess_no] + bcolors.OKGREEN + curr_letter + bcolors.ENDC
    #Cyan, letter somewhere else in word
    elif curr_letter in true_word:
        #Don't ever change a green letter to a cyan letter in alphabet_dict
        if alphabet_dict[curr_letter] < 2:
            alphabet_dict[curr_letter] = 2
        guess_board[guess_no] = guess_board[guess_no] + bcolors.OKCYAN + curr_letter + bcolors.ENDC
    else:
        #Change yellows to reds if not in word
        if alphabet_dict[curr_letter] == 0:
            alphabet_dict[curr_letter] = 1
        guess_board[guess_no] = guess_board[guess_no] + bcolors.FAIL + curr_letter + bcolors.ENDC
    return(alphabet_dict)

#Run game function
streak = 0
play_again = 1

while(play_again == 1):
    #Initialize alphabet tracking dict, previous guess tracking dict, winner status (you start as a loser) 
    alphabet_dict = {}
    for letter in alphabet_list:
        alphabet_dict[letter] = 0
    # 0 - Not used yet
    # 1 - Used, not in word
    # 2 - Used, Letter in wrong position
    # 3 - Used, Letter in correct position
    guess_board = {}
    result = play_wordle(select_word(LENGTH_OF_WORD), alphabet_dict)
    if result == 1:
        streak = streak + 1
    else:
        streak = 0
    play_again = input("Your streak is " + str(streak) + ". Play again? 1 or 0: ")
    if play_again == str(1) or play_again == str(0):
        play_again = int(play_again)
    else:
        print("Bad input. Your streak is GONE!")
