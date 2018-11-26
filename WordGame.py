# -*- coding: utf-8 -*-
"""
# Working Directory: E:\Temp
# Created on Sun Oct 14 16:22:30 2018

# @author: Anant.Kumar
#Purpose : To create a quiz to test vocabulary of the user. The game takes a word (application proposes a word, user may input his/her own choice of word if he wishes, and prepares 
# around 20 words, some of them are english words and rest are just jumbled characters put together. User has to select the engligh word from the given set of words. Each answer carries
# +1 score for it being right and -1 for wrong. There are 3 rounds of game and to qualify for next round user must get 60% of the score in previous rounds.The complexity of the quiz
# as round progresses. At the end of each round, program shows those correct answers which user could not identify.

Known Issues:
1. The round 3 starts with a word of 8 - 9 characters length and preparing a quiz may take substantial time, depending on the processsor speed.
2. Sometimes quiz may have repeating words.
3. User must put the data.json file in the same directory as this python script file. data.json is a Dictionary data type file and serves as dictionary to the program.


"""

import os
import json
from difflib import get_close_matches
import random
import itertools
from os import system, name

dirname, filename = os.path.split(os.path.abspath(__file__))
#print("running from", dirname)
#print ("file is", filename)
#os.chdir("E:\\OneDrive\\AmateurWork\\Python\\WordGame")
os.chdir(dirname)

## Produces permuitation of characters
def generate(vals="abc"):
    """ The program will generate words using permutations of character in the the supplied word"""
    ## Code to generate permutations
    return ("".join(x) for x in itertools.chain.from_iterable(itertools.permutations(vals,i+1) for i in range(1, len(vals))))


#Clear the screen
def clear(): 
    """The program will clear the console screen"""
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

#Produces translation of the word
def translate(w):
    """The program will translate the word, based on the entry found in dict dictionary. Incase there is no entry for the word, it will return None"""
    w = w.lower()    
    if ((w in dict.keys()) and ("ISO" not in dict[w])):
        return dict[w]
    elif ((w.capitalize() in dict.keys()) and ("ISO" not in dict[w.capitalize()])):
        return dict[w.capitalize()]
    elif ((w.upper() in dict.keys()) and ("ISO" not in dict[w.upper()])):
        return dict[w.upper()]    
    else:
        return None

def purgeSpace(word):
    """The function will remove any blank space and any dashes from the word suplied and return the resultant word"""
    purgedWord = ""
    for character in word:
        if character!=" " and character != "-":
            purgedWord+=character
    return purgedWord

def print_unattempted(userInputList, wordDictGame, correctWordList):
    """The function prints unattempted correct words"""
    print("\n\n\tYou missed following correct words to identify:")
    for i in range(1, len(wordDictGame)+1):
        if ((i not in userInputList) and (wordDictGame[i] in correctWordList)):
            print("\t", wordDictGame[i], " : ", translate(w = wordDictGame[i]), "\n")

def maxWordLength(i):
    """The function calculates maximum word length in the quiz"""
    return min(i*2+3, 10)
def minWordLength(i):
    """The function calculates minimum word length in the quiz"""
    return i*2+2

def handleLevel(userScore, maxScore):
    """The function handles once user finishes a level by prompting relevant message"""
    if(userScore >= 0.6*maxScore):
        print("\n\n\tYou did a great job. Your Score: ", userScore, " / ", maxScore)
    else:
        print("\n\n\tGame Over. Your Score: ", userScore, " / ", maxScore, "\n\tSee you again.")
        fail()
        
def fail():
    """ The funtion will prepare the program to exit"""
    input("\tProgram will exit now. Press enter to proceed..")
    clear()
    exit()


########### MAIN PROGRAM ##############

#Loads dictoinary in the program
dict = json.load(open("data.json"))


# Initialize the wordlist for acceptable word to initialize the game
wordlist = []
countCorrectWord = 10
correctWordList = []
countIncorrectWord = 10
incorrectWordList = []
minDesiredCorrectWord = 5
maxRound = 3
clear()

print("\n\nThe program will test your Engligh vocabulary.")

# Pick a random word based from dictionary on word length criteria of the game
for round in range(1, maxRound+1, 1):
    for key, val in dict.items():  
        if(len(key) >= minWordLength(i = round) and len(key) <= maxWordLength(i = round)):
            wordlist.append(key)    
    myword = random.choice(wordlist)    
    print(f"\n\nTo proceed ROUND {round}, random word selected: ", myword.upper())

#Ask user for his / her choice of word if any. If no, proceed with the random word selected.
    temp = "\n\nPress ENTER to proceed or type your word ("+ str(minWordLength(i = round))+" - "+str(maxWordLength(i = round))+ ") characters ONLY): "
    temp = input(temp)
    if(temp != ""):
        if(len(temp) < minWordLength(i = round) or len(temp) > maxWordLength(i = round)):
            print("The word is too long / short. Proceeding with ", myword.upper(), " instead.")
        else:
            myword = temp
    else:
        print("\n\nGame proceeding with ", myword.upper())

