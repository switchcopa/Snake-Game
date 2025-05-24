
def check_collisions(player, SCREEN_WIDTH, SCREEN_HEIGHT):
    position = player.position()

    for x, y in position:
        if x < 0 or y < 0 or x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT:
            print("GAME OVER")
            return True

    return False