#перша частина коду
import pygame as pg
import sys
import random
pg.init()

# Constants
WIDTH, HEIGHT = 500, 500
FPS = 40
BG_COLOR = (100, 100, 100)
GAME_TIME = 10
TARGET_SCORE = 5
DISPLAY_TIME = 2
CARD_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
# Initialize Pygame
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fast Clicker")
clock = pg.time.Clock()
# Class definition
class Area:
   def __init__(self, rect, color):
       self.rect = rect
       self.color = color
   def set_color(self, color):
       self.color = color
   def fill_color(self, surface):
       pg.draw.rect(surface, self.color, self.rect)
   def set_border_color(self, surface, border_color, border_width=2):
       pg.draw.rect(surface, border_color, self.rect, border_width)
class Label(Area):
   def __init__(self, rect, color, text, font_size=20, text_color=(255, 255, 255)):
       super().__init__(rect, color)
       self.text = text
       self.font = pg.font.SysFont("Arial", font_size)
       self.text_color = text_color
   def set_text(self, text):
       self.text = text
   def display_with_text(self, surface):
       self.fill_color(surface)
       self.set_border_color(surface, self.color)
       text_surface = self.font.render(self.text, True, self.text_color)
       text_rect = text_surface.get_rect(center=self.rect.center)
       surface.blit(text_surface, text_rect)
# Create cards
cards = []
card_width, card_height = 100, 150
margin = 20
for i in range(4):
   x = i * (card_width + margin) + margin
   y = HEIGHT // 2 - card_height // 2
   rect = pg.Rect(x, y, card_width, card_height)
   color = CARD_COLORS[i]
   label = Label(rect, color, "CLICK!")
   cards.append(label)
# Game loop
def game():
   global TARGET_SCORE
   score = 0
   start_time = pg.time.get_ticks()
   display_click_time = None
   while True:
       # Event handling
       for event in pg.event.get():
           if event.type == pg.QUIT:
               pg.quit()
               sys.exit()
           elif event.type == pg.MOUSEBUTTONDOWN:
               for card in cards:
                   if card.rect.collidepoint(event.pos):
                       if card.text == "CLICK!":
                           card.set_color((0, 255, 0))  # Green for correct click
                           score += 1
                       else:
                           card.set_color((255, 0, 0))  # Red for incorrect click
       # Update
       elapsed_time = (pg.time.get_ticks() - start_time) / 1000
       if elapsed_time >= GAME_TIME or score >= TARGET_SCORE:
           if score >= TARGET_SCORE:
               print("You win!")
           else:
               print("Game over!")
           pg.display.flip()
           pg.time.wait(2000)  # Display the result for 2 seconds
           return
       # Randomly display "CLICK!"
       if display_click_time is None or (pg.time.get_ticks() - display_click_time) > DISPLAY_TIME * 1000:
           for card in cards:
               card.set_text("")
           random_card = random.choice(cards)
           random_card.set_text("CLICK!")
           display_click_time = pg.time.get_ticks()
       # Draw
       screen.fill(BG_COLOR)
       for card in cards:
           card.display_with_text(screen)
       # Display score and timer
       draw_text(f"Time: {int(GAME_TIME - elapsed_time)}s", 20, (255, 255, 255), 60, 20)
       draw_text(f"Score: {score}/{TARGET_SCORE}", 20, (255, 255, 255), WIDTH - 100, 20)
       pg.display.flip()
       clock.tick(FPS)
def draw_text(text, size, color, x, y):
   font = pg.font.SysFont("Arial", size)
   text_surface = font.render(text, True, color)
   text_rect = text_surface.get_rect(center=(x, y))
   screen.blit(text_surface, text_rect)
if __name__ == "__main__":
   game()
   pg.quit()
   sys.exit()

