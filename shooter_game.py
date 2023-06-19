#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

win_width = 1200
win_height = 600
FPS = 60
game = True
mixer.init()
mixer.music.load('Space-Jazz.ogg')
mixer.music.play()
bk = transform.scale(image.load('galaxy.jpg'), (win_width, win_height ))
count_enemy = 0
kill_enemy = 0
num_fire = 0
rel_time = False
health = 3

window = display.set_mode((win_width, win_height))
clock = time.Clock()
finish = False
class Gamesprite(sprite.Sprite):
    """
    Базовый класс игрового спрайта.

    Args:
        player (pygame.Surface): Изображение спрайта.
        width (int): Ширина спрайта.
        height (int): Высота спрайта.
        speed (int): Скорость спрайта.
        x (int): Начальная позиция по оси X.
        y (int): Начальная позиция по оси Y.
    """
    def __init__(self, player, width, height, speed, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(player), (self.width, self.height ))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

    def reset(self):
        """
        Отображает спрайт на текущей позиции на экране.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    """
    Класс игрока.

    Args:
        player (pygame.Surface): Изображение игрока.
        width (int): Ширина игрока.
        height (int): Высота игрока.
        speed (int): Скорость игрока.
        x (int): Начальная позиция по оси X.
        y (int): Начальная позиция по оси Y.
    """
    def update(self):
        """
        Обновляет положение игрока на основе нажатых клавиш.
        """
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < win_height - self.height:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - self.width:
            self.rect.x += self.speed
    
    def fire(self):
        """
        Выпускает пулю из игрока.
        """
        bullet = Bullet('bullet.png', 10, 45, 25, self.rect.centerx - 5, self.rect.top - 10)
        bullets.add(bullet)
        kick = mixer.Sound('fire.ogg')
        kick.play()
        
class Enemy(Gamesprite):
    """
    Класс врага.

    Args:
        player (pygame.Surface): Изображение игрока.
        width (int): Ширина игрока.
        height (int): Высота игрока.
        speed (int): Скорость игрока.
        x (int): Начальная позиция по оси X.
        y (int): Начальная позиция по оси Y.
    """
    def update(self):
        """
        Обновляет положение врага.
        """
        global count_enemy
        self.rect.y += self.speed
        if self.rect.y > win_height:
            count_enemy += 1
            self.rect.y = 0 - self.height
            self.rect.x = randint(0, win_width - self.width)  

class Bullet(Gamesprite):
    """
    Класс пули.

    Args:
        player (pygame.Surface): Изображение пули.
        width (int): Ширина пули.
        height (int): Высота пули.
        speed (int): Скорость пули.
        x (int): Начальная позиция по оси X.
        y (int): Начальная позиция по оси Y.
    """
    def update(self):
        """
        Обновляет положение пули.
        """
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

font.init()
small_font = font.SysFont('Arial', 30)


hero = Player('rocket.png', 90, 120, 20, win_width // 2 - 90, win_height - 120)

enemies = sprite.Group()

asteroids = sprite.Group()

main_font = font.SysFont('Arial', 100)
win_game = main_font.render('YOU WIN', True, (0, 255, 0))
lose_game = main_font.render('YOU LOSE', True, (255, 0, 0))
reload = small_font.render('Wait, reload', True, (255, 0, 100))
win_image_width, win_image_height = win_game.get_size()
lose_image_width, lose_image_height = lose_game.get_size()
reload_image_width, reload_image_height = reload.get_size()
x_reload = (win_width - reload_image_width) // 2
y_reload = (win_height - reload_image_height) // 2
x_win = (win_width - win_image_width) // 2
y_win = (win_height - win_image_height) // 2
x_lose = (win_width - lose_image_width) // 2
y_lose = (win_height - lose_image_height) // 2

for enemy in range(5):
    enemy = Enemy('ufo.png', randint(80, 120), randint(50, 90), randint(1, 3), randint(0, win_width - 120), -90)
    enemies.add(enemy)
    """
    Основной игровой цикл.
    """
for asteroid in range(3):
    asteroid = Enemy('asteroid.png', randint(50, 100), randint(30, 70), randint(1, 2), randint(0, win_width - 120), -90)
    asteroids.add(asteroid)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    hero.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
    if finish != True:
        window.blit(bk, (0, 0))
        hero.update()
        hero.reset()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time >= 2:
                num_fire = 0
                rel_time = False
            else:
                window.blit(reload, (x_reload, y_reload))
        for item in sprites_list:
            kill_enemy += 1
            enemy = Enemy('ufo.png', randint(80, 120), randint(50, 90), randint(1, 3), randint(0, win_width - 120), -90)
            enemies.add(enemy)
        if kill_enemy >= 10:
            finish = True
            window.blit(win_game, (x_win, y_win))
        if count_enemy >= 5 :
            finish = True
            window.blit(lose_game, (x_lose, y_lose))
        if sprite.spritecollide(hero, enemies, True) or sprite.spritecollide(hero, asteroids, True):
            health -= 1
        if health <= 0:
            finish = True
            window.blit(lose_game, (x_lose, y_lose))
            
        lost = small_font.render('Пропущено врагов: ' + str(count_enemy), True, (255, 255, 255))
        window.blit(lost, (20, 50))
        kill = small_font.render('Сбито врагов: ' + str(kill_enemy), True, (255, 255, 255))
        window.blit(kill, (20, 20))
        hp = small_font.render('Осталось жизней: ' + str(health), True, (255, 255, 255))
        window.blit(hp, (920, 20))
        display.update()
        clock.tick(FPS)
    else:
        finish = False
        count_enemy = 0
        kill_enemy = 0
        num_fire = 0
        rel_time = False
        health = 3
        for e in enemies:
            e.kill()
            
        for a in asteroids:
            a.kill()

        for b in bullets:
            b.kill()

        for enemy in range(5):
            enemy = Enemy('ufo.png', randint(80, 120), randint(50, 90), randint(1, 3), randint(0, win_width - 120), -90)
            enemies.add(enemy)
            
        for asteroid in range(3):
            asteroid = Enemy('asteroid.png', randint(50, 100), randint(30, 70), randint(1, 2), randint(0, win_width - 120), -90)
            asteroids.add(asteroid) 