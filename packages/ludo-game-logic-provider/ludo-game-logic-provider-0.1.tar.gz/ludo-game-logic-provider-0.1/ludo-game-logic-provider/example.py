# Assuming the Room and RoomState classes have been translated to Python and exist in the "rooms" and "states" modules respectively


from room import Room
from states.room_state import RoomState

def main():
    room = Room(
        RoomState()
    )

    room.createBots(4)

    print(room.state.players.keys())

    room.setActivePlayer('bot1')

    print(room.logic.nextActionsPlayerWithWallCollision(2))

    room.state.players['bot1'].tokens[0].position = 6
    room.state.players['bot1'].tokens[1].position = 2

    print(room.logic.nextActionsPlayerWithWallCollision(2))

    print('hint = ', room.state.players['bot1'].tokens[0].stateHint.value)
    print('hint = ', room.state.players['bot1'].tokens[1].stateHint.value)

main()


