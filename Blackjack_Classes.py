import os
from PIL import Image
import random
import Constants
from dataclasses import dataclass
import customtkinter
Card_Image_Directory = 'Card_Images'
Card_Images = []
for root, subdir, files in os.walk(Card_Image_Directory):
    for file in files:
        File = os.path.join(root, file)
        Card_Images.append(File)

@dataclass
class Card:
    suit: str
    face: str
    value: int
    front_image: customtkinter.CTkImage
    back_image: customtkinter.CTkImage

class Deck:
    Cards: list[Card] = []

    for pngFile in Card_Images:
        if pngFile.__contains__('card_back'):
            card_back = pngFile
            
    for pngFile in Card_Images:
        if pngFile.__contains__('card_back'):
            continue
        Card_Info = os.path.basename(pngFile).split('_')
        Suit_Value = Card_Info[2].split('.')
        Suit = Suit_Value[0].capitalize()
        Face = Card_Info[0].capitalize()
        if Face in ['2', '3', '4', '5', '6', '7', '8', '9','10']:
            Value = int(Card_Info[0])
        elif Face == 'Ace':
            Value = Constants.ace_value
        elif Face in ['Jack', 'Queen', 'King']:
            Value = Constants.facecard_value
        

        new_card = Card(suit = Suit, face = Face, value = Value, front_image = Image.open(pngFile), back_image = Image.open(card_back))

        Cards.append(new_card)

@dataclass
class Hand:
    cards: list[Card] = None
    score: int = 0
    
    def add_card(self, card: Card):
        if self.cards is None:
            self.cards = []
        self.score += card.value
        self.cards.append(card)

    def draw_card(self, number_of_cards):
        for i in range(number_of_cards):
            card_drawn: Card = random.choice(Deck.Cards)
            Deck.Cards.remove(card_drawn)
            self.add_card(card_drawn)
        return card_drawn.front_image

    def deal(self):
        self.cards = []
        self.draw_card(number_of_cards = 2)
    
    def hit(self):
        if self.cards is not None:
            self.draw_card(number_of_cards = 1)

class Player:
    def __init__(self):
        self.main_hand = Hand()
        self.Money: int = 1000

    def split_hand(self):
        """Allows hand to be split. Not implemented yet (March 20, 2023)"""
        self.split1, self.split2 = Hand(), Hand()
        self.split1.add_card(self.main_hand.cards[0])
        self.split2.add_card(self.main_hand.cards[1])