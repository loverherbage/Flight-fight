import pygame
import sys
import traceback
import plane as player
import bullet
import enemy
from pygame.locals import *
from supply import *
from random import *
import threading

pygame.init()
pygame.mixer.init()
bg_size = width, height = 480, 750
screen = pygame.display.set_mode(bg_size)
source_img = pygame.image.load("image/source.png").convert_alpha()
boob_supply_img = source_img.subsurface(pygame.Rect(808, 694, 66, 50)).convert_alpha()
boob_supply_img_rect = boob_supply_img.get_rect()
boob_supply_img_rect.left, boob_supply_img_rect.top = 10, bg_size[1] - boob_supply_img_rect.height - 10

pygame.display.set_caption("飞机大战")
img_icon = pygame.image.load("image/plane.png").convert_alpha()
pygame.display.set_icon(img_icon)
background = pygame.image.load("image/bg.png").convert()
game_over_background = pygame.image.load("image/bg_game_over.png").convert_alpha()

pause_img = pygame.image.load("image/pause.png").convert_alpha()
start_img = pygame.image.load("image/start.png").convert_alpha()
fin_paused_img = pause_img
paused_rect = fin_paused_img.get_rect()
paused_rect.left, paused_rect.top = bg_size[0] - paused_rect.width - 10, 10

bul_frequency, min_frequency, mid_frequency, big_frequency = 10, 100, 500, 1500
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
supplies = pygame.sprite.Group()
img_index = 0
i = 1
score = 0
score_font = num_font = pygame.font.Font(None, 36)
is_pause = is_double = game_over = False
boob_num = 2
# 设定一个供给事件计时器
SUPPLY_TIME = USEREVENT
# 设定一个双倍子弹持续计时器
DOUBLE_BULLET_TIME = USEREVENT + 1
# 设定一个无敌时间计时器
INVINCIBLE_TIME = USEREVENT + 2
BOOBBREAK_TIME = USEREVENT + 3
explosion_thread = []
def drawExplosion(each_enemy):
    global score
    for img in each_enemy.explosion_images:
        screen.blit(img, each_enemy.rect)
        pygame.display.update(each_enemy.rect)
        pygame.time.delay(10)
    score += each_enemy.max_blood * 10
    enemies.remove(each_enemy)


def drawGameOver():
    global width, height
    game_font = pygame.font.Font()
    restart = pygame.image.load("image/restart.png").convert_alpha()
    over = pygame.image.load("image/over.png").convert_alpha()
    restart_img = pygame.transform.scale(restart, (250, 50))
    over_img = pygame.transform.scale(over, (250, 50))
    restart_rect = restart_img.get_rect()
    restart_rect.left, restart_rect.top = (width - restart_rect.width) // 2, 0.6 * height
    over_rect = over_img.get_rect()
    over_rect.left, over_rect.top = (width - over_rect.width) // 2, 0.7 * height

    screen.blit(restart_img, restart_rect)
    screen.blit(over_img, over_rect)
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if restart_rect.left < pos[0] < restart_rect.right and restart_rect.top < pos[1] < restart_rect.bottom:
            main()


def genEnemies(plane, index):
    if index % bul_frequency == 0:
        if is_double:
            blt = bullet.DoubleBullet((plane.rect.centerx - 33, plane.rect.centery))
            blt2 = bullet.DoubleBullet((plane.rect.centerx + 33, plane.rect.centery))
            bullets.add(blt)
            bullets.add(blt2)
        else:
            blt = bullet.Bullet((plane.rect.left, plane.rect.midtop))
            bullets.add(blt)
    if index % min_frequency == 0:
        min_e = enemy.minEnemy(bg_size)
        enemies.add(min_e)
    if index % mid_frequency == 0:
        mid_e = enemy.midEnemy(bg_size)
        enemies.add(mid_e)
    if index % big_frequency == 0:
        big_e = enemy.BigEnemy(bg_size)
        enemies.add(big_e)


def drawEnemies(index):
    global score,explosion_thread
    for each_enemy in enemies:
        if not each_enemy.is_over:
            # 若是没有被击败
            each_enemy.move()
            if each_enemy.rect.top > int(bg_size[1]):
                enemies.remove(each_enemy)
            screen.blit(each_enemy.normal_images, each_enemy.rect)
        else:
            t = threading.Thread(target=drawExplosion, args=(each_enemy,), daemon=False)
            t.start()
            explosion_thread.append(t)
        drawBloodLine(each_enemy)


def drawBullets():
    for b in bullets:
        b.move()
        screen.blit(b.image, b.rect)
        if b.rect.bottom < 0:
            bullets.remove(b)


def drawScore():
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 5))


def drawPlane(plane, index):
    global game_over
    if not plane.is_hit:
        if index % 5 == 0:
            plane.image_index = (plane.image_index + 1) % 2
    else:
        if index % 5 == 0:
            plane.image_index = (plane.image_index + 1) % 6
            if plane.image_index == 0:
                if plane.blood > 0:
                    plane.blood -= 1
                    plane.is_hit = False
                    pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)
    if plane.blood <= 0:
        game_over = True

    screen.blit(plane.image[plane.image_index], plane.rect)


def drawControlBar():
    if not is_pause:
        screen.blit(pause_img, paused_rect)
    else:
        screen.blit(start_img, paused_rect)


