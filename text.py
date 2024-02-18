# Třída pro vkládání textu

class Text:
    def __init__(self, surface, font, color, x, y):
        self.surface = surface # Plocha, na kterou se bude text vykreslovat
        self.font = font # Font textu
        self.color = color # Barva textu

        # Pozice středu textu
        self.x = x
        self.y = y

    def draw(self, text): # Funkce pro vykreslení textu
        img = self.font.render(text, True, self.color)
        self.center = (self.x - img.get_width() // 2, self.y - img.get_height() // 2) # Střed textu
        self.surface.blit(img, self.center) # Vykreslení textu