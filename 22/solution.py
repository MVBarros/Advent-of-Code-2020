import copy

class Player:
    def __init__(self, name: str, deck: list):
        self.name = name
        self.deck = deck

    def __repr__(self):
        return f'{self.name}: {self.deck}'
    
    def play(self):
        return self.deck.pop(0)
    
    def deck_size(self):
        return len(self.deck)

    def has_lost(self):
        return len(self.deck) == 0

    def win(self, cards: list):
        self.deck += cards
        
    def __hash__(self):
        return hash(self.name)
    
    def sum(self) -> int:
        total = 0
        card_size = len(self.deck)
        for i, card in enumerate(self.deck):
            total += (card_size - i) * card
        return total

class Combat:
    def __init__(self, players: set):
        self.players = players
    
    def is_finished(self) -> bool:
        return len(self.players) == 1

    def play(self) -> Player:
        while not self.is_finished():
            self.round()
            self.players = [player for player in self.players if not player.has_lost()]
        return self.players[0]

    def round(self):
        plays = {player : player.play() for player in self.players}
        winner = max(plays, key=plays.get)
        played_cards = list(plays.values())
        played_cards.sort(reverse=True)
        winner.win(played_cards)
            
    def sum(self) -> int:
        return sum((player.sum() for player in self.players))

class RecursiveCombat(Combat):
    def __init__(self, players: set, num=1):
        self.players = players
        self.past_states = set()
        self.num = num
        
    def is_finished(self) -> bool:
        return len(self.players) == 1

    def play(self) -> Player:
        while not self.is_finished():
            curr_state = self.state()
            if curr_state in self.past_states:
                return self.players[0]
            self.past_states.add(curr_state)

            self.round()
            self.players = [player for player in self.players if not player.has_lost()]
        return self.players[0]

    def round(self):
        plays = {player : player.play() for player in self.players}
        winner = None
        for player, card in plays.items():
            if card > player.deck_size():
                winner = max(plays, key=plays.get)
                played_cards = list(plays.values())
                played_cards.sort(reverse=True)
                winner.win(played_cards)
                return        
        winner_name = self.play_subgame(plays)
        for player in self.players:
            if player.name == winner_name:
                winner = player
        played_cards = [plays[winner]]
        for player in self.players:
            if player.name != winner_name:
                played_cards.append(plays[player])
        winner.win(played_cards)
        
    def play_subgame(self, plays):
        player_copies = list()
        for player, cards in plays.items():
            new_player = Player(player.name, player.deck[:cards])
            player_copies.append(new_player)
        subgame = RecursiveCombat(player_copies, self.num + 1)
        return subgame.play().name
            
    def sum(self) -> int:
        return sum((player.sum() for player in self.players))

    def state(self) -> str:
        return "".join([str(player) for player in self.players])

        
def parse_player(deck: str) -> Player:
    name, *cards = deck.split('\n')
    cards = [int(card) for card in cards]
    name = name[:-1] # remove ':' at end of player name
    return Player(name, cards)


def parse_input(path:str) -> set:
    with open(path, 'r') as fd:
        players = fd.read().split('\n\n')
        return {parse_player(player) for player in players}
players = parse_input('input.txt')

game = Combat(copy.deepcopy(players))

game.play()

game = RecursiveCombat(players)

game.play()


print(game.sum())
