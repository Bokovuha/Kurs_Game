import time

from init import *
from Game_rules import *


class Player(pg.sprite.Sprite):
    def __init__(self):
        self.shield = 100
        self.ammo = 0
        pg.sprite.Sprite.__init__(self)
        self.position = None
        self.image = pg.Surface((50, 40))
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 88
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)            //Хитбокс корабля
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        pos = pg.mouse.get_pos()
        self.rect.midtop = pos
        self.rect.move_ip(0, 25)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom < 0:
            self.rect.bottom = 0
        if self.rect.top > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image_orig = rnd.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)            //Хитбокс астероида
        self.rect.x = rnd.randrange(WIDTH - self.rect.width)
        self.rect.y = rnd.randrange(-40, -0)
        self.speedy = rnd.randrange(aster_min_speed, aster_max_speed)
        self.speedx = rnd.randrange(-1, 1)
        self.rot = 0
        self.rot_speed = rnd.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = rnd.randrange(WIDTH - self.rect.width)
            self.rect.y = rnd.randrange(-100, -40)
            self.speedy = rnd.randrange(aster_min_speed, aster_max_speed)
        self.rotate()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 30:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 20))
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Ammo(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((75, 75))
        self.image = ammo_png
        self.image = pg.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = item_speed

    def update(self):
        self.rect.y += self.speedy


class Heal(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((100, 100))
        self.image = heal_png
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = item_speed

    def update(self):
        self.rect.y += self.speedy


player = Player()
all_sprites.add(player)

font_name = pg.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 30
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 5)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


for i in range(aster_count):
    newmob()


def ammospawn():
    x = rnd.randint(200, WIDTH - 200)
    y = rnd.randint(200, HEIGHT - 200)
    b = Ammo(x, y)
    all_sprites.add(b)
    ammo.add(b)


def ammo_draw():
    ammo_pic = pg.transform.scale(ammo_png, (50, 50))
    screen.blit(ammo_pic, (1840, 10))


def healspawn():
    x = rnd.randint(200, WIDTH - 200)
    y = rnd.randint(200, HEIGHT - 200)
    h = Heal(x, y)
    all_sprites.add(h)
    heal.add(h)


def button_start_draw():
    screen.blit(start, (750, 400))
    mouse = pg.mouse.get_pos()
    if 750 < mouse[0] < 1250 and 400 < mouse[1] < 600:
        screen.blit(start_gray, (750, 400))


def button_start_new_draw():
    screen.blit(start_new, (750, 600))
    mouse = pg.mouse.get_pos()
    if 750 < mouse[0] < 1250 and 600 < mouse[1] < 800:
        screen.blit(start_new_gray, (750, 600))


def button_exit_draw():
    screen.blit(exit, (750, 200))
    mouse = pg.mouse.get_pos()
    if 750 < mouse[0] < 1250 and 200 < mouse[1] < 400:
        screen.blit(exit_gray, (750, 200))


def new_game():
    player.ammo = 0
    player.shield = 100
    player.score = 0
    for mob in mobs:
        mob.kill()
    all_sprites.remove(mobs)
    newmob()
    for i in range(aster_count):
        newmob()

