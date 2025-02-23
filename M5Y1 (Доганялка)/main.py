from pygame import *
init()
class gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=55, height=55):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self): window.blit(self.image, (self.rect.x, self.rect.y))
class player(gamesprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.last_direction = "up"

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.last_direction = "left"
        if keys[K_RIGHT] and self.rect.x < win_width - 60:
            self.rect.x += self.speed
            self.last_direction = "right"
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
            self.last_direction = "up"
        if keys[K_DOWN] and self.rect.y < win_height - 60:
            self.rect.y += self.speed
            self.last_direction = "down"

    def fire(self):
        if not finish:
            varbullet = bullet('bullet.png', self.rect.centerx, self.rect.centery, 8, self.last_direction)
            bullets.add(varbullet)
            gun_sound.play()
class enemy(gamesprite):
    side = 'left'
    def __init__(self, enemy_image, x, y, speed):
        super().__init__(enemy_image, x, y, speed, 65, 85)
        self.alive = True
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    def die(self):self.kill;self.alive=False
class bullet(gamesprite):
    def __init__(self, image, x, y, speed, direction):super().__init__(image,x,y,speed,15,15);self.direction=direction
    def update(self):
        if self.direction=='up':self.rect.y-=self.speed
        elif self.direction=='down':self.rect.y+=self.speed
        elif self.direction=='left':self.rect.x-=self.speed
        elif self.direction=='right':self.rect.x+=self.speed
        if self.rect.y<0 or self.rect.y>win_height or self.rect.x<0 or self.rect.x>win_width:self.kill()
class wall(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3,wall_x,wall_y,wall_width,wall_height):super().__init__();self.color_1=color_1;self.color_2=color_2;self.color_3=color_3;self.width=wall_width;self.height=wall_height;self.image=Surface([self.width,self.height]);self.image.fill((color_1, color_2, color_3));self.rect=self.image.get_rect();self.rect.x=wall_x;self.rect.y=wall_y
    def draw_wall(self):window.blit(self.image, (self.rect.x, self.rect.y))
# Функція для запуску гри
def start_game():
    global pacman, monster, final_point, walls, bullets, finish, start_time
    
    pacman = player('sprite1.png', 5, win_height - 80, 4)
    monster = enemy('monster.png', win_width - 80, 280, 2)
    final_point = gamesprite('final_point.png', win_width - 120, win_height - 80, 0)
    
    # Група стіни
    walls = sprite.Group(wall(154, 205, 50, 100, 0, 10, 380),wall(154, 205, 50, 200, 130, 10, 380),wall(154, 205, 50, 450, 130, 10, 380),wall(154, 205, 50, 300, 0, 10, 350),wall(154, 205, 50, 390, 120, 130, 10))
    # Група патрони
    bullets = sprite.Group()
    # Статус гри
    finish = False
    # Час для статистики
    start_time = time.get_ticks()
    
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")
background = transform.scale(image.load("background.png"), (700, 500))

sprite1 = transform.scale(image.load('sprite1.png'), (100, 100))
sprite2 = transform.scale(image.load('sprite2.png'), (100, 100))
#дані про спрайт-картинку
x1 = 100
y1 = 300
 
x2 = 300
y2 = 300
 
speed = 10

#ігровий цикл
run = True
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('dubstep.ogg')
mixer.music.play()

money_sound = mixer.Sound('final_point.mp3')
kick_sound = mixer.Sound('kick.ogg')
gun_sound = mixer.Sound('gun.mp3')
voice_sound = mixer.Sound('linganguli.ogg')

while run:
    window.blit(background,(0, 0))
    window.blit(sprite1, (x1, y1))
    window.blit(sprite2, (x2, y2))
 
    for e in event.get():
       if e.type == QUIT:
           run = False
 
    keys_pressed = key.get_pressed()
 
    if keys_pressed[K_LEFT] and x1 > 5:
       x1 -= speed
    if keys_pressed[K_RIGHT] and x1 < 595:
       x1 += speed
    if keys_pressed[K_UP] and y1 > 5:
       y1 -= speed
    if keys_pressed[K_DOWN] and y1 < 395:
       y1 += speed
    
    if keys_pressed[K_e]:
       FPS = int(input('enter fps:\n>>> '))
 
    if keys_pressed[K_a] and x2 > 5:
       x2 -= speed
    if keys_pressed[K_d] and x2 < 595:
       x2 += speed
    if keys_pressed[K_w] and y2 > 5:
       y2 -= speed
    if keys_pressed[K_s] and y2 < 395:
       y2 += speed
 
    display.update()
    clock.tick(FPS)





















































































































fpiBank = 700