#Print meaning of the word selected
    print("INFO:Meaning of ", myword.upper(), "\n ", translate(w = myword))
    myword = purgeSpace(word = myword)
    #print("Meaning: ", dict[myword])
    input("> Press ENTER to proceed: ")
    print("\n\n\tPreparing game. Please wait!!")
    #print(list(generate(myword.upper()))) # force iteration to print result
#Create a list of correct word and incorrect word    
    correctWordCount = 0
    for word in list(generate(vals = myword.upper())):
        if(translate(w = word) != None):
            if(word not in correctWordList):
                correctWordList.append(word)                        
        else:
            if(word not in incorrectWordList):
                incorrectWordList.append(word)

    #Deletes original word from the correct word list
    if(myword in correctWordList):
        wordlist.remove(myword)

    #Exit the program if not enough correct words
    if(len(correctWordList) < minDesiredCorrectWord):
        print("Could not prepare a interesting quiz from the word: ", myword.upper())
        fail()

    #print("\n\nIncorrect Word List: ", incorrectWordList)

    #Create list for assorted wordlist
    wordDictGame = {}
    wordListGame = []

#Sort the wordlist based on length, longest wordlist to shortes and copy the top few words to wordList for the game
    wordListGame = sorted(correctWordList, key = len, reverse = True)[:min(len(correctWordList), countCorrectWord)].copy()
    #print(correctWordList)
    #print(wordListGame)
    correctWordCount = len(wordListGame)

# Include few incorect word in the word game list as well
    for cntr in range(0, min(len(incorrectWordList), countIncorrectWord) ):
        wordListGame.append(random.choice(incorrectWordList))
# Create a dictionary by randomly selected word from the list created above, with index being the serial number. 
    for cntr in range(1, len(wordListGame)+ 1):
        wordDictGame[cntr] = random.choice(wordListGame)
        wordListGame.remove(wordDictGame[cntr])

    userScore = 0
    userInputList = []
# Print the quiz words and ask for user input, repeated number of chances which is equal to number ofnwords inthe WordList
    for cntr in range(1, len(wordDictGame)):

        clear()
        print(f"\n\nRound: {round}\n\nTest your vocubulary. Enter number corresponding to the words listed below, which you think is an English word.\nYou have ", len(wordDictGame), " chances \nThere are ", correctWordCount, " correct words. \n\n \t(A blank entry will submit the round for evaluation.)")
        for ctr in range(1, len(wordDictGame) + 1):
            if((ctr -1) % 5 == 0):
                print("\n\n")
            print("\t\t", ctr, "-", wordDictGame[ctr], end = " ")
        print("\n\nWords already attempted: ", userInputList, "\nScore: ", userScore )

        user = input("\n> ")
        #Check if the user input is a number or not
        if(user == ""):            
            #print_unattempted(userInputList, wordDictGame, correctWordList)
            #handleLevel(userScore, min(len(correctWordList), countCorrectWord))
            break
        else:
            try:
                inputNumber = int(user)
                if inputNumber <= 0:
                    raise NotPositiveError
                pass
            except ValueError:
                print("This was not a number, please try again.")
            except NotPositiveError:
                print("The number was not positive, please try again.")
            #Check if the user input value is already input before. If not input before, check if the entwered number corresponds to a correct english word
            if(inputNumber in userInputList):
                print("The word ", wordDictGame[inputNumber], " already played. Try other word.")
                pass
            else:
                #Append the user input  number in the list for future checking
                userInputList.append(inputNumber)
                userInputList.sort()
                #Check if the number corresponds to a correct english word
                if(wordDictGame[inputNumber] in correctWordList):
                    print("\tCorrect (+1) \n\t", wordDictGame[inputNumber], " means ", translate(w = wordDictGame[inputNumber]), "\n\n \t", len(wordDictGame) - cntr, " attempts left.\n")
                    userScore += 1
                elif(wordDictGame[inputNumber] not in correctWordList):
                    print("\tWrong (-1) No word ", wordDictGame[inputNumber], " in database", "\n\n \t", len(wordDictGame) - cntr, " attempts left.\n")
                    userScore -= 1
            input("Press ENTER to continue...")
    
    print_unattempted(userInputList = userInputList, wordDictGame = wordDictGame, correctWordList = correctWordList)
    handleLevel(userScore = userScore, maxScore = min(len(correctWordList), countCorrectWord))
    if(round <= maxRound-1):
        input("\n\tYou are moving to next round. Enter to proceed..")
    clear()
    