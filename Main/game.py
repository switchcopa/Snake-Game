import random
import config
from Main.config import GOLDEN_APPLE_SPAWN_CHANCE, APPLE_SPAWN_CHANCE
from snake import *
import collision
import food
import json

# you can set your own path for a json folder
path = "C:\\Users\\100TR\\PycharmProjects\\SnakeGame\\Main\\scores.json"

class Game:
    def __init__(self, width, height, caption):
        self.width = width
        self.height = height
        self.caption = str(caption)
        self.running = False
        self.paused = False
        self.over = False

    def set_screen(self):
        # set the width, height and caption of the window
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

        return screen

    def run(self):
        # initialize pygame
        pygame.init()
        pygame.font.init()

        # clock to control the frame rate
        clock = pygame.time.Clock()
        fps = config.FPS
        screen = self.set_screen()

        # snake object
        snake = Snake(speed=config.SNAKE_SPEED)

        # load the data (I used json for database lol)
        try:
            with open(path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {
                "high_score" : 0
                # put more stuff in here later
            }

        last_spawned = pygame.time.get_ticks() # this controls the apple spawning time
        last_move = pygame.time.get_ticks() # update the snake
        move_delay = 250 / snake.speed # delay time to update the snake's position
                                       # likely used for snake's speed

        # set the font
        font = pygame.font.SysFont(config.FONT, config.FONT_SIZE)
        # render text for pause
        pause_text = font.render("GAME PAUSED", True, colors.RED)

        if self.running is False:
            self.running = True

            apple = None # current apple spawned is None
            apple_type = None # the type or color of the apple

            while self.running:
                if not self.paused and not self.over:

                    now = pygame.time.get_ticks()

                    screen.fill(colors.BLACK) # fill the screen with full black

                    # basically everything that has to do with text
                    text_score = font.render("Score: ", True, colors.WHITE)
                    score = font.render(str(snake.score), True, colors.WHITE)
                    body_count = font.render("Count:", True, colors.WHITE) # Please don't make fun of the variable name
                    count = font.render(str(snake.count()), True, colors.WHITE)
                    game_over = font.render("GAME OVER", True, colors.RED)
                    prompt_replay = font.render("Press Space to replay", True, colors.YELLOW)
                    high_score_display = font.render("High Score: ", True, colors.GREEN)

                    # display the text
                    screen.blit(text_score, (20, 20))
                    screen.blit(score, (125, 22))
                    screen.blit(count, (350, 20))
                    screen.blit(body_count, (250, 20))

                    # display the snake
                    snake.draw(screen)

                    # spawn the apple
                    if not apple and now - last_spawned >= config.FOOD_SPAWN_TIME:
                        chance = random.randint(0, APPLE_SPAWN_CHANCE)

                        if GOLDEN_APPLE_SPAWN_CHANCE < chance <= APPLE_SPAWN_CHANCE:
                            apple = food.Apple.spawn(screen)
                            apple_type = colors.GREEN
                        else:
                            apple = food.GoldenApple.spawn(screen)
                            apple_type = colors.YELLOW
                        last_spawned = now

                    # display the actual apple
                    if apple:
                        pygame.draw.rect(screen, apple_type,
                                         (*apple, 20, 20))

                    # eat the food and grow size dependent on the config settings
                    if snake.position()[0] == apple and apple_type == colors.GREEN:
                        snake.score += config.SCORE_INCREMENT_GREEN
                        call_count = config.GROW_SIZE_APPLE
                        while call_count > 0:
                            snake.grow(apple)
                            call_count -= 1

                        apple = None # delete the apple

                    # eat the golden apple (more special)
                    elif snake.position()[0] == apple and apple_type == colors.YELLOW:
                        snake.score += config.SCORE_INCREMENT_GOLDEN
                        call_count = config.GROW_SIZE_GOLDEN_APPLE
                        while call_count > 0:
                            snake.grow(apple)
                            call_count -= 1

                        apple = None

                    # Move the snake, and check if it collides with the border
                    if now - last_move > move_delay:
                        snake.move()
                        if collision.check_collisions(snake, config.WIDTH, config.HEIGHT):
                            screen.blit(game_over, (config.WIDTH // 2 - 100, config.HEIGHT // 2 - 30))
                            # game over
                            self.over = True
                            # display the prompts
                            screen.blit(prompt_replay, (config.WIDTH // 2 - 160, config.HEIGHT // 2 + 50))
                            screen.blit(high_score_display, (config.WIDTH // 2 - 100, config.HEIGHT // 2 - 100))

                            # control the high score
                            max_high_score = snake.count()

                            if max_high_score > data["high_score"]:

                                data["high_score"] = max_high_score
                                with open(path, 'w') as file:
                                    json.dump(data, file, indent=4)

                            high_score_count = font.render(
                                str(data["high_score"]),
                                True, colors.GREEN)

                            screen.blit(
                                high_score_count, (
                                    config.WIDTH // 2 + 80,
                                    config.HEIGHT // 2 - 100))

                        # set the last move to be when was this move
                        last_move = now

                clock.tick(fps)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    # controls the user input for the snake
                    # for each direction, the snake's body parts follows the head
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and snake.direction != "DOWN":
                            snake.direction = "UP"
                        if event.key == pygame.K_DOWN and snake.direction != "UP":
                            snake.direction = "DOWN"
                        if event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                            snake.direction = "LEFT"
                        if event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                            snake.direction = "RIGHT"

                        # this controls the pause menu
                        if event.key == pygame.K_ESCAPE:
                            self.paused = not self.paused
                            screen.blit(pause_text, (
                                config.WIDTH // 2 - 100,
                                config.HEIGHT // 2 - 30))

                        # this controls to restart the game
                        if event.key == pygame.K_SPACE and self.over:
                            snake = Snake()
                            apple = None
                            last_spawned = pygame.time.get_ticks()
                            last_move = pygame.time.get_ticks()
                            self.running = True
                            self.paused = False
                            self.over = False

                # update the display
                pygame.display.flip()