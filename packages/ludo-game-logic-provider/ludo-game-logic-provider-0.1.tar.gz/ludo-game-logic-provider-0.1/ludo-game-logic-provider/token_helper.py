from enums.player_position_enum import *


startFieldIndexes = {
    PlayersPositionEnum.TL.value: 0,
    PlayersPositionEnum.TR.value: 13,
    PlayersPositionEnum.BR.value: 26,
    PlayersPositionEnum.BL.value: 39
}

relativeToAbsolute = [
    {"team": PlayersPositionEnum.TL.value, "relative": -1, "absolute": -1},
    {"team": PlayersPositionEnum.TR.value, "relative": -1, "absolute": -1},
    {"team": PlayersPositionEnum.BR.value, "relative": -1, "absolute": -1},
    {"team": PlayersPositionEnum.BL.value, "relative": -1, "absolute": -1}
]

# tokens base config
for i in range(52):
    relativeToAbsolute.append({"team": PlayersPositionEnum.TL.value, "relative": i, "absolute": (startFieldIndexes[PlayersPositionEnum.TL.value] + i) % 52})
    relativeToAbsolute.append({"team": PlayersPositionEnum.TR.value, "relative": i, "absolute": (startFieldIndexes[PlayersPositionEnum.TR.value] + i) % 52})
    relativeToAbsolute.append({"team": PlayersPositionEnum.BR.value, "relative": i, "absolute": (startFieldIndexes[PlayersPositionEnum.BR.value] + i) % 52})
    relativeToAbsolute.append({"team": PlayersPositionEnum.BL.value, "relative": i, "absolute": (startFieldIndexes[PlayersPositionEnum.BL.value] + i) % 52})

# tokens winning line
for i in range(6):
    relativeToAbsolute.append({"team": PlayersPositionEnum.TL.value, "relative": 52 + i, "absolute": "b" + str(i)})
    relativeToAbsolute.append({"team": PlayersPositionEnum.TR.value, "relative": 52 + i, "absolute": "r" + str(i)})
    relativeToAbsolute.append({"team": PlayersPositionEnum.BR.value, "relative": 52 + i, "absolute": "g" + str(i)})
    relativeToAbsolute.append({"team": PlayersPositionEnum.BL.value, "relative": 52 + i, "absolute": "y" + str(i)})

def relativeToAbsoluteIndex(relative, team):
    find = None

    for e in relativeToAbsolute:
         if e["relative"] == relative and e["team"] == team:
            find = e

    if not find:
        return -1
    return find["absolute"]

def a2r(absolute, team):
    find = next((e for e in relativeToAbsolute if e["absolute"] == absolute and e["team"] == team), None)
    if not find:
        return None
    return find["relative"]