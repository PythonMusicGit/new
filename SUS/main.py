from pygame import *
from random import randint

# Клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=55, height=55):
        super().__init__()
        
        self.image = transform.scale(image.load(player_image), (width, height))
        
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Гравець
class Player(GameSprite):
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
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.centery, 8, self.last_direction)
            bullets.add(bullet)
            gun_sound.play()

# Ворог
class Enemy(GameSprite):
    side = "left"
    
    def __init__(self, enemy_image, x, y, speed):
        super().__init__(enemy_image, x, y, speed, 65, 65)
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
            
    """Вбивство монстра."""
    def die(self):
        self.kill()
        self.alive = False
    
    
class Bullet(GameSprite):
    def __init__(self, image, x, y, speed, direction):
        super().__init__(image, x, y, speed, 240, 240)
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Якщо пуля вилетіла за видиме вікно - видаляємо її
        if self.rect.y < 0 or self.rect.y > win_height or self.rect.x < 0 or self.rect.x > win_width:
            self.kill()

# Стіна
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        self.image = Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Функція для запуску гри
def start_game():
    global pacman, monster, final_point, walls, bullets, finish, start_time
    heehee = bool(randint(0,1))
    if heehee:
        pacman = Player('sprite1.png', 5, win_height - 80, 4)
    else:
        pacman = Player('sprite2.png', 5, win_height - 80, 4)
    monster = Enemy('monster.png', win_width - 80, 280, 2)
    final_point = GameSprite('final_point.png', win_width - 120, win_height - 80, 0)
    
    # Група стіни
    walls = sprite.Group(
        Wall(154, 205, 50, 100, 0, 10, 380),
        Wall(154, 205, 50, 200, 130, 10, 380),
        Wall(154, 205, 50, 450, 130, 10, 380),
        Wall(154, 205, 50, 300, 0, 10, 350),
        Wall(154, 205, 50, 390, 120, 130, 10)
    )
    # Група патрони
    bullets = sprite.Group()
    # Статус гри
    finish = False
    # Час для статистики
    start_time = time.get_ticks()
    
    
# Створення вікна
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")

# Завантаження фонів
# фон гри
background = transform.scale(image.load("background.png"), (win_width, win_height))
# фон при перемозі
win_bg = transform.scale(image.load("background.png"), (win_width, win_height))
# фон при поразці
lose_bg = transform.scale(image.load("background.png"), (win_width, win_height))

# Чи гра ввімкнута?
game = True
# Статуси гри
finish = False

# Годинник та ФПС
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 50)

# Фонова музика гри
mixer.init()
mixer.music.load('dubstep.ogg')
mixer.music.play()

money_sound = mixer.Sound('final_point.mp3')
kick_sound = mixer.Sound('kick.ogg')
gun_sound = mixer.Sound('gun.mp3')
voice_sound = mixer.Sound('linganguli.ogg')

# Запускаємо гру
start_game()


while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                pacman.fire()
            if e.key == K_RETURN and finish:
                start_game()
            if e.key == K_e:
                voice_sound.play()
    if not finish:
        window.blit(background, (0,0))
        pacman.update()
        bullets.update()
        pacman.reset()
        final_point.reset()
        bullets.draw(window)
        if monster.alive:
            monster.update()
            monster.reset()
        for wall in walls:
            wall.draw_wall()
        for bullet in bullets:
            if monster.alive and sprite.collide_rect(bullet, monster):
                monster.die()
                bullet.kill()
        game_time = (time.get_ticks() - start_time) // 1000
    timer_text = font.render(f"Час: {game_time}", True, (255, 255, 255))
    window.blit(timer_text, (10, 10))  # Лівbй верхній кут з відступами 10, 10
    if game_time >= 60:
        finish = True
        window.blit(lose_bg, (0,0))
        text1 = font.render("Chaz Vyishov!", True, (255,0,0))
        text2 = font.render("Natysnit Enter", True, (255,0,0))
        window.blit(text1,(250,200))
        window.blit(text2,(250,250))
        kick_sound.play()
    # Поразка (пакмен торкнувся монстра або стіни)
    if (sprite.collide_rect(pacman, monster) and monster.alive) or sprite.spritecollide(pacman, walls, False):
        finish = True
        window.blit(lose_bg, (0, 0))

        text1 = font.render("Ви програли!", True, (255, 0, 0))
        text2 = font.render("Натисніть Enter", True, (255, 0, 0))
        window.blit(text1, (250, 200))
        window.blit(text2, (250, 250))
        kick_sound.play()


    
    display.update()
    clock.tick(FPS)