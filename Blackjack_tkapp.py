import random
import customtkinter
import Constants
import Messages
from Blackjack_Classes import Card, Deck, Hand, Player
from ui import MainFrame, Label, Button, ToplevelWindow

class Blackjack(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry(f"{Constants.app_width}x{Constants.app_height}")
        self.update()

        self.User = Player()
        self.Dealer = Player()
        
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

        self.top_frame = MainFrame(master = self, anchor = 'n')
        self.bottom_frame = MainFrame(master = self, anchor = 's')

    def button_configs(self, enable_buttons: list[Button], disable_buttons: list[Button]):
        [button.configure(state = 'enabled') for button in enable_buttons]
        [button.configure(state = 'disabled') for button in disable_buttons]

    def deal_hand(self):
        """Draw 2 cards for player and dealer"""
        self.button_configs(enable_buttons = [self.hit_button, self.stand_button], disable_buttons = [self.deal_button])

        self.User.main_hand.deal()
        self.Dealer.main_hand.deal()
        self.top_frame.place_cards(master = self.top_frame.left, player_hand = self.User.main_hand)
        self.top_frame.place_cards(master = self.top_frame.right, player_hand = self.Dealer.main_hand, show_card_back = True)

        if self.User.main_hand.score == Constants.blackjack:
            self.determine_winner(bet_multiplier = Constants.natural_blackjack_multiplier)
            self.Label = Label(
                master = self.bottom_frame.right,
                text = 'Natural blackjack! You get a 150% payout on your bet!')
            return
        
    def hit(self):
        """Draw card and display on screen"""
        self.User.main_hand.hit()
        self.top_frame.place_cards(master = self.top_frame.left, player_hand = self.User.main_hand)

        if self.User.main_hand.score < Constants.blackjack:
            return
        if self.User.main_hand.score - (10 * len([card.face for card in self.User.main_hand.cards if card.face == 'Ace'])) < Constants.blackjack:
            return
        
        self.determine_winner()

    def stand(self):
        """Dealer draws cards until hand is worth >= 17"""
        while self.Dealer.main_hand.score <= 16:
            self.Dealer.main_hand.hit()
        
        self.determine_winner()

    def determine_winner(self, bet_multiplier: float|int = 1):
        self.button_configs(enable_buttons = [], disable_buttons = [self.deal_button, self.hit_button, self.stand_button])

        def handle_bet():
            """Add/subtract bet from user's money based on if they won or loss"""
            self.User.Money = self.User.Money + (int(self.bet.get()) * bet_multiplier) if player_win == True else self.User.Money - (int(self.bet.get()) * bet_multiplier)
            self.money_counter.configure(text = f'Current money: ${str(self.User.Money)}, Bet: ')
        def display_outcome():
            """Print message to screen based on if user won or loss"""
            self.Label = Label(
                master = self.bottom_frame.right,
                text = random.choice(Messages.win_messages) if player_win == True else random.choice(Messages.loss_messages))
            self.Label = Label(
                master = self.bottom_frame.right,
                text = f'User hand: {self.User.main_hand.score} vs Dealer hand: {self.Dealer.main_hand.score}')
        def flip_cards():
            """Flip dealers cards so all cards are face up"""
            for card in self.top_frame.right.winfo_children():
                card.destroy()
                
            self.top_frame.place_cards(master = self.top_frame.right, player_hand = self.Dealer.main_hand)

        self.User.main_hand.score = self.User.main_hand.score - (10 * len([card.face for card in self.User.main_hand.cards if card.face == 'Ace'])) if self.User.main_hand.score > Constants.blackjack else self.User.main_hand.score
        player_win = True if self.User.main_hand.score == Constants.blackjack or self.User.main_hand.score > self.Dealer.main_hand.score and self.User.main_hand.score < Constants.blackjack or self.Dealer.main_hand.score > Constants.blackjack else False
        
        display_outcome()
        handle_bet()
        flip_cards()

        self.reset_button = Button(
            master = self.ui_frame,
            text = 'New Game',
            command = self.reset_game) 
        
    def reset_game(self):
        """Reset UI, players"""
        self.top_frame.destroy()
        self.bottom_frame.destroy()
        self.top_frame = MainFrame(master = self, anchor = 'n')
        self.bottom_frame = MainFrame(master = self, anchor = 's')

        def shuffle():
            """Add cards back into deck"""
            for player in [self.User, self.Dealer]:
                player.main_hand.score = 0
                for card in player.main_hand.cards:
                    Deck.Cards.append(card)
                    player.main_hand.cards.remove(card)
                    
        shuffle()

        self.button_configs(enable_buttons = [self.deal_button], disable_buttons = [])

        self.deal_button.configure(state = 'enabled')
        self.hit_button.configure(text = 'Hit')
        self.stand_button.configure(text = 'Stand')
        self.reset_button.destroy()
        
if __name__ == "__main__":
    app = Blackjack()
    app.mainloop()
