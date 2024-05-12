import pygame


class Food:
    def __init__(self, pos):
        self.pos = pos  # Position de la nourriture sur la carte

    def draw(self, screen):import pygame

class Food:
    def __init__(self, pos):
        self.pos = pos  # Position de la nourriture sur la carte
        self.sprite_sheet = pygame.image.load("assets/snake_tileset_64x64.png")  # Charger la sprite sheet
        self.sprite_rect = pygame.Rect(0, 192, 64, 64)  # Rect pour extraire un sprite de 64x64

    def draw(self, screen):
        # Extraire le sprite de la sprite sheet
        sprite = self.sprite_sheet.subsurface(self.sprite_rect)
        # Redimensionner le sprite à 32x32
        scaled_sprite = pygame.transform.scale(sprite, (32, 32))
        # Dessiner le sprite sur l'écran
        screen.blit(scaled_sprite, (self.pos[0] * 32, self.pos[1] * 32))

        pygame.draw.rect(screen, (0, 255, 0), (self.pos[0] * 25, self.pos[1] * 25, 25, 25))
