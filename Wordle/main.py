import funcs #funcs.py file
import os
from PyDictionary import PyDictionary

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

global definition
answer = answer.strip()
try:
    definition = dictionary.meaning(str(answer))
except:
    definition = {"":["ERROR: definition not found", "please check your internet connection"]}

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
    print("\n")
    print("Correct! The answer was " + funcs.colour.GREEN_TEXT + answer.strip() + "\033[0m.")
    print("You got it in " + str(guessno) + " tries!")

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
        if i <6:
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

print("\n")
print("The answer was " + funcs.colour.GREEN_TEXT + answer.strip() + "\033[0m.")

define()