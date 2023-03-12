import random
from dataclasses import dataclass
import Deck
from Deck import Deck

CardKeys = list(Deck.Cards.keys())
@dataclass
class Player:
    Hand: dict = None
    Hand_value: int = 0
    Name: str = None
    Money: int = 1000

    def Deal(self, cards_in_play: list):

        for card in range(2):
            card_key = random.choice(CardKeys)
            while card_key in cards_in_play:
                card_key = random.choice(CardKeys)

            while card_key not in self.Hand.keys():
                self.Hand[card_key] = Deck.Cards[card_key]
            self.Hand_value += self.Hand[card_key]['Value']
            cards_in_play.append(card_key)

        matching_cards, card_images = [], []
        for idx, card_key in enumerate(list(self.Hand.keys())):  
            matching_cards.append(card_key.split(' ')[0])
            card_images.append(self.Hand[card_key]['Front'])
        
        return cards_in_play, matching_cards, card_images

    def Hit(self, cards_in_play: list):
        if self.Hand is not None:

            card_key = random.choice(CardKeys)
            while card_key in cards_in_play:
                card_key = random.choice(CardKeys)
            NewCard = Deck.Cards[card_key]
            self.Hand[card_key] = NewCard
            self.Hand_value += self.Hand[card_key]['Value']

            cards_in_play.append(card_key)
            
            for card_key in self.Hand.keys():
                card_image = self.Hand[card_key]['Front']
        
        return cards_in_play, card_image

