from game_logic_provider import GameLogicProvider
from enums.player_position_enum import PlayersPositionEnum
from states.player_state import PlayerState
from states.player_token_state import PlayerTokenState
from utils_helper import shuffle

class Room:
    def __init__(self, state):
        self.state = state
        self.logic = GameLogicProvider(self)
        self.teamColors = shuffle(['blue', 'red', 'green', 'yellow'])
        self.teamPositions = [PlayersPositionEnum.BL, PlayersPositionEnum.TL, PlayersPositionEnum.TR, PlayersPositionEnum.BR]

    def createBots(self, numberOfPlayers):
        for i in range(1, numberOfPlayers):
            self.state.players[
                'bot' + str(i)
            ] = PlayerState(
                self.teamPositions.pop(0),
                self.teamColors.pop(0),
                [
                    PlayerTokenState(0, -1, 0 if self.state.isQuickMode else -1, 2 if self.state.isQuickMode else 1, 0),
                    PlayerTokenState(1, -1, 0 if self.state.isQuickMode else -1, 2 if self.state.isQuickMode else 1, 1 if self.state.isQuickMode else 0),
                    PlayerTokenState(2, -1, -1, 1, 0),
                    PlayerTokenState(3, -1, -1, 1, 0),
                ],
                0,
                0,
                'Computer',
                False,
                self.state.isQuickMode,
                i,
                '',
                '',
                '',
                0,
                '',
            )
        self.setActivePlayer('bot1')

    def setActivePlayer(self, playerId):
        self.state.activePlayer = playerId

