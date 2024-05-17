import pygame

class Food:
    def __init__(self, pos):
        self.pos = pos
        self.sprite_sheet = pygame.image.load("assets/snake_tileset_64x64.png")
        self.sprite_rect = pygame.Rect(0, 192, 64, 64)  # Example position for an apple sprite

    def draw(self, screen):
        sprite = self.sprite_sheet.subsurface(self.sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (32, 32))
        screen.blit(scaled_sprite, (self.pos[0] * 32 + 32, self.pos[1] * 32 + 96))