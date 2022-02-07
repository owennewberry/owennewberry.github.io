import random
from replit import db

player = ""

#slotsMsg = "Welcome to the Slot Machine! To win you must get one of the following combinations:\n"+"BAR\tBAR\tBAR\t\tpays\t$250\n"+"BELL\tBELL\tBELL/BAR\tpays\t$20\n"+"PLUM\tPLUM\tPLUM/BAR\tpays\t$14\n"+"ORANGE\tORANGE\tORANGE/BAR\tpays\t$10\n"+"CHERRY\tCHERRY\tCHERRY\t\tpays\t$7\n"+"CHERRY\tCHERRY\t  -\t\tpays\t$5\n"+"CHERRY\t  -\t  -\t\tpays\t$2\n"+"7\t  7\t  7\t\tpays\t The Jackpot!\n"

#Constants:
INIT_STAKE = 0
INIT_BALANCE = db["jackpot"]
ITEMS = ["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR", "7"]

firstWheel = None
secondWheel = None
thirdWheel = None
stake = INIT_STAKE
balance = INIT_BALANCE

def play(author):
    INIT_STAKE = db[author]
    if db[author] < 1:
      return
    global stake, firstWheel, secondWheel, thirdWheel
    firstWheel = spinWheel()
    secondWheel = spinWheel()
    thirdWheel = spinWheel()
    return printScore(author)

def spinWheel():
    '''
    returns a random item from the wheel
    '''
    randomNumber = random.randint(0, 6)
    return ITEMS[randomNumber]

def printScore(author):
    '''
    prints the current score
    '''
    global stake, firstWheel, secondWheel, thirdWheel, balance
    if((firstWheel == "CHERRY") and (secondWheel != "CHERRY")):
        win = 2
        balance = balance - 2
    elif((firstWheel == "CHERRY") and (secondWheel == "CHERRY") and (thirdWheel != "CHERRY")):
        win = 5
        balance = balance - 5
    elif((firstWheel == "CHERRY") and (secondWheel == "CHERRY") and (thirdWheel == "CHERRY")):
        win = 7
        balance = balance - 7
    elif((firstWheel == "ORANGE") and (secondWheel == "ORANGE") and ((thirdWheel == "ORANGE") or (thirdWheel == "BAR"))):
        win = 10
        balance = balance - 10
    elif((firstWheel == "PLUM") and (secondWheel == "PLUM") and ((thirdWheel == "PLUM") or (thirdWheel == "BAR"))):
        win = 14
        balance = balance - 14
    elif((firstWheel == "BELL") and (secondWheel == "BELL") and ((thirdWheel == "BELL") or (thirdWheel == "BAR"))):
        win = 20
        balance = balance - 20
    elif((firstWheel == "BAR") and (secondWheel == "BAR") and (thirdWheel == "BAR")):
        win = 250
        balance = balance - 250
    elif((firstWheel == "7") and (secondWheel == "7") and (thirdWheel == "7")):
        win = balance
        balance = balance - win
    else:
        win = -1
        balance = balance + 1

    stake += win
    if win == balance:
        result = win
    if(win > 0):
        result = win
    else:
        result = -1
    return result
    