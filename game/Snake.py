import pygame
from pygame.rect import Rect


class Snake:
    def __init__(self, start_pos, direction=(1, 0)):
        self.body = [(start_pos, direction)]  # Corps initial de longueur 1 avec direction
        self.growth_pending = 2  # Nombre d'unités de croissance à effectuer
        self.sprite_sheet = pygame.image.load("assets/snake_tileset_64x64.png")  # Charger la sprite sheet
        self.straight_body_sprite_rects = {
            (1, 0): pygame.Rect(64, 0, 64, 64),  # Corps de serpent horizontal
            (-1, 0): pygame.Rect(64, 0, 64, 64),  # Corps de serpent horizontal
            (0, 1): pygame.Rect(128, 64, 64, 64),  # Corps de serpent vertical
            (0, -1): pygame.Rect(128, 64, 64, 64),  # Corps de serpent vertical
        }
        self.turn_body_sprite_rects = {
            (1, 0): pygame.Rect(0, 0, 64, 64),  # Coin supérieur gauche
            (-1, 0): pygame.Rect(128, 0, 64, 64),  # Coin supérieur droit
            (0, 1): pygame.Rect(0, 64, 64, 64),  # Coin inférieur gauche
            (0, -1): pygame.Rect(128, 128, 64, 64),  # Coin inférieur droit
        }
        self.tail_body_sprite_rects = {
            (-1, 0): pygame.Rect(192, 192, 64, 64),  # Queue du serpent vers la droite
            (1, 0): pygame.Rect(256, 128, 64, 64),  # Queue du serpent vers la gauche
            (0, -1): pygame.Rect(192, 128, 64, 64),  # Queue du serpent vers le bas
            (0, 1): pygame.Rect(256, 192, 64, 64)  # Queue du serpent vers le haut
        }
        self.head_sprite_rects = {
            (1, 0): pygame.Rect(256, 0, 64, 64),  # Tête du serpent tournée vers la droite
            (-1, 0): pygame.Rect(192, 64, 64, 64),  # Tête du serpent tournée vers la gauche
            (0, 1): pygame.Rect(256, 64, 64, 64),  # Tête du serpent tournée vers le bas
            (0, -1): pygame.Rect(192, 0, 64, 64),  # Tête du serpent tournée vers le haut
        }

    def move(self):
        head, head_dir = self.body[0]  # Obtenir la position et la direction de la tête
        new_head = (head[0] + head_dir[0], head[1] + head_dir[1])  # Nouvelle position de la tête
        self.body.insert(0, (new_head, head_dir))  # Ajouter la nouvelle tête du serpent

        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.body.pop()  # Supprimer la dernière partie du corps pour maintenir la taille constante

    def change_direction(self, new_direction):
        # Changer uniquement la direction de la tête du serpent
        head, head_dir = self.body[0]
        self.body[0] = (head, new_direction)

    def grow(self):
        # Augmenter le nombre d'unités de croissance
        self.growth_pending += 1

    def draw(self, screen):
        for i, (segment, segment_dir) in enumerate(self.body):
            if i == 0:
                print("head: ", segment_dir)
                # Dessiner la tête du serpent dans la bonne direction
                sprite_rect = self.head_sprite_rects[segment_dir]
            elif i == len(self.body) - 1:
                print("tail: ", segment_dir)
                # Dessiner la queue du serpent dans la bonne direction
                sprite_rect = self.tail_body_sprite_rects[segment_dir]
            else:
                # Vérifier si un segment est un virage
                prev_segment, prev_segment_dir = self.body[i - 1]
                next_segment, next_segment_dir = self.body[i + 1]
                if prev_segment_dir != next_segment_dir:
                    sprite_rect = self.turn_body_sprite_rects[next_segment_dir]  # Utiliser la direction du prochain segment pour le virage
                else:
                    sprite_rect = self.straight_body_sprite_rects[segment_dir]  # Corps droit

            sprite = self.sprite_sheet.subsurface(sprite_rect)  # Extraire le sprite de la sprite sheet
            scaled_sprite = pygame.transform.scale(sprite, (64, 64))  # Redimensionner le sprite à 64x64
            screen.blit(scaled_sprite, (segment[0] * 64, segment[1] * 64))  # Dessiner le sprite sur l'écran
