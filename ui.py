
import customtkinter
import Constants
from Blackjack_Classes import Card, Deck, Hand, Player

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master = None, anchor: str = None, expand: bool = True, fill: str = 'both', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.width = Constants.app_width
        self.height = Constants.subframe_height
        self.subframe_width = Constants.subframe_width
        self.fg_color = Constants.app_bg_color
        self.corner_radius = 0
        self.pack(anchor = anchor, expand = expand, fill = fill)

        self.left = customtkinter.CTkFrame(
            master = self,
            width = self.subframe_width,
            height = Constants.subframe_height,
            fg_color = Constants.app_bg_color,
            corner_radius = self.corner_radius,
            border_color = Constants.button_color,
            border_width = 0)
        self.left.pack(in_ = self, side = 'left', expand = expand, fill = fill)
        
        self.right = customtkinter.CTkFrame(
            master = self,
            width = self.subframe_width,
            height = Constants.subframe_height,
            fg_color = Constants.app_bg_color,
            corner_radius = self.corner_radius,
            border_color = Constants.button_color,
            border_width = 0)
        self.right.pack(in_ = self, side = 'right', expand = expand, fill = fill)
    
    def place_cards(self, master: customtkinter.CTkFrame, player_hand: Hand = None, show_card_back: bool = False):
        for card in master.winfo_children():
            card.destroy()
        for idx, card in enumerate(player_hand.cards):
            if show_card_back == True and idx == 1:
                image = card.back_image
            else:
                image = card.front_image
            card_image = customtkinter.CTkButton(
                master = master,
                width = Constants.card_width,
                height = Constants.card_height,
                border_spacing = 0,
                text = '',
                bg_color = 'transparent',
                fg_color = 'transparent',
                hover = 'false',
                corner_radius = 0,
                image = customtkinter.CTkImage(light_image = image, size = (Constants.card_width, Constants.card_height)))
                        
            relx = (master.winfo_x() / 2000) + (len(master.winfo_children()) / 10)
            card_image.place(in_ = master, relx = relx, rely = 0.1)

class Button(customtkinter.CTkButton):
    def __init__(
        self, 
        master = None, 
        state: str = 'enabled', 
        width: int = Constants.button_width, 
        fg_color = Constants.button_color, 
        padx: int = 10, 
        pady: int = 10, 
        text: str = '', 
        anchor: str = 'n', 
        side = 'left', 
        command = None, 
        *args, **kwargs):
        super().__init__(
            master = master, 
            state = state, 
            width = width, 
            fg_color = fg_color, 
            text = text, 
            command = command, 
            *args, **kwargs)
        self.text = text
        self.pack(in_ = master, padx = padx, pady = pady, anchor = anchor, side = side)

class Label(customtkinter.CTkLabel):
    def __init__(
        self, 
        master = None, 
        width: int = Constants.subframe_width, 
        padx: int = 10, 
        pady: int = 10, 
        text: str = '', 
        justify = 'center', 
        anchor: str = None, 
        side: str = None, 
        fill = 'both', 
        *args, **kwargs):
        super().__init__(
            master = master, 
            width = width, 
            text = text, 
            justify = justify, 
            *args, **kwargs)
        self.text = text
        self.pack(in_ = master, padx = padx, pady = pady, anchor = anchor, fill = fill, side = side)

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f'{250}x{150}')
        self.title('Blackjack')
        self.label = Label(
            master = self, text = 'Split?')

        self.decision: customtkinter.BooleanVar = None
        self.yes_button = Button(
            master = self,
            text = 'Yes',
            command = self.yes_button_press,
            side = 'left')
        self.no_button = Button(
            master = self,
            text = 'No',
            command = self.no_button_press,
            side = 'right')

    def yes_button_press(self):
        self.decision = True
        self.destroy()
    
    def no_button_press(self):
        self.decision = False
        self.destroy()
