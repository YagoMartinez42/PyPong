from pygame import *

#clase padre para los objetos
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (wight, height)) #por ejemplo. 55,55 - parámetros
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def update_img(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   def update_r(self):
       keys = key.get_pressed()
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
           self.rect.y += self.speed
   def update_l(self):
       keys = key.get_pressed()
       if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
           self.rect.y += self.speed

#escena del videojuego:
back = (200, 255, 255) #fondo
win_width = 1280
win_height = 720
window = display.set_mode((win_width, win_height))
window.fill(back)

#banderas responsables por el estado del juego
game = True
finish = False
clock = time.Clock()
FPS = 60

#creando pelota y paletas 
racket1 = Player('racket.png', 30, 200, 4, 50, 150) 
racket2 = Player('racket.png', 1200, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 575, 350, 4, 50, 50)

font.init()
font = font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

speed_x = 3
speed_y = 3
reboundTimerStart = time.get_ticks()

while game:
   reboundTimer = time.get_ticks()
   for e in event.get():
       if e.type == QUIT:
           game = False
  
   if not finish:
       window.fill(back)
       racket1.update_l()
       racket2.update_r()
       ball.rect.x += speed_x
       ball.rect.y += speed_y

       if (sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball)) and reboundTimer - reboundTimerStart > 500:
           speed_x *= -1
           reboundTimerStart = time.get_ticks()
      
       #si la pelota llega a los bordes de la pantalla, cambiar dirección de movimiento
       if ball.rect.y > win_height - ball.rect.width or ball.rect.y < 0:
           speed_y *= -1

       #si la pelota va más allá de esta paleta, mostrar la condición de derrota para el jugador 1
       if ball.rect.x < 0:
           finish = True
           window.blit(lose1, (200, 200))
           game_over = True

       #si la pelota va más allá de esta paleta, mostrar la condición de derrota para el jugador 2
       if ball.rect.x > win_width - ball.rect.width:
           finish = True
           window.blit(lose2, (200, 200))
           game_over = True

       racket1.update_img()
       racket2.update_img()
       ball.update_img()

   display.update()
   clock.tick(FPS)
