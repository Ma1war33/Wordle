import os
import sys

#gets file path
filepath = sys.argv[0]
filepath = filepath[:-7]

import funcs #funcs.py file

try:
    from PyDictionary import PyDictionary
except:
    print("\n\033[38;5;196mERROR: Failed to import PyDictionary.\033[0m")
    print(funcs.colour.GREY + "Please make sure it is installed, see below for more detail:" + funcs.colour.BASE + "\n") 

dictionary=PyDictionary()

#clears terminal
def clearterminal():
    os.system('cls' if os.name == 'nt' else 'clear')

wordle = funcs.wordle()
coloured_guess = []
clearterminal() #runs function to clear terminal

global answer
answer = wordle.getanswer() #gets random 5 letter word (answer)
clearterminal()


print("\033[38;1;256mABCDEFGHIJKLMNOPQRSTUVWXYZ\033[0m") #welcome message
print("\n")

global guessno
guessno =1

def define():
    global definition
    print("\n")

    for i in range(len(list(definition.values())[0])):
        try:
            x = (list(definition.values())[0])[i][0]
        except:
            pass
        if x == "(":
            pass
        else:
            list(definition.values())[0][i] = list(definition.values())[0][i].replace(" (", "; ")
            print(funcs.colour.GREY + "* " + (list(definition.values())[0])[i].strip() + funcs.colour.BASE)
        if i > 1:
            break
    
    print("\n")


#runs on correct guess
def win():
    global answer
    print("\n")
    print("Correct! The answer was " + funcs.colour.GREEN_TEXT + answer.strip() + "\033[0m.")
    print("You got it in " + str(guessno-1) + " tries!")

    global definition
    answer = answer.strip()
    try:
        definition = dictionary.meaning(str(answer))
    except:
        definition = {"":["ERROR: definition not found", "please check your internet connection"]}
        define()
    quit()

#gets guess from player
def get_guess():
    global guess
    guess = input("Guess " + str(guessno) + "/6: ")

get_guess()

#reprints previous (cleared) messages
def reprint():
    clearterminal()

    print(funcs.letters_coloured_str) #alphabet at the top
    print("\n")
    for i in range(len(coloured_guess)): #previous guesses + current guess
        if i <funcs.number_of_allowed_guesses-1:
            print("Guess " + str(i+1) + "/6: " + coloured_guess[i])

#check if guess is a valid word and compares guess to answer using funcs.py
def check_guess():
    global guessno
    global coloured_guess

    if wordle.wordchecker(guess) == True:  #checks if guess is a word
        coloured_guess.append(wordle.guesschecker(guess)) #adds guess(coloured) to list of previous guesses(coloured)
        guessno+=1

        reprint()

        if wordle.answercheck(guess) == True: #checks if guess is answer
            win()

        if guessno <int(funcs.number_of_allowed_guesses): #gets next guess
            get_guess()

        if guessno <(int(funcs.number_of_allowed_guesses)+1): #loop
            check_guess()
        
    else:
        #restarts if guess is not a valid word
        clearterminal()
        reprint()

        get_guess()
        check_guess()

check_guess()

global definition
answer = answer.strip()
try:
    sys.stdout = open(os.devnull, 'w')
    definition = dictionary.meaning(str(answer))
    sys.stdout = sys.__stdout__

    if definition == None:
        definition = {"":["\n\033[38;5;196mERROR: failed to get definition\033[0m", "please check your internet connection"]}
    else:
        definition=definition
except:
    definition = {"":["\n\033[38;5;196mERROR: failed to get definition\033[0m", "please check your internet connection"]}

print("\n")
print("The answer was " + funcs.colour.GREEN_TEXT + answer.strip() + "\033[0m.")

define()