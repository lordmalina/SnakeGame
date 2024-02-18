# Třída pro vytvoření tlačítka

import pygame

class Button:
        def __init__(self, x, y, image, scale, hover_image):
            self.width = image.get_width() # Získání šířky obrázku
            self.height = image.get_height() # Získání výšky obrázku
            self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale))) # Změna velikosti obrázku
            self.rect = self.image.get_rect() # získání velikosti obrázku
            self.rect.center = (x, y) # pozice středu tlačítka
            self.clicked = False # Proměnná pro zjištění, zda je tlačítko stisknuto
            self.hover = pygame.transform.scale(hover_image, (int(self.width * scale), int(self.height * scale))) # obrázek pro hover efekt tlačítka

        def hover(self, surface): # Funkce pro hover efekt tlačítka, která se volá, když je myš nad tlačítkem
            surface.blit(self.hover, (self.rect.x, self.rect.y))

        def draw(self, surface): # Funkce pro vykreslení tlačítka, která zároveň vrací True, pokud je tlačítko stisknuto, aby bylo možné vykonávat různé akce
            action = False # Proměnná pro vrácení True, pokud je tlačítko stisknuto
            pos = pygame.mouse.get_pos() # Získání pozice myši
            if self.rect.collidepoint(pos): # Podmínka pro zjištění, zda je myš nad tlačítkem
                surface.blit(self.hover, (self.rect.x, self.rect.y)) # Vykreslení tlačítka
                if pygame.mouse.get_pressed()[0] and self.clicked == False: # Podmínka pro zjištění, zda je tlačítko stisknuto
                    self.clicked = True
                    action = True # Vrácení True, pokud je tlačítko stisknuto
            else:
                surface.blit(self.image, (self.rect.x, self.rect.y)) # Vykreslení tlačítka

            if pygame.mouse.get_pressed()[0] == False:
                self.clicked = False

            return action