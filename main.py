import sys
import pandas as pd
from init import *
from Classes import *
from Game_rules import *
import pygame as pg


is_working = True
running = False
menu = True
endgame = False
leader = False

while is_working:

    while menu:
        screen = pg.display.set_mode((1920, 1080))
        screen.blit(background, background_rect)
        button_start_draw()
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if 750 < mouse[0] < 1250 and 400 < mouse[1] < 600:
                    menu = False
                    running = True
        pg.display.flip()
        pg.display.update()

    if running:
        pg.mixer.music.play(loops=-1)

    while running:
        pg.mouse.set_visible(False)
        clock.tick(FPS)
        now = pg.time.get_ticks()
        if now % 2 == 0 or now % 5 == 0:
            score = score + 1
        if now % ammo_chance == 0:
            ammospawn()
        if now % heal_chance  == 0:
            healspawn()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.ammo > 0:
                        player.ammo = player.ammo - 1
                        player.shoot()

        all_sprites.update()

        hits = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_circle)
        for hit in hits:
            player.shield -= damage
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            expl_sound.play()
            newmob()
            if player.shield <= 0:
                score = 0
                pg.mixer.music.stop()
                running = False
                endgame = True
        hits = pg.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            expl_sound.play()
            newmob()

        hits = pg.sprite.spritecollide(player, ammo, True)
        for hit in hits:
            player.ammo += 1
            ammo_sound.play()

        hits = pg.sprite.spritecollide(player, heal, True)
        for hit in hits:
            if player.shield < 100:
                player.shield += damage
            heal_sound.play()

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 30, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_text(screen, str(player.ammo), 30, 1800, 15)
        ammo_draw()
        pg.display.flip()

    while endgame:
        pg.mouse.set_visible(True)
        screen = pg.display.set_mode((1920, 1080))
        screen.blit(background, background_rect)
        draw_text(screen, "Вы проиграли", 100, WIDTH / 2, 10)
        button_start_new_draw()
        button_exit_draw()
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if 750 < mouse[0] < 1250 and 200 < mouse[1] < 400:
                    is_working = False
                    sys.exit()
                if 750 < mouse[0] < 1250 and 600 < mouse[1] < 800:
                    endgame = False
                    new_game()
                    running = True
        pg.display.flip()
        pg.display.update()

