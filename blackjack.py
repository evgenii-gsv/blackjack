import random
import os
import sys
import time


class Card:
    def __init__(self, suit, value, card_value):
        self.suit = suit
        self.value = value
        self.card_value = card_value


def print_cards(cards, hidden=False):
    if hidden:
        print(cards[0].value + cards[0].suit, end=' ')
        print('XX', end=' ')
    else:
        for card in cards:
            print(card.value + card.suit, end=' ')
    print()


def new_deck_shuffle():
    deck = []
    for suit in suits * decks_quantity:
        for card in cards * decks_quantity:
            deck.append(Card(suits_values[suit], card, cards_value[card]))
    random.shuffle(deck)
    return deck


def get_cards_value(cards):
    value = 0
    for card in cards:
        value += card.card_value
    return value


def clear():
    os.system('cls')


def player_round(hand, deck, chips, bet):
    score = get_cards_value(hand)
    while score < 21:
        print('Type h to Hit, s to Stand, d to Double Down:')
        choice = input().lower().strip()
        if choice == 'h' or choice == 'hit':
            hand.append(deck[0])
            deck.pop(0)
            # if we go beyond 21, check if we have Aces with value 11 and make it 1
            if get_cards_value(hand) > 21:
                for card in hand:
                    if card.card_value == 11:
                        card.card_value = 1
                        break
            score = get_cards_value(hand)
            print()
            print('Your cards:')
            print_cards(hand)
            print('Your score:', score)
        elif choice == 's' or choice == 'stand':
            break
        elif choice == 'd' or 'double' in choice:
            if chips - bet >= 0:
                chips -= bet
                bet = bet * 2
                print('Your new bet is:', bet)
                hand.append(deck[0])
                deck.pop(0)
                # if we go beyond 21, check if we have Aces with value 11 and make it 1
                if get_cards_value(hand) > 21:
                    for card in hand:
                        if card.card_value == 11:
                            card.card_value = 1
                            break
                score = get_cards_value(hand)
                print()
                print('Your cards:')
                print_cards(hand)
                print('Your score:', score)
                break
            else:
                print('You don\'t have enough chips to Double Down.')
        else:
            print('Your choice is not clear.')
    return deck, chips, score, bet


