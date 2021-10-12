from collections import deque
from enum import Enum
from dataclasses import dataclass
from typing import Deque, List
from random import shuffle


class Suite(Enum):
    HEART = 1
    DIAMOND = 2
    SPADE = 3
    CLUBS = 4


class Value(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


@dataclass(frozen=True)
class Card:
    suit: Suite
    value: Value

    def __str__(self):
        return f'{self.value.name} of {self.suit.name}S'


class Deck:
    def __init__(self):
        self.cards = self.__new_deck()

    def __len__(self):
        return len(self.cards)

    def print_deck(self):
        for card in self.cards:
            print(card)

    def shuffle(self) -> bool:
        if len(self) == 0:
            return False
        shuffle(self.cards)
        return True

    def draw(self) -> Card:
        if len(self):
            return self.cards.pop()

    def draw_from_bottom(self) -> Card:
        if len(self):
            return self.cards.popleft()
    
    def place_at_bottom(self, card: Card):
        self.cards.appendleft(card)

    def place_at_top(self, card:Card):
        self.cards.append(card)

    def contains_duplicates(self) -> bool:
        return len(self) > len(set(self.cards))

    def __new_deck(self) -> Deque[Card]:
        _cards = deque([])
        for suit in Suite:
            for value in Value:
                _cards.append(Card(suit, value))

        return _cards


class Player:
    def __init__(self, name, deck: Deck):
        self.name = name
        self.cards = []
        self.deck = deck

    def __str__(self):
        return f'{self.name}: num_of_card: {len(self.cards)}'

    @property
    def total_card_value(self):
        return sum(card.value.value for card in self.cards)

    def show_cards(self):
        print(f"{self.name}'s cards")
        print("**********************")
        for card in self.cards:
            print(card)

    def draw_card(self):
        self.cards.append(self.deck.draw())

    def place_card_at_bottom(self, index):
        self.deck.place_at_bottom(self.cards.pop(index))

    def shuffle_deck(self):
        self.deck.shuffle()


if __name__ == '__main__':
    deck = Deck()
    player1 = Player('Steve Ballmer', deck)
    player2 = Player('Homer Simpson', deck)
    
    player1.shuffle_deck()

    for _ in range(2):
        player1.draw_card()
        player2.draw_card()

    player1.show_cards()
    player2.show_cards()

    print('player1 value', player1.total_card_value)
    print('player2 value', player2.total_card_value)
