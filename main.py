# pygame setup
import pygame

from game.Game import Game

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('PySnake')
clock = pygame.time.Clock()
running = True

# Créer une instance de la classe Game avec une carte de 20x20
game = Game(20, 20)

while running:
    running = game.handle_events()  # Gérer les événements
    game.update()  # Mettre à jour le jeu
    game.draw(screen)  # Dessiner le jeu à l'écran
    clock.tick(6)  # Limite les FPS à 10

pygame.quit()