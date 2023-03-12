import os
from PIL import Image
import Constants
Card_Image_Directory = 'Card_Images'

Card_Images = []
for root, subdir, files in os.walk(Card_Image_Directory):
    for file in files:
        File = os.path.join(root, file)
        Card_Images.append(File)

class Deck:
    Cards = {}
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
        
        Cards[f'{Face} of {Suit}'] = {
            'Suit': Suit,
            'Face': Face,
            'Value': Value,
            'Front': Image.open(pngFile),
            'Back': Image.open(card_back)}
