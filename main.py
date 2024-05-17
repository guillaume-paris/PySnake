# pygame setup
import pygame

from game.Game import Game

pygame.init()
screen = pygame.display.set_mode((704, 768))
pygame.display.set_caption('PySnake')
clock = pygame.time.Clock()
running = True

# Créer une instance de la classe Game avec une carte de 20x20
game = Game(20, 20)

background_image = pygame.image.load("assets/background.png")
background_image = pygame.transform.scale(background_image, (704, 768))

while running:
    running = game.handle_events()  # Gérer les événements
    game.update()  # Mettre à jour le jeu
    screen.blit(background_image, (0, 0))
    game.draw(screen)  # Dessiner le jeu à l'écran
    clock.tick(6)  # Limite les FPS à 10

pygame.quit()