def blackjack_game(deck, chips):
    player_cards = []
    dealer_cards = []

    # getting player's bet or exiting the program
    validating_bet = True
    while validating_bet:
        print()
        print(f'Place your bet. You have {chips} chips. Type \'stop\' to stop playing.')
        bet = input('>>>> ').lower().strip()
        if bet == 'stop':
            if chips < initial_chips_value:
                print(f'You stopped playing with {chips} chips. You lost {initial_chips_value - chips} chips.')
            elif chips > initial_chips_value:
                print(f'You stopped playing with {chips} chips. You won {chips - initial_chips_value} chips.')
            else:
                print(f'You stopped playing with {chips} chips. You didn\'t win any chips.')
            sys.exit()
        try:
            bet = int(bet)
            if chips - bet < 0:
                print('You don\'t have enough chips for this bet.')
            else:
                chips -= bet
                print(f'Your bet is {bet} chips.')
                validating_bet = False
        except ValueError:
            print('Invalid bet.')

    # dealing hands to player and dealer
    while len(dealer_cards) < 2:
        player_cards.append(deck[0])
        deck.pop(0)
        dealer_cards.append(deck[0])
        deck.pop(0)
    player_score = get_cards_value(player_cards)
    dealer_score = get_cards_value(dealer_cards)

    # checking if player or dealer has two Aces and modifying the value of one of the cards
    if player_score > 21:
        player_cards[0].card_value = 1
        player_score = get_cards_value(player_cards)
    if dealer_score > 21:
        dealer_cards[0].card_value = 1
        dealer_score = get_cards_value(dealer_cards)

    print('Dealer cards:')
    print_cards(dealer_cards, True)
    print()
    print('Your cards:')
    print_cards(player_cards)
    print('Your score:', player_score)

    # checking if dealer got a visible Ace and asking for Insurance Bet
    if dealer_cards[0].card_value == 11 or dealer_cards[0].card_value == 1:
        insurance_bet = 0
        if chips - int(bet/2) >= 0:
            print(f'Dealer has a chance of Blackjack. Would you like to place an Insurance Bet of {int(bet/2)} chips? (y/n)')
            choice = input('>>>> ').lower().strip()
            if choice == 'y' or choice == 'yes':
                insurance_bet = int(bet/2)
                chips -= insurance_bet
        else:
            print('Dealer has a chance of Blackjack. You don\'t have enough chips to place an Insurance Bet.')
        print('Dealer checks for Blackjack...')
        time.sleep(2)

        # checking if dealer got a Blackjack
        if dealer_score == 21:
            print('Dealer cards:')
            print_cards(dealer_cards)
            print('Dealer\'s got a Blackjack, Dealer wins.')
            if insurance_bet != 0:
                chips += insurance_bet * 2
                print(f'You won {insurance_bet} chips because of the Insurance Bet.')
            return deck, chips
        else:
            print('Dealer didn\'t get Blackjack.')
            if insurance_bet != 0:
                print(f'You lost {insurance_bet} chips because of the Insurance Bet.')

    # checking if player got a Blackjack, which pays 3 to 2
    if player_score == 21:
        chips += bet + int(bet*1.5)
        print(f'You got a Blackjack, you won {int(bet*1.5)} chips.')
        return deck, chips

    # checking if we can split hand
    if player_cards[0].value == player_cards[1].value and chips - bet >= 0:
        print(f'Would you like to Split your hand? You will need to place an additional bet of {bet} chips. (y/n)')
        choice = input('>>>> ').lower().strip()
        if choice == 'y' or choice == 'yes':

            # making two hands and accepting the bet
            chips -= bet
            first_hand_bet = bet
            second_hand_bet = bet
            first_hand = [player_cards[0]]
            second_hand = [player_cards[1]]
            first_hand.append(deck[0])
            deck.pop(0)
            second_hand.append(deck[0])
            deck.pop(0)
            first_hand_score = get_cards_value(first_hand)
            second_hand_score = get_cards_value(second_hand)
            print('Your total bet is:', bet * 2)
            print()
            print('Playing your first hand:')
            print_cards(first_hand)
            print('Your score:', first_hand_score)

            # playing first hand round
            deck, chips, first_hand_score, first_hand_bet = player_round(first_hand, deck, chips, first_hand_bet)
            if first_hand_score > 21:
                print(f'You busted and lost {first_hand_bet} chips.')
                first_hand_bet = 0

            print()
            print('Playing your second hand:')
            print_cards(second_hand)
            print('Your score:', second_hand_score)

            # playing second hand round
            deck, chips, second_hand_score, second_hand_bet = player_round(second_hand, deck, chips, second_hand_bet)
            if second_hand_score > 21:
                print(f'You busted and lost {second_hand_bet} chips.')
                second_hand_bet = 0
            if first_hand_score > 21 and second_hand_score > 21:
                return deck, chips

            # dealer's round on split hands
            print()
            print('Dealer cards:')
            print_cards(dealer_cards)
            print('Dealer score:', dealer_score)
            time.sleep(1)
            while dealer_score < 17:
                dealer_cards.append(deck[0])
                deck.pop(0)
                # if we go beyond 21, check if we have Aces with value 11
                if get_cards_value(dealer_cards) > 21:
                    for card in dealer_cards:
                        if card.card_value == 11:
                            card.card_value = 1
                            break
                dealer_score = get_cards_value(dealer_cards)
                print()
                print('Dealer hits')
                print_cards(dealer_cards)
                print('Dealer score:', dealer_score)
                time.sleep(1)

            # checking if dealer busted
            if dealer_score > 21:
                print(f'Dealer busted and you won {first_hand_bet + second_hand_bet} chips.')
                chips += (first_hand_bet + second_hand_bet)*2
                return deck, chips

            # end split round
            if dealer_score >= first_hand_score:
                print(f'Dealer won with the score of {dealer_score} against your first hand score of {first_hand_score}.')
                print(f'You lost {first_hand_bet} chips.')
            else:
                chips += first_hand_bet * 2
                print(f'You won with the first hand score of {first_hand_score} against Dealer\'s score of {dealer_score}.')
                print(f'You won {first_hand_bet} chips.')
            if dealer_score >= second_hand_score:
                print(f'Dealer won with the score of {dealer_score} against your second hand score of {second_hand_score}.')
                print(f'You lost {second_hand_bet} chips.')
            else:
                chips += second_hand_bet * 2
                print(f'You won with the second hand score of {second_hand_score} against Dealer\'s score of {dealer_score}.')
                print(f'You won {second_hand_bet} chips.')
            return deck, chips

    # player's round
    deck, chips, player_score, bet = player_round(player_cards, deck, chips, bet)

    # checking if player busted
    if player_score > 21:
        print(f'You busted and lost {bet} chips.')
        return deck, chips

    # dealer's round
    print()
    print('Dealer cards:')
    print_cards(dealer_cards)
    print('Dealer score:', dealer_score)
    time.sleep(1)
    while dealer_score < 17:
        dealer_cards.append(deck[0])
        deck.pop(0)
        # if we go beyond 21, check if we have Aces with value 11
        if get_cards_value(dealer_cards) > 21:
            for card in dealer_cards:
                if card.card_value == 11:
                    card.card_value = 1
                    break
        dealer_score = get_cards_value(dealer_cards)
        print()
        print('Dealer hits')
        print_cards(dealer_cards)
        print('Dealer score:', dealer_score)
        time.sleep(1)

    # checking if dealer busted
    if dealer_score > 21:
        print(f'Dealer busted and you won {bet} chips.')
        chips += bet * 2
        return deck, chips

    # end round
    if dealer_score >= player_score:
        print(f'Dealer won with the score of {dealer_score} against your score of {player_score}.')
        print(f'You lost {bet} chips.')
        return deck, chips
    else:
        chips += bet * 2
        print(f'You won with the score of {player_score} against Dealer\'s score of {dealer_score}.')
        print(f'You won {bet} chips.')
        return deck, chips


if __name__ == '__main__':
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    suits_values = {"Spades": "♠", "Hearts": "♥", "Clubs": "♣", "Diamonds": "♦"}
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    cards_value = {
        'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10
    }
    decks_quantity = 6
    initial_chips_value = 1000
    player_chips = initial_chips_value
    deck = new_deck_shuffle()
    print('Welcome to Blackjack table. Dealer stands on 17. Blackjack pays 3 to 2.')
    while True:
        deck, player_chips = blackjack_game(deck, player_chips)
        # if we got through 2/3 of the deck, we get a new deck
        if len(deck) <= decks_quantity * 52 / 3:
            deck = new_deck_shuffle()
            print('Deck of cards is reshuffled.')
        # checking if we ran out of chips
        if player_chips <= 0:
            print('You have lost all your money. Go home and think about what you\'ve done.')
            break
