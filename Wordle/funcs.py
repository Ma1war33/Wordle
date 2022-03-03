import random
import sys

#gets file path
filepath = sys.argv[0]
filepath = filepath[:-7]
print("\033[38;5;32mFile directory: " + str(filepath))
print("Running...\033[0m")

#reads preferences file
with open(filepath + "preferences.txt", "r") as preferences:
    x =preferences.readlines()
    colourblind_mode =x[0]
    colourblind_mode =colourblind_mode.split()
    colourblind_mode =colourblind_mode[2].strip()

    infinite_guesses =x[3]
    infinite_guesses =infinite_guesses.split()
    infinite_guesses =infinite_guesses[2].strip()

number_of_allowed_guesses = 7
if infinite_guesses == "True":
    number_of_allowed_guesses = 999999999
elif infinite_guesses == "False":
    number_of_allowed_guesses = 7

class colour:
    #defines ANSI colours depending on whether colourblind mode is enabled
    if colourblind_mode == "True":
        GREEN = "\033[48;5;32m"
        GREEN_TEXT = "\033[38;5;32m"
    elif colourblind_mode == "False":
        GREEN = "\033[48;5;34m"
        GREEN_TEXT = "\033[38;5;34m"
    else:
        print("error")

    YELLOW = "\033[48;5;208m"
    GREY = "\033[38;5;243m"
    DARKGREY = "\033[38;5;237m"
    YELLOW_TEXT = "\033[38;5;208m"
    WHITE = "\033[38;5;256m"
    BASE = "\033[0m"
    BOLD = "\033[1m"

#defining some varialbes
class alphabet:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    letter_count = {}

letters_coloured_str ="ABCDEFGHIJKLMNOPQRSTUVWYXYZ"

global already_coloured_letters
already_coloured_letters = {}

#setting all letters in dict to false
for each in alphabet.alphabet:
    already_coloured_letters[each] = False

class wordle():
    global letters_coloured
    global letters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    letters_coloured = letters

    #Gets a random word from "answers.txt"
    def getanswer(self):
        with open(filepath + "wordlists/answers.txt", "r") as answers:
            answers_list =answers.readlines()
            answer_number =random.randint(0, (len(answers_list)-1))

            global answer
            answer =answers_list[answer_number]

        print("\033[8m" + str(answer) + colour.BASE)
        return answer

    #checks if guess is a word
    def wordchecker(self, guess):
        with open(filepath + "wordlists/words.txt", "r") as words:
            word_list =words.readlines()
        
        for i in range(len(word_list)):
            if guess == word_list[i].strip():
                return True
    
    #checks if guess is the answer
    def answercheck(self, guess):
        guess =str(guess)
        return(guess.strip() == answer.strip())

    #compares guess to answer (colours + highlights guess)
    def guesschecker(self, guess):
        global letters_coloured_str
        guess =str(guess)

        #word --> list
        guess_list =list(guess)
        guess_list_coloured = list(guess)
        answer_list =list(answer)
        
        global number_of_y_letters
        number_of_y_letters = {}

        for each in alphabet.alphabet:
            number_of_y_letters[each] = 0

        #comparing guess to ansmwer
        for i in range(len(guess_list)):
            if guess_list[i] == answer_list[i]:
                #If letters and the same and in the same position they are coloured GREEN
                guess_list_coloured[i] =colour.GREEN+guess_list[i]+colour.BASE

                #related to alphabet displayed above
                x = alphabet.alphabet.index(guess_list[i])
                letters_coloured[x] = colour.GREEN_TEXT + alphabet.alphabet[x].upper() + colour.BASE
                already_coloured_letters[alphabet.alphabet[x]] =True

                number_of_y_letters[guess_list[i]] +=1
                try:
                    z =guess_list_coloured.index(colour.YELLOW+guess_list[i]+colour.BASE)
                    guess_list_coloured[z] =guess_list[i]
                except:
                    pass
            else:
                #Counts number of each letter in answer
                for l in range(len(alphabet.alphabet)):
                    alphabet.letter_count[alphabet.alphabet[l]]= answer_list.count(alphabet.alphabet[l])
                
                #highlights yellow the letters that are in the answer but not in the correct position
                #highlights the letters while the [letters highlighted] is less than the [total number of one letter in answer] for each letter
                if int(number_of_y_letters[guess_list[i]]) < int(alphabet.letter_count[guess_list[i]]):
                    guess_list_coloured[i] =colour.YELLOW+guess_list[i]+colour.BASE
                    number_of_y_letters[guess_list[i]] +=1
    
        #Combining list into str
        guess_coloured =""
        for i in guess_list_coloured:
            guess_coloured +=i

        #Makes alphabet at top coloured
        for i in range(len(letters)):
            
            #doesn't colour letters that have already been coloured
            if already_coloured_letters[alphabet.alphabet[i]] == False:
                
                if alphabet.alphabet[i] in answer_list and alphabet.alphabet[i] in guess_list: #If guessed letter is in answer
                    if answer_list.index(alphabet.alphabet[i]) == guess_list.index(alphabet.alphabet[i]): #if the letters are in the same position in the word
                        letters_coloured[i] = colour.GREEN_TEXT + alphabet.alphabet[i].upper() + colour.BASE #colours the letter green
                        already_coloured_letters[alphabet.alphabet[i]] =True 
                    else:
                        letters_coloured[i] = colour.YELLOW_TEXT + alphabet.alphabet[i].upper() + colour.BASE #otherwise (if not in the same position) colours the letter yellow
                        already_coloured_letters[alphabet.alphabet[i]] ="yellow"
                    
                elif alphabet.alphabet[i] in guess_list and alphabet.alphabet[i] not in answer_list: #if guessed letter is not in word
                    letters_coloured[i] = colour.DARKGREY + alphabet.alphabet[i].upper() + colour.BASE #colours letter darkgrey
                    already_coloured_letters[alphabet.alphabet[i]] =True
                else:
                    #if the current letter has not been guessed
                    letters_coloured[i] = alphabet.alphabet[i].upper()

            elif already_coloured_letters[alphabet.alphabet[i]] == "yellow": #if the letter has been coloured yellow (i.e. may need to be coloured green)
                try:
                    #if the letter is in the same place in the guess and in the answer
                    if answer_list.index(alphabet.alphabet[i]) == guess_list.index(alphabet.alphabet[i]) and already_coloured_letters == False:
                        letters_coloured[i] = colour.GREEN_TEXT + alphabet.alphabet[i].upper() + colour.BASE #colours letter green
                        already_coloured_letters[alphabet.alphabet[i]] =True
                    else:
                        pass
                except:
                    pass
            else: 
                pass

        #combines list into str
        letters_coloured_str =""
        for i in range(len(letters_coloured)):
            letters_coloured_str += colour.BOLD + letters_coloured[i] + colour.BASE
        
        return guess_coloured