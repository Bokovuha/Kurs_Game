from os import path
import pygame as pg
import random as rnd

pg.init()

img_dir = path.join(path.dirname(__file__), 'img')
exp_dir = path.join(path.dirname(__file__), 'img/explosion')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1920
HEIGHT = 1080
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

score = 0

start = pg.image.load(path.join(img_dir, "Start.png"))
start_gray = pg.image.load(path.join(img_dir, "Start_2.png"))
start_new = pg.image.load(path.join(img_dir, "Start_new.png"))
start_new_gray = pg.image.load(path.join(img_dir, "Start_new_2.png"))
exit = pg.image.load(path.join(img_dir, "Exit.png"))
exit_gray = pg.image.load(path.join(img_dir, "Exit_2.png"))
background = pg.image.load(path.join(img_dir, "Fon.jpg"))
background_rect = background.get_rect()
player_img = pg.image.load(path.join(img_dir, "ship.png"))
bullet_img = pg.image.load(path.join(img_dir, "bullet.png"))
ammo_png = pg.image.load(path.join(img_dir, "ammo.png"))
heal_png = pg.image.load(path.join(img_dir, "heal.png"))
meteor_images = []
meteor = ["asteroid_100x100.png", "asteroid_100x100_2.png", "asteroid_100x100_3.png",
          "asteroid_150x150.png", "asteroid_150x150_2.png", "asteroid_150x150_3.png",
          "asteroid_200x200.png", "asteroid_200x200_2.png", "asteroid_200x200_3.png"]

for img in meteor:
    meteor_images.append(pg.image.load(path.join(img_dir, img)))
explosion_anim = {'lg': [], 'sm': []}

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(exp_dir, filename))
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (125, 125))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (75, 75))
    explosion_anim['sm'].append(img_sm)

shoot_sound = pg.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
expl_sound = pg.mixer.Sound(path.join(snd_dir, 'expl.wav'))
heal_sound = pg.mixer.Sound(path.join(snd_dir, 'heal.wav'))
ammo_sound = pg.mixer.Sound(path.join(snd_dir, 'ammo.wav'))
pg.mixer.music.load(path.join(snd_dir, 'Backmusic.wav'))
pg.mixer.music.set_volume(0.3)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
bullets = pg.sprite.Group()
ammo = pg.sprite.Group()
heal = pg.sprite.Group()