def drawSupplyBar():
    screen.blit(boob_supply_img, boob_supply_img_rect)
    num_text = num_font.render(f'X {boob_num}', True, (255, 255, 255))
    screen.blit(num_text, (boob_supply_img_rect.right + 10, boob_supply_img_rect.top + 10))


def drawExtraChance(plane):
    global img_icon
    img = pygame.transform.scale(img_icon, (40, 40))
    left_x = plane.width - 10
    top_y = plane.height - 50
    x = left_x
    for p in range(1, plane.blood):
        x = x - 40
        screen.blit(img, (x, top_y))


def genSupply(index):
    if index % 3600 == 0:
        choice = randint(0, 1)
        if choice == 0:
            sup = BulletSupply(bg_size)
        else:
            sup = BoobSupply(bg_size)
        supplies.add(sup)


def drawSupply():
    for sup in supplies:
        sup.move()
        screen.blit(sup.image, sup.rect)


def saveBoob():
    global boob_num
    if boob_num < 3:
        boob_num += 1


def doubleBullet():
    global is_double
    is_double = True
    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)


def destroyAll():
    for e in enemies:
        e.is_over = True


def drawBloodLine(sprite_enemy):
    pygame.draw.line(screen, (0, 0, 0), (sprite_enemy.rect.left, sprite_enemy.rect.top - 5),
                     (sprite_enemy.rect.right, sprite_enemy.rect.top - 5), 2)
    blood_remain = sprite_enemy.blood / sprite_enemy.max_blood
    if blood_remain >= 0.2:
        blood_color = (0, 255, 0)
    else:
        blood_color = (255, 0, 0)
    pygame.draw.line(screen, blood_color, (sprite_enemy.rect.left, sprite_enemy.rect.top - 5),
                     (sprite_enemy.rect.left + blood_remain * sprite_enemy.rect.width, sprite_enemy.rect.top - 5), 2)


def main():
    global i, is_pause, fin_paused_img, paused_rect, paused_rect, is_double, boob_num, explosion_thread
    can_boob = True
    # pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    plane = player.Plane(bg_size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    is_pause = not is_pause
                if not is_pause:
                    fin_paused_img = pause_img
                else:
                    fin_paused_img = start_img
            elif event.type == DOUBLE_BULLET_TIME:
                is_double = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            elif event.type == INVINCIBLE_TIME:
                plane.is_invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
            elif event.type == BOOBBREAK_TIME:
                can_boob = True
                pygame.time.set_timer(BOOBBREAK_TIME, 0)

        screen.blit(background, (0, 0))
        if not game_over:
            if not is_pause:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_w] or key_pressed[K_UP]:
                    plane.moveUp()
                if key_pressed[K_s] or key_pressed[K_DOWN]:
                    plane.moveDown()
                if key_pressed[K_a] or key_pressed[K_LEFT]:
                    plane.moveLeft()
                if key_pressed[K_d] or key_pressed[K_RIGHT]:
                    plane.moveRight()
                if key_pressed[K_SPACE]:
                    if boob_num > 0 and can_boob:
                        boob_num -= 1
                        destroyAll()
                        pygame.time.set_timer(BOOBBREAK_TIME, 3 * 1000)
                        can_boob = False
                # 判断我方飞机是否被敌机碰触，如果有，返回被碰触的所有敌机列表
                enemies_down = pygame.sprite.spritecollide(plane, enemies, False, pygame.sprite.collide_mask)
                if enemies_down and not plane.is_invincible:
                    plane.is_hit = True
                    for e in enemies_down:
                        e.is_hit = True
                # 判断敌机是否被子弹击中，如果击中，删除子弹，返回被击中敌机精灵列表
                enemies_hitting = pygame.sprite.groupcollide(enemies, bullets, False, True, pygame.sprite.collide_mask)
                if enemies_hitting:
                    # 敌机若是被击中，首先将其生命值-1
                    for en in enemies_hitting:
                        en.blood -= 1
                        # 若是生命值小于等于0,将其is_hit设为True.绘制爆炸造型并删除此角色
                        if en.blood <= 0:
                            en.is_over = True
                # 判断补给是否被我方飞机获取
                supplies_down = pygame.sprite.spritecollide(plane, supplies, True, pygame.sprite.collide_mask)
                for sup in supplies_down:
                    if sup.name == "boob":
                        saveBoob()
                    else:
                        doubleBullet()
                    sup.is_hit = True
                    enemies.remove(sup)

                # 生成子弹、敌机
                genEnemies(plane, i)
                genSupply(i)
                # 在屏幕上绘制子弹
                drawBullets()
                drawSupply()
                # 在屏幕上绘制敌机
                drawEnemies(i)
                # 在屏幕上绘制我方战舰
                drawPlane(plane, i)
                drawScore()
                drawControlBar()
                drawSupplyBar()
                drawExtraChance(plane)
            screen.blit(fin_paused_img, paused_rect)
            pygame.display.flip()
            i += 1
            if i % 1800 == 0:
                i = 0
            clock.tick(60)
        else:
            screen.blit(game_over_background, (0, 0))
            drawGameOver()
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    try:
        main()
        for thread in explosion_thread:
            thread.join()
        print("jh")
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
