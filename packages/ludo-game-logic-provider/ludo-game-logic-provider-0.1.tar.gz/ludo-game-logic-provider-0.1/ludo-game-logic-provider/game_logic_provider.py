from token_helper import *
from enums.player_position_enum import PlayersPositionEnum
from enums.hint_state_enum import HintStateEnum

class GameLogicProvider:
    def __init__(self, room):
        self.room = room

    def nextActionsPlayerWithWallCollision(self, diceValue=0):
        currentPlayer = self._currentPlayerData()
        otherPlayers = self._otherPlayersData()
        freeToActionBotWall = self._checkActionWall(diceValue, currentPlayer, otherPlayers)

        if len(freeToActionBotWall) == 0:
            return []
        actions = []
        for tokenIndex in freeToActionBotWall:

            if (
                (not self.room.state.isQuickMode and currentPlayer['tokens'][tokenIndex] + diceValue <= 57)
                or (self.room.state.isQuickMode and currentPlayer['finishBlocked'] == False and currentPlayer['tokens'][tokenIndex] + diceValue <= 57)
                or (self.room.state.isQuickMode and currentPlayer['finishBlocked'] == True)
            ) and (
                (currentPlayer['tokens'][tokenIndex] == -1 and diceValue == 6)
                or currentPlayer['tokens'][tokenIndex] > -1
            ):
                actions.append({
                    'availableTokenIndex': tokenIndex,
                    'tokenValue': currentPlayer['tokens'][tokenIndex],
                    'typeMove': 'RELEASE' if currentPlayer['tokens'][tokenIndex] == -1 else 'OTHER'
                })

        self.updateStateTokens(
            [token for token in currentPlayer['stateTokens'] if any(action['availableTokenIndex'] == token.index for action in actions)],
            [token for token in currentPlayer['stateTokens'] if all(action['availableTokenIndex'] != token.index for action in actions)],
            diceValue
        )
        
        return actions

    def updateStateTokens(self, activePlayerTokens, notActivePlayerTokens, newDeciRollValue):
        for token in activePlayerTokens:
            if token.position == -1 and token.prevPosition == -1:
                token.stateHint = HintStateEnum.NONE
            if self.checkTokenOnSafeZone(token.position + newDeciRollValue):
                token.stateHint = HintStateEnum.SAFE
            elif self.canTokenKillOtherPlayerWithSaveZone(token.position + newDeciRollValue):
                token.stateHint = HintStateEnum.KILL
            elif self.checkTokenOnWin(token.position + newDeciRollValue, token.position):
                token.stateHint = HintStateEnum.WIN
            else:
                token.stateHint = HintStateEnum.NONE
        for token in notActivePlayerTokens:
            token.stateHint = HintStateEnum.NONE

    def checkTokenOnSafeZone(self, position):
        currentPLayer = self._currentPlayerData()
        absCurrentTokenPosition = relativeToAbsoluteIndex(position, currentPLayer['team'])
        safeZones = list(map(lambda e: relativeToAbsoluteIndex(e, PlayersPositionEnum.TL.value), [0, 8, 13, 21, 26, 34, 39, 47]))
        return absCurrentTokenPosition in safeZones

    def checkTokenOnWin(self, positionWithDiceValue, position):
        currentPLayer = self._currentPlayerData()
        if position == 51:
            return False
        positionWithDiceValue = positionWithDiceValue + 1 if position == 50 else positionWithDiceValue
        return currentPLayer['finishBlocked'] == False and positionWithDiceValue == 57

    def canTokenKillOtherPlayerWithSaveZone(self, position):
        currentPLayer = self._currentPlayerData()
        otherPlayers = self._otherPlayersData()
        absCurrentTokenPosition = relativeToAbsoluteIndex(position, currentPLayer['team'])
        safeZones = list(map(lambda e: relativeToAbsoluteIndex(e, PlayersPositionEnum.TL.value), [0, 8, 13, 21, 26, 34, 39, 47]))
        if absCurrentTokenPosition in safeZones:
            return None
        for player in otherPlayers:
            tokens = player['tokens']
            team = player['team']
            playerId = player['playerId']
            for tokenIndex in range(len(tokens)):
                absTokenPlayer = relativeToAbsoluteIndex(tokens[tokenIndex], team)
                if absCurrentTokenPosition == absTokenPlayer:
                    return {
                        'killedPlayerId': playerId,
                        'tokenIndex': tokenIndex
                    }
        return None

    def countTokensOnPosition(self, relative, team, withoutIndex=None):
        if relative == -1:
            return 1
        absolutePosition = relativeToAbsoluteIndex(relative, team)
        count = 0
        for player in self.room.state.players.values():
            if withoutIndex == None or player.playerId != self.room.state.activePlayer or (player.playerId == self.room.state.activePlayer and withoutIndex != None and withoutIndex != withoutIndex):
                tokens = player.tokens
                count += sum(1 for token in tokens if relativeToAbsoluteIndex(token.position, player.team) == absolutePosition)
        return count

    def _currentPlayerData(self):
        activePlayer = self.room.state.activePlayer
        currentPlayer = self.room.state.players[activePlayer]
        return {
            'finishBlocked': currentPlayer.finishBlocked,
            'tokens': [e.position for e in currentPlayer.tokens],
            'team': currentPlayer.team.value,
            'teamColor': currentPlayer.teamColor,
            'diceValue': currentPlayer.diceValue,
            'stateTokens': currentPlayer.tokens
        }

    def _otherPlayersData(self):
        activePlayer = self.room.state.activePlayer
        return [
            {
                'playerId': playerId,
                'tokens': [e.position for e in player.tokens],
                'team': player.team,
                'teamColor': player.teamColor
            }
            for playerId, player in self.room.state.players.items()
            if playerId != activePlayer
        ]

    def _checkActionWall(self, roll, currentPlayer, otherPLayers):
        walls = []
        for player in otherPLayers:
            walls += self._getPlayerWalls(player['tokens'], player['team'])

        availablePlayerIndex = []
        for i in range(len(currentPlayer['tokens'])):
            if currentPlayer['tokens'][i] == -1:
                availablePlayerIndex.append(i)
                continue
            currentPosition = relativeToAbsoluteIndex(self._nextTokenPositionForWall(currentPlayer, i, roll), currentPlayer['team'])
            wasCatch = currentPosition in walls
            if not wasCatch:
                availablePlayerIndex.append(i)
        return availablePlayerIndex

    def _nextTokenPositionForWall(self, currentPlayer, index, roll):
        if currentPlayer['finishBlocked'] == True and currentPlayer['tokens'][index] <= 51 and (currentPlayer['tokens'][index] + roll) > 51:
            return (currentPlayer['tokens'][index] + roll) % 52
        return currentPlayer['tokens'][index] + roll

    def _getPlayerWalls(self, tokens, team):
        indexes = {}
        for token in tokens:
            if token in indexes:
                indexes[token] += 1
            else:
                indexes[token] = 1
        return [int(e) for e in indexes.keys() if indexes[e] > 1]