import random

def shuffle(array):
    currentIndex = len(array)
    while currentIndex != 0:
        randomIndex = random.randint(0, currentIndex - 1)
        currentIndex -= 1
        array[currentIndex], array[randomIndex] = array[randomIndex], array[currentIndex]
    return array

def getRandomValueBetween(min=1, max=6):
    return random.randint(min, max)