import pygame
from random import choice
from game.Snake import Snake
from game.Food import Food  # Importer la classe Food depuis le module Food


def retrieve_high_score():
    try:
        with open("assets/high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        with open("assets/high_score.txt", "w") as f:
            f.write("0")
            return 0


def update_high_score(score):
    high_score = retrieve_high_score()
    if score > high_score:
        with open("assets/high_score.txt", "w") as file:
            file.write(str(score))


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        print("Game created with width: {} and height: {}", (width // 2), (height // 2))
        self.snake = Snake(((width // 2), (height // 2)))  # Initialisation du serpent
        self.stillAlive = True
        self.pause = False
        self.food = None  # Initialisation de la nourriture
        self.highScore = retrieve_high_score()
        self.generate_food()  # Appel pour générer la première nourriture

    def generate_food(self):
        # Liste de toutes les positions valides sur la carte
        valid_positions = [(x, y) for x in range(self.width) for y in range(self.height) if
                           (x, y) not in self.snake.body]
        # Choisir aléatoirement une position parmi les positions valides
        food_pos = choice(valid_positions)
        # Créer un objet de la classe Food avec la position de la nourriture
        self.food = Food(food_pos)

    def update(self):
        if not self.pause:
            self.snake.move()  # Mettre à jour la position du serpent
        if self.check_collision():  # Vérifier les collisions
            self.stillAlive = False
        if self.snake.body[0][0] == self.food.pos:
            self.snake.grow()  # Augmenter la taille du serpent
            self.generate_food()  # Générer une nouvelle position pour la nourriture
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))  # Haut
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))  # Bas
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))  # Gauche
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))  # Droite
                elif event.key == pygame.K_SPACE and not self.stillAlive:
                    self.snake = Snake((self.width // 2, self.height // 2))
                    self.stillAlive = True
                elif event.key == pygame.K_p:
                    self.pause = not self.pause
        return True

    def check_collision(self):
        head, _ = self.snake.body[0]  # Obtenir les coordonnées de la tête du serpent
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            return True
        # Vérifier si la tête du serpent entre en collision avec son propre corps
        if head in [segment[0] for segment in self.snake.body[1:]]:
            return True
        return False

    def draw(self, screen):
        # Remplir l'écran avec un damier de couleur verte foncée et verte
        for y in range(96, 736, 32):
            for x in range(32, 672, 32):
                if (x // 32 + y // 32) % 2 == 0:
                    pygame.draw.rect(screen, (163, 208, 74), (x, y, 32, 32))
                else:
                    pygame.draw.rect(screen, (169, 216, 81), (x, y, 32, 32))
        if not self.stillAlive:
            self.game_over_screen(screen)
            update_high_score((len(self.snake.body) - 3) * 10)
        else:
            self.food.draw(screen)  # Dessiner la nourriture
            self.snake.draw(screen)  # Dessiner le serpent
        self.game_score_title(screen)
        pygame.display.flip()

    def game_over_screen(self, screen):
        font = pygame.font.Font(None, 40)
        textGameOver = font.render("Game Over!", True, (255, 0, 0))
        textTryAgain = font.render("Press SPACE to try again", True, (255, 0, 0))
        textExit = font.render("Press ESC to exit", True, (255, 0, 0))
        textRectExit = textExit.get_rect(center=(352, 420))
        textRectTryAgain = textTryAgain.get_rect(center=(352, 380))
        textRectGameOver = textGameOver.get_rect(center=(352, 280))
        screen.blit(textGameOver, textRectGameOver)
        screen.blit(textTryAgain, textRectTryAgain)
        screen.blit(textExit, textRectExit)

    def game_score_title(self, screen):
        fontScore = pygame.font.Font(None, 38)
        fontTitle = pygame.font.Font(None, 64)
        textScore = fontScore.render("Score: {}".format((len(self.snake.body) - 3) * 10), True, (255, 255, 255))
        textTitle = fontTitle.render("PySnake", True, (255, 255, 255))
        if (len(self.snake.body) - 3) * 10 > self.highScore:
            self.highScore = (len(self.snake.body) - 3) * 10
        textHighScore = fontScore.render("High Score: {}".format(self.highScore), True, (255, 255, 255))
        screen.blit(textTitle, (64, 24))
        screen.blit(textScore, (320, 20))
        screen.blit(textHighScore, (320, 50))
