# Třída, která vytváří nepřátelského hada

import pygame
import random
import time

class HostileSnake:
    def __init__(self, x, y, size, par, direction, fps, length = 12):
        self.x = x
        self.y = y
        self.size = size # Velikost jednoho bloku hada
        self.direction = direction # Směr pohybu hada
        self.body = [[self.x, self.y]] # Tělo hada - list souřadnic
        self.parameter = par # Parametr pro odkaz na objekt GameSurface
        self.length = length # Délka hada
        self.fps = fps # FPS
        self.last_turn_time = time.time() # Proměnná pro omezení změny směru hada

    def native_length(self): # Funkce pro nastavení délky hada na začátku hry
        # podmínky, které určují směr generování hada podle toho jakým směrem se bude pohybovat
        # Podle délky hada se pomocí cyklu for přidají do listu body souřadnice jednotlivých částí hada. Přidají se v opačném směru než je směr pohybu hada
        if self.direction == "right":
            for i in range(1, self.length):
                self.body.append([self.x - i * self.parameter.cell_size[0], self.y])
        elif self.direction == "left":
            for i in range(1, self.length):
                self.body.append([self.x + i * self.parameter.cell_size[0], self.y])
        elif self.direction == "up":
            for i in range(1, self.length):
                self.body.append([self.x, self.y + i * self.parameter.cell_size[1]])
        elif self.direction == "down":
            for i in range(1, self.length):
                self.body.append([self.x, self.y - i * self.parameter.cell_size[1]])

    def increase_length(self): # Funkce pro zvýšení délky hada
        # podmínky, které určují směr generování hada podle toho jakým směrem se pohybuje
        # Tato funkce se volá, když had sežere jablko. Přidá se nová část hada na konec hada. Přidá se v opačném směru než je směr pohybu hada
        if self.direction == "right":
            self.body.append([self.body[-1][0] - self.parameter.cell_size[0], self.body[-1][1]])
        elif self.direction == "left":
            self.body.append([self.body[-1][0] + self.parameter.cell_size[0], self.body[-1][1]])
        elif self.direction == "up":
            self.body.append([self.body[-1][0], self.body[-1][1] + self.parameter.cell_size[1]])
        elif self.direction == "down":
            self.body.append([self.body[-1][0], self.body[-1][1] - self.parameter.cell_size[1]])

    def move(self): # Funkce pro pohyb hada
        self.body = self.body[-1:] + self.body[:-1] # Posunutí těla hada

        # Podmínky pro pohyb hada, kde self.body[0] je hlava hada a self.body[1] je první část hada za hlavou
        # druhé číslo označuje souřadnici X a Y. 0 je X a 1 je Y
        # např. self.body[0][0] je X souřadnice hlavy hada a self.body[0][1] je Y souřadnice hlavy hada
        if self.direction == "right":
            self.body[0][1] = self.body[1][1] 
            self.body[0][0] = self.body[1][0] + self.parameter.cell_size[1]
        elif self.direction == "left":
            self.body[0][1] = self.body[1][1]
            self.body[0][0] = self.body[1][0] - self.parameter.cell_size[1]
        elif self.direction == "up":
            self.body[0][0] = self.body[1][0]
            self.body[0][1] = self.body[1][1] - self.parameter.cell_size[1]
        elif self.direction == "down":
            self.body[0][0] = self.body[1][0]
            self.body[0][1] = self.body[1][1] + self.parameter.cell_size[1]

    def change_direction(self, new_direction): # Funkce pro změnu směru hada
        # Tento časový interval pomáhá omezit změnu směru hada sám do sebe, což by v našem případě vedlo ke Game Over.
        current_time = time.time() # Proměnná pro uložení aktuálního času
        cooldown_time = 1 / (2 * self.fps) # Proměnná pro uložení času, který musí uplynout, aby se mohl had otočit

        if current_time - self.last_turn_time > cooldown_time: # Podmínka, která určuje, zda se had může otočit
            # Podmínky pro změnu směru hada
            if new_direction == "right" and self.direction != "left":
                self.direction = new_direction
            elif new_direction == "left" and self.direction != "right":
                self.direction = new_direction
            elif new_direction == "up" and self.direction != "down":
                self.direction = new_direction
            elif new_direction == "down" and self.direction != "up":
                self.direction = new_direction
            self.last_turn_time = current_time # Uložení času poslední změny směru hada

    def draw(self, surface): # Funkce pro vykreslení hada
        # barvy pro vykreslení hada
        outer_color = (0, 0, 0) # Barva okraje hada
        inner_color = (105,105,105) # Barva těla hada
        head_color = (50, 50, 50) # Barva hlavy hada

        # Podmínka, která určuje, zda se má vykreslit hlava hada
        draw_head = True # Proměnná pro určení, zda se má vykreslit hlava hada
        for segment in self.body:
            if draw_head == True: # Tato podmínka vždy projde jako první a vykreslí hlavu hada, později nastaví proměnnou draw_head na False a hlava se už nevykreslí
                pygame.draw.rect(surface, outer_color, (segment[0], segment[1], self.size, self.size))
                pygame.draw.rect(surface, head_color, (segment[0] + 1, segment[1] + 1, self.size - 2, self.size - 2))
                draw_head = False
            else:
                pygame.draw.rect(surface, outer_color, (segment[0], segment[1], self.size, self.size))
                pygame.draw.rect(surface, inner_color, (segment[0] + 1, segment[1] + 1, self.size - 2, self.size - 2))

    def turn_when_hit_wall(self): # Funkce pro otočení hada, když narazí do zdi
        # Každá z podmínek představuje jednu stěnu, buď levou, pravou, horní nebo dolní
        # Každá z nich má 2 podpodmínky, které zajišťují to, aby se had při nárazu do stěny otočil směrem ke středu stěny
        if self.body[0][0] <= self.parameter.start_pos and self.direction == "left": # Podmínka pro levou stěnu 
            if self.body[0][1] <= self.parameter.center[1]:
                self.change_direction("down")
            elif self.body[0][1] > self.parameter.center[1]:
                self.change_direction("up")
        elif self.body[0][0] >= self.parameter.size[0] - self.size + self.parameter.start_pos and self.direction == "right": # Podmínka pro pravou stěnu
            if self.body[0][1] <= self.parameter.center[1]:
                self.change_direction("down")
            elif self.body[0][1] > self.parameter.center[1]:
                self.change_direction("up")
        elif self.body[0][1] <= 0 and self.direction == "up": # Podmínka pro horní stěnu
            if self.body[0][0] <= self.parameter.center[0]:
                self.change_direction("right")
            elif self.body[0][0] > self.parameter.center[0]:
                self.change_direction("left")
        elif self.body[0][1] >= self.parameter.size[1] - self.size and self.direction == "down": # Podmínka pro dolní stěnu
            if self.body[0][0] <= self.parameter.center[0]:
                self.change_direction("right")
            elif self.body[0][0] > self.parameter.center[0]:
                self.change_direction("left")

    def random_turn(self): # Funkce pro náhodné otočení hada
        # Tato funkce je volána v pravidelných intervalech a otočí hada náhodně
        # Pole je pomocí podmínek pomyslně rozděleno do 4 kvadrantů a had se v každém smí otočit jen do dvou sousedních kvadrantů, nikoliv do stěny.
        # to zajišťuje, že se had tzv. "motá" kolem středu herní plochy
        # např. pokud se had nachází v pravém horním kvadrantu, může změnit směr jen na "left" nebo "down
        # pokud ovšem současný směr je např. "right" a funkce mu vygeneruje směr "right", tak se nic nestane a to přidává na náhodnosti pohybu hada
        random_number = random.randint(0, 1) # Náhodné číslo pro určení směru hada
        if self.body[0][0] >= self.parameter.center[0] and self.body[0][1] <= self.parameter.center[1]: # Podmínka pro pravý horní kvadrant
            if random_number == 0 and self.direction != "right":
                self.change_direction("left")
            elif random_number == 1 and self.direction != "up":
                self.change_direction("down")
        elif self.body[0][0] < self.parameter.center[0] and self.body[0][1] <= self.parameter.center[1]: # Podmínka pro levý horní kvadrant
            if random_number == 0 and self.direction != "left":
                self.change_direction("right")
            elif random_number == 1 and self.direction != "up":
                self.change_direction("down")
        elif self.body[0][0] < self.parameter.center[0] and self.body[0][1] > self.parameter.center[1]: # Podmínka pro levý dolní kvadrant
            if random_number == 0 and self.direction != "left":
                self.change_direction("right")
            elif random_number == 1 and self.direction != "down":
                self.change_direction("up")
        elif self.body[0][0] >= self.parameter.center[0] and self.body[0][1] > self.parameter.center[1]: # Podmínka pro pravý dolní kvadrant
            if random_number == 0 and self.direction != "right":
                self.change_direction("left")
            elif random_number == 1 and self.direction != "down":
                self.change_direction("up")