import random
import customtkinter
from Player import Player
import Constants
import Messages
from UI_Elements import ToplevelWindow, Split_Frame, Button, Label

class Blackjack(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.cards_in_play = []
        self.ace_in_hand = []
        self.title("Blackjack")
        self.geometry(f"{Constants.app_width}x{Constants.app_height}")
        self.update()

        self.Dealer = Player(Hand = {}, Name = 'Dealer')
        self.User = Player(Hand = {}, Name = 'User')

        self.ui_frame = customtkinter.CTkFrame(
            master = self,
            width = Constants.app_width,
            height = Constants.ui_frame_height,
            fg_color = Constants.app_bg_color,
            corner_radius = 0)
        self.ui_frame.pack(anchor = 'n', side = 'top', fill = 'both')

        self.money_counter = Label(
            master = self.ui_frame,
            width = 200,
            text = f'Current money: ${str(self.User.Money)}, Bet: ',
            side = 'left',
            anchor = 'nw')
        
        initial_bet = 50
        self.bet = customtkinter.CTkEntry(
            master = self.ui_frame,
            width = 60,
            justify = 'center',
            placeholder_text = initial_bet)
        self.bet.insert(0, initial_bet)
        self.bet.pack(padx = 10, pady = 10, side = 'left', anchor = 'n')

        self.deal_button = Button(
            master = self.ui_frame,
            text = 'Deal',
            command = self.deal_hand)

        self.hit_button = Button(
            master = self.ui_frame,
            text = 'Hit',
            state = 'disabled',
            command = self.hit)
        
        self.stand_button = Button(
            master = self.ui_frame,
            text = 'Stand',
            state = 'disabled',
            command = self.stand)

        self.top_frame = Split_Frame(master = self, anchor = 'n')
        self.bottom_frame = Split_Frame(master = self, anchor = 's')
        
    def place_card(self, master: customtkinter.CTkFrame, card_image = None):
        card = customtkinter.CTkButton(
            master = master,
            width = Constants.card_width,
            height = Constants.card_height,
            border_spacing = 0,
            text = '',
            bg_color = 'transparent',
            fg_color = 'transparent',
            hover = 'false',
            corner_radius = 0,
            image = customtkinter.CTkImage(
                    light_image = card_image,
                    size = (Constants.card_width, Constants.card_height)))
                    
        relx = (master.winfo_x() / 2000) + (len(master.winfo_children()) / 10)
        card.place(in_ = master, relx = relx, rely = 0.1)

    def deal_hand(self):
        self.hit_button.configure(state = 'enabled')
        self.stand_button.configure(state = 'enabled')
        self.deal_button.configure(state = 'disabled')

        self.cards_in_play, matching_cards, card_images = self.User.Deal(cards_in_play = self.cards_in_play)
        for card_image in card_images:
            self.place_card(master = self.top_frame.user_subframe, card_image = card_image)
        
        self.Dealer.Deal(cards_in_play = self.cards_in_play)
        for idx, card_key in enumerate(list(self.Dealer.Hand.keys())):
            self.place_card(
                master = self.top_frame.dealer_subframe, 
                card_image = self.Dealer.Hand[card_key]['Front'] if idx == 0 else self.Dealer.Hand[card_key]['Back'])

        if self.User.Hand_value == Constants.blackjack:
            self.determine_winner(bet_multiplier = Constants.natural_blackjack_multiplier)
            self.Label = Label(
                master = self.bottom_frame.dealer_subframe,
                text = 'Natural blackjack! You get a 150% payout on your bet!')
        
        if matching_cards[0] == '6' and matching_cards[1] == '9':
            self.Label = Label(
                master = self.bottom_frame.dealer_subframe,
                text = 'Nice')

        matching_cards = ['Ace', 'Ace']
        if matching_cards[0] == matching_cards[1]:
            self.split_hand_popup = ToplevelWindow(self) 
            self.split_hand_popup.focus()
            self.wait_window(self.split_hand_popup)
            if self.split_hand_popup.decision == True:
                self.split()

    def split(self):
        for card in self.top_frame.user_subframe.winfo_children():
            card.destroy()
        
        self.hit_button.configure(text = 'Hit Top Hand')
        self.stand_button.configure(text = 'Stand Top Hand')

        self.place_card(
            master = self.top_frame.user_subframe, 
            card_image = [self.User.Hand[card_key]['Front'] for idx, card_key in enumerate(list(self.User.Hand.keys())) if idx == 0][0])
        
        self.place_card(
            master = self.bottom_frame.user_subframe, 
            card_image = [self.User.Hand[card_key]['Front'] for idx, card_key in enumerate(list(self.User.Hand.keys())) if idx == 1][0])

    def hit(self):
        self.cards_in_play, card_image = self.User.Hit(cards_in_play = self.cards_in_play)
        
        self.place_card(master = self.top_frame.user_subframe, card_image = card_image)

        self.ace_in_hand = [card_key for card_key in self.User.Hand.keys() if 'Ace' in card_key]
        
        if self.User.Hand_value < Constants.blackjack:
            return
        if self.ace_in_hand:
            if self.User.Hand_value - (10* len(self.ace_in_hand)) < Constants.blackjack:
                return
        
        self.determine_winner()
        self.hit_button.configure(state = 'disabled')

    def stand(self):
        for button in [self.deal_button, self.hit_button, self.stand_button]:
            button.configure(state = 'disabled')

        while self.Dealer.Hand_value <= 16:
            self.cards_in_play, card_image = self.Dealer.Hit(cards_in_play = self.cards_in_play)
        
        self.determine_winner()

    def determine_winner(self, bet_multiplier: float|int = 1):
        for button in [self.deal_button, self.hit_button, self.stand_button]:
            button.configure(state = 'disabled')

        def handle_bet(self):

            self.User.Money = self.User.Money + (int(self.bet.get()) * bet_multiplier) if win == True else self.User.Money - (int(self.bet.get()) * bet_multiplier)

            self.money_counter.configure(text = f'Current money: ${str(self.User.Money)}, Bet: ')

        def display_outcome(self):
            self.Label = Label(
                master = self.bottom_frame.dealer_subframe,
                text = random.choice(Messages.win_messages) if win == True else random.choice(Messages.loss_messages))

            self.Label = Label(
                master = self.bottom_frame.dealer_subframe,
                text = f'User hand: {self.User.Hand_value} vs Dealer hand: {self.Dealer.Hand_value}')

        def flip_cards(self):
            for card in self.top_frame.dealer_subframe.winfo_children():
                card.destroy()
                
            for idx, card_key in enumerate(list(self.Dealer.Hand.keys())):
                self.place_card(
                    master = self.top_frame.dealer_subframe, 
                    card_image = self.Dealer.Hand[card_key]['Front'])

        self.reset_button = Button(
            master = self.ui_frame,
            text = 'New Game',
            command = self.reset_game) 
        
        if self.ace_in_hand:
            self.User.Hand_value -= (10 * len(self.ace_in_hand))
        win = True if self.User.Hand_value >= self.Dealer.Hand_value and self.User.Hand_value <= Constants.blackjack or self.Dealer.Hand_value > Constants.blackjack else False
        
        flip_cards(self)
        handle_bet(self)
        display_outcome(self)

    def reset_game(self):
        self.top_frame.destroy()
        self.bottom_frame.destroy()
        self.top_frame = Split_Frame(master = self, anchor = 'n')
        self.bottom_frame = Split_Frame(master = self, anchor = 's')

        self.User.Hand, self.User.Hand_value = {}, 0
        self.Dealer.Hand, self.Dealer.Hand_value = {}, 0 

        self.deal_button.configure(state = 'enabled')
        self.reset_button.destroy()
        self.cards_in_play, self.ace_in_hand  = [], []
        
if __name__ == "__main__":
    app = Blackjack()
    app.mainloop()

