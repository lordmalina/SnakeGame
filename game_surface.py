# Třída pro vytvoření herní plochy

import pygame

class Grid:
    def __init__(self, surface, columns, rows):
        self.surface = surface # Herní plocha
        self.columns = columns # Počet sloupců
        self.rows = rows # Počet řádků
        self.size = (self.surface.get_height(), self.surface.get_height()) # Velikost herní plochy
        self.cell_size = (self.size[0] / self.columns, self.size[1] / self.rows) # Velikost jedné buňky
        self.start_pos = (self.surface.get_width() - self.surface.get_height()) # Pozice, od které se začne vykreslovat herní plocha
        self.center = (self.start_pos + (self.size[0] / 2), self.size[1] / 2) # Střed herní plochy

    def draw(self): # Funkce pro vykreslení herní plochy
        for i in range(self.columns): # Cyklus pro vykreslení sloupců
            for j in range(self.rows): # Cyklus pro vykreslení řádků
                if (i + j) % 2 == 0: # Podmínka pro zjištění, zda je buňka sudá nebo lichá, aby se mohla vykreslit správná barva a vznikala šachovnice
                    color = (139, 203, 6) # Barva pozadí
                    # vykreslení každé sudé buňky
                    pygame.draw.rect(self.surface, color, ((i * self.cell_size[0]) + self.start_pos,
                                                            (j * self.cell_size[1]), self.cell_size[0], self.cell_size[1]))
                else:
                    color = (161, 225, 28) # Barva pozadí
                    # vykreslení každé liché buňky
                    pygame.draw.rect(self.surface, color, ((i * self.cell_size[0]) + self.start_pos,
                                                            (j * self.cell_size[1]), self.cell_size[0], self.cell_size[1]))