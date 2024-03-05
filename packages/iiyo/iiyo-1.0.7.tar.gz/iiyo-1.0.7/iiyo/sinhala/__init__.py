import random
from .Data import *


# prastha_pirulu
def prasthapirulu():
    return random.choice(Prastha_Pirulu_List)


# prastha_pirulu
def pp():
    return random.choice(Prastha_Pirulu_List)


# theravili
def theravili():
    current_quiz = random.choice(theravili_List)
    # Display the quiz question without the answer
    
    print(f"Quiz: {current_quiz.split('-')[0]}")

    # Wait for user input
    input("Press Enter to answer..")

    # Display the answer
    print(f"Answer: {current_quiz.split('-')[1].strip()}")


# thun_theravili
def thun_theravili():
    current_quiz = random.choice(thun_theravili_List)
    # Display the quiz question without the answer
    
    print(f"Quiz: {current_quiz.split('-')[0]}")

    # Wait for user input
    input("Press Enter to answer..")

    # Display the answer
    print(f"Answer: {current_quiz.split('-')[1].strip()}")


# thun_theravili shorts
def thun():
    current_quiz = random.choice(thun_theravili_List)
    # Display the quiz question without the answer
    
    print(f"Quiz: {current_quiz.split('-')[0]}")

    # Wait for user input
    input("Press Enter to answer..")

    # Display the answer
    print(f"Answer: {current_quiz.split('-')[1].strip()}")

