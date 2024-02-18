# Třída pro vložení obrázku, v našem případě loga

import pygame

class Logo:
        def __init__(self, x, y, image, scale):
            self.width = image.get_width() # Získání šířky obrázku
            self.height = image.get_height() # Získání výšky obrázku
            self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale))) # Změna velikosti obrázku
            self.rect = self.image.get_rect() # získání obrázku
            self.rect.center = (x, y) # Střed obrázku

        def draw(self, surface): # Funkce pro vykreslení loga
            surface.blit(self.image, (self.rect.x, self.rect.y)) # Vykreslení loga