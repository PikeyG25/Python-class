#Parker Gowans
#12/18
#Cards
import random
deck = []
player1_hand = []
player2_hand = []

def makedeck(deck):
    """ populate the deck of cards """
    SUITS = ["hearts","diamonds","clubs","spades"]
    VALUES = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    for e in SUITS:
        for i in VALUES:
            card = i+" "+e
            deck.append(card)

def shuffledeck(deck):
    for i in range(len(deck)):
        j=random.randrange(len(deck))
        temp = deck[i]
        deck[i] = deck[j]
        deck[j] = temp

def dealcard(deck,player1_hand,player2_hand):
    for i in range(5):
        card = deck.pop()
        player2_hand.append(card)
        card = deck.pop()
        player1_hand.append(card)

        
makedeck(deck)
print(len(deck))
print(deck)

print()
print()
print()
shuffledeck(deck)
print(deck)

dealcard(deck,player1_hand,player2_hand)

print(player1_hand)
print(player2_hand)
print(len(deck))

