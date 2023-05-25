import pygame
import numpy as np
import random as rd
from time import sleep
import os

win_width = 1200
win_height = 700
money = 0

pygame.init()
win = pygame.display.set_mode((win_width,win_height)) # window surface
pygame.display.set_caption("Power-Stars")

# Load the slot machine images
background_image = pygame.image.load("img/background.jpg")
slot_image = pygame.image.load("img/slot.png")

# Scale the images to fit the screen
background_image = pygame.transform.scale(background_image, (win_width, win_height))

# Define the symbols
symbols = [" ", "img/symbol1.png", "img/symbol2.png", "img/symbol3.png", "img/symbol4.png", "img/symbol5.png", "img/symbol6.png", "img/symbol7.png"]
symbol_positions = [(110, 130), (310, 130), (510, 130), (710, 130), (910, 130), # up 
                    (110, 280), (310, 280), (510, 280), (710, 280), (910, 280), # middle
                    (110, 430), (310, 430), (510, 430), (710, 430), (910, 430)] # down

# Define the Cards
Poker = ["img/red.png", "img/black.png"]
card_positions = []

# create a font object.
font = pygame.font.Font('freesansbold.ttf', 32)
user_text = ''

input_rect = pygame.Rect(win_width // 2 - 50, win_height // 2 + 100, 140, 32)
input_rect_select = pygame.Rect(win_width // 2 - 300, win_height // 2 + 280, 140, 32)

####################################################################################################################

class Cards: # Dublaj Rosie-Neagra :p
    _cards = ["R","B"]
    _history = []
    card_images = []
    card_poz = [110, 130] # fake tuple

    def RedBlack(self, money) -> bool:
        global card_positions

        if money == 0: 
            return 0

        k = 0 # Nr max 
        while True:
            choice = TextInputRedBlack(user_text, font, input_rect, self.card_images)
            if choice[0].lower() == 'n':
                return money
            elif choice[0].lower() == 'r' or choice[0].lower() == 'b':
                if k == 3:
                    return money
                    
                #print(self._history)
                chance = rd.choice(self._cards)

                if len(self._history) > 4: # Reset to not load the page
                    self._history.clear()
                    card_positions = []
                    self.card_poz = [110, 130]
                    self.card_images = []
               
                self._history.append(chance) # Feature provizoriu
                for i in self._history: # Graphic interface
                    if i[0] == "R":
                        #print("Rosie")
                        card_image = pygame.image.load(Poker[0])
             
                    elif i[0] == "B":
                        #print("Neagra")
                        card_image = pygame.image.load(Poker[1])
                
                    card_image = pygame.transform.scale(card_image, (150, 150))
                    self.card_images.append(card_image)
                                      
                    card_positions.append( (self.card_poz[0] , self.card_poz[1]))
                    self.card_poz[0] = self.card_poz[0] + 200

                
                self.card_poz = [110, 130] # raload the vector position
                card = choice
                #print(f"{card} == {chance} ") # selected card and chance card

                if card.lower() == chance.lower(): # selected card and chance card
                    money = 2 * money
                    k += 1
                else:
                    return 0 

class Gamble(Cards):
    A = np.zeros((3,5), dtype=int )
    lin = 3
    col = 5

    def __init__(self, money, lines) -> bool: # Retinem suma
        self.money = money
        self.lines = lines

    def Spin(self, gamble):
        if self.money <= 0:
            print("You dont have money to bet!")
            ok = 3
            return False, int(ok)

        self.money -= gamble # Sold update
        symbol_images = [] # It is used to printed the image acording to the random value
        for i in range(self.lin):
            for j in range(self.col):
                self.A[i][j] = rd.randint(1,7)
                symbol_image = pygame.image.load(symbols[self.A[i][j]])
                symbol_image = pygame.transform.scale(symbol_image, (150, 150))
                symbol_images.append(symbol_image)
    
        user_text = ''
        ok = TextInputSpin(user_text, symbol_images, self.money, self._Checker(gamble, symbol_images))
        if ok == 4: # No to R/B
            self.money = self.money + self._Checker(gamble, symbol_images) # Alg function
        elif ok == 5: # Yes to R/B
            self.money = self.money + self.RedBlack(self._Checker(gamble, symbol_images))
        os.system('clear')   

        if self.money < gamble:
            return False, int(ok)
        return True, int(ok)
    
    def _Checker(self, gamble, symbol_images) -> float:
        rate = 0

        if self._all_equal(self.A[1]) == True and self.lines >= 1: # Linia 1 
            rate += 1
            print("Linia 1")
        if self._all_equal(self.A[0]) == True and self.lines >= 2: # Linia 2
            rate += 1
            print("Linia 2")
        if self._all_equal(self.A[2]) == True and self.lines >= 3: # Linia 3
            rate += 1
            print("Linia 3")
        
        X = [ self.A[0][0], self.A[1][1], self.A[2][2], self.A[1][3], self.A[0][4] ]
        if self._all_equal(X) == True and self.lines >= 4: # Linia 4
            rate += 1
            print("Linia 4")

        X = [ self.A[2][0], self.A[1][1], self.A[0][2], self.A[1][3], self.A[2][4] ]
        if self._all_equal(X) == True and self.lines >= 5: # Linia 5
            rate += 1
            print("Linia 5")

        X = [ self.A[1][0], self.A[2][1], self.A[2][2], self.A[2][3], self.A[1][4] ]
        if self._all_equal(X) == True and self.lines >= 6: # Linia 6
            rate += 1
            print("Linia 6")

        X = [ self.A[1][0], self.A[0][1], self.A[0][2], self.A[0][3], self.A[1][4] ]
        if self._all_equal(X) == True and self.lines >= 7: # Linia 7
            rate += 1
            print("Linia 7")

        X = [ self.A[2][0], self.A[2][1], self.A[1][2], self.A[0][3], self.A[0][4] ]
        if self._all_equal(X) == True and self.lines >= 8: # Linia 8
            rate += 1
            print("Linia 8")

        X = [ self.A[0][0], self.A[0][1], self.A[1][2], self.A[2][3], self.A[2][4] ]
        if self._all_equal(X) == True and self.lines >= 9: # Linia 9
            rate += 1
            print("Linia 9")
        
        X = [ self.A[2][0], self.A[1][1], self.A[1][2], self.A[1][3], self.A[0][4] ]
        if self._all_equal(X) == True and self.lines >= 10: # Linia 10
            rate += 1
            print("Linia 10")

        #print(self.A)
        
        return rate * gamble # win
                   
    def _all_equal(self, arr) -> bool:
        count = 0
        for i in range(len(arr)-1):
            if arr[i] == arr[i+1]:
                count += 1
            else:
                count = 1 # count of a new number

            if count == 3:
                return True
        return False
    

def DrawTextBox(user_text, font, input_rect, w, h):
    pygame.draw.rect(win,(0,0,0),input_rect,2) # the last param is for outline
    text_surface = font.render(user_text, True, (255,255,255)) # reda textul user cu fontul selectat
    win.blit(text_surface,(win_width // 2 + w , win_height // 2 + h))

    input_rect.w = max(100, text_surface.get_width() + 10 )
    pygame.display.update()
    return user_text

def TextInput(user_text, font, input_rect, string):
    active = False
    running = True
    
    while running:
        try:
            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                if event.type == pygame.KEYDOWN:
                    if active == True:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[0:-1]
                        else:
                            user_text += event.unicode
                
                        if event.key == pygame.K_RETURN:
                            instance = float(user_text)
                            active = False
                            return instance # Exit from function

            text = font.render('Welcome to Power-Stars', True, (255, 0, 0), (255,255,255) )
            textRect = text.get_rect() # Rectangular for text
            textRect.center = (win_width // 2 , win_height // 2)

            win.blit(background_image, (0,0)) # Menu Start
            win.blit(text, textRect)

            text1 = font.render(string, True, (255, 0, 0), (255,255,255) )
            textRect1 = text1.get_rect() # Rectangular for text
            textRect1.center = (win_width // 2 + 300, win_height // 2 + 300)
            win.blit(text1, textRect1)

            user_text = DrawTextBox(user_text, font, input_rect, -50, 100)
        
        except:
            print("You pressed the wrong key!")
            running = True

def TextInputSpin(user_text, symbol_images, money, choice):
    k = 0
    active = False
    running = True
    while running:
        try:
            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect_select.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                if event.type == pygame.KEYDOWN:
                    if active == True:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[0:-1]
                        else:
                            user_text += event.unicode
                
                        if event.key == pygame.K_RETURN:
                            instance = user_text
                            if k == 1 : # For Red/Black
                                if instance[0].lower() == 'n':
                                    return 4
                                elif instance[0].lower() == 'y':
                                    return 5
                            active = False
                            instance = int(instance) #??
                            return instance # Exit from function
                        
                    if event.key == pygame.K_SPACE:
                        instance = 1
                        return instance


            win.blit(background_image, (0,0)) # Menu Start
            for i in range(len(symbol_positions)):
                win.blit(symbol_images[i], symbol_positions[i])
        

            text1 = font.render("Space-Spin 2-Change bet 3-Cash out", True, (255, 0, 0), (255,255,255) )
            textRect1 = text1.get_rect() # Rectangular for text
            textRect1.center = (win_width // 2 + 300, win_height // 2 + 300)
            win.blit(text1, textRect1)

            text = font.render(f'Balance: {money}', True, (255, 0, 0), (255,255,255) )
            textRect = text.get_rect() # Rectangular for text
            textRect.center = (win_width // 2 - 400 , win_height // 2 - 300)
            win.blit(text, textRect)

            if choice != 0: # If he win , we ask him if he want to double it
                text1 = font.render("Do you want to double your money Y/N ?", True, (255, 0, 0), (255,255,255) )
                textRect1 = text1.get_rect() # Rectangular for text
                textRect1.center = (win_width // 2 + 300, win_height // 2 + 300)
                win.blit(text1, textRect1)
                
                k = 1
                
            user_text = DrawTextBox(user_text, font, input_rect_select, -300, 280)
        except:
            running = True
            print("You pressed the wrong key!")

def TextInputRedBlack(user_text, font, input_rect, card_images ):
    active = False
    running = True
    while running:

        ## EVENTS ##
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[0:-1]
                    else:
                        user_text += event.unicode
            
                    if event.key == pygame.K_RETURN:
                        instance = user_text
                        if instance[0].lower() == 'r':
                            return 'r'
                        elif instance[0].lower() == 'b':
                            return 'b'
                        active = False
                        return instance # Exit from function

        text = font.render('Red or Black ?', True, (255, 0, 0), (255,255,255) )
        textRect = text.get_rect() # Rectangular for text
        textRect.center = (win_width // 2 , win_height // 2)

        win.blit(background_image, (0,0)) # Menu Start
        for i in range(len(card_positions)):
            win.blit(card_images[i], card_positions[i])
        
        win.blit(text, textRect)

        user_text = DrawTextBox(user_text, font, input_rect, -50, 100)
        


#######################--MAIN--########################

money = TextInput(user_text, font, input_rect, "How much money do you have? ")
user_text = ''
lines = int(TextInput(user_text, font, input_rect, "How many lines do you want? "))

if lines > 10: # In case you enter more than 10 lines
    lines = 10

G = Gamble(money, lines)

while True:
    user_text = ''
    gamble = TextInput(user_text, font, input_rect, f"Select bet (between {lines/100} and {lines*5} )")
    bankruptcy = True
    
    win.blit(background_image, (0,0)) # Menu slot
    pygame.display.flip()

    if gamble <= lines*5 and gamble >= lines/100:
            while bankruptcy == True:
                bankruptcy, ok = G.Spin(gamble)

                if ok == 1:
                    pygame.display.flip()
                    continue
                if ok == 2:
                    break
                if ok == 3:
                    print("Cash out")
                    exit(0)
                
               
    if( bankruptcy == False): # Daca avem faliment
        continue
    else:
        print("Select a corect bet! ")




