#---------------------
#-----OOP Summative---
#-------June 02, 2022-
#-----Mason Skinner---
#---------------------
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
#-----Constants---
WIDTH = 480
HEIGHT = 600
FPS = 60
#-----Colors-----
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50,38))
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.dmg = 10
        self.last_shot = 0
        self.lives = 3
        self.hide_timer = pygame.time.get_ticks()
        self.power = 0
        self.shields = 0
        self.lasers = 0
        self.power_time = 0
        self.shield_time = 0
        self.laser_time = 0
        self.POWERTIME = 10000
        self.SHIELDTIME = 8000
        self.LASERTIME = 5000
        self.dead = False
        self.respawn = False
        self.old = 0
        self.i = 0
        
    def update(self):
        self.speedx = 0
        if self.dead == False:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
            self.rect.x += self.speedx
            if keystate[pygame.K_SPACE]:
                if self.lasers  >= 1:
                    player_laser.update()
                    all_sprites.add(player_laser)
                    self.laser = True
                else:
                    self.shoot()
                    self.laser = False
            else:
                all_sprites.remove(player_laser)
                self.laser = False
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0 
        if self.dead and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.dead = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            start = pygame.time.get_ticks()
            self.old = 0
            self.i = 0
            self.respawn = True
        if self.respawn == True:
            now = pygame.time.get_ticks()
            if now - self.old >= 200:
                player_group.remove(self)
                self.old = now
                self.i += 1
            elif now - self.old  >= 100:
                player_group.add(self)
            if self.i == 10:
                player_group.add(self)
                self.respawn = False
        if self.power >= 1 and pygame.time.get_ticks() - self.power_time > self.POWERTIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            if self.power == 0:
                self.power_time = 0
        if self.shields >= 1 and pygame.time.get_ticks() - self.shield_time > self.SHIELDTIME:
            self.shields -= 1
            self.shield_time = pygame.time.get_ticks()
            if self.shields == 0:
                all_sprites.remove(player_shield)
                self.shield_time = 0
        if self.lasers >= 1 and pygame.time.get_ticks() - self.laser_time > self.LASERTIME:
            self.lasers = self.lasers - 1
            self.laser_time = pygame.time.get_ticks()
            if self.lasers == 0:
                all_sprites.remove(player_laser)

    def kill_self(self):
        self.dead = True
        all_sprites.remove(player_laser)
        all_sprites.remove(player.shield)
        self.lasers = 0
        self.laser = False
        self.shields = 0
        if self.power >= 1:
            self.power -= 1
        player_group.remove(self)
        self.hide_timer = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 0:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 1:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def powerup(self):
        self.power += 1
        if self.power_time == 0:
            self.power_time = pygame.time.get_ticks()
    def invulnerable(self):
        self.shields += 1
        if self.shield_time == 0:
            all_sprites.add(player_shield)
            self.shield_time = pygame.time.get_ticks()
    def laser_gun(self):
        if self.lasers == 0:
            self.laser_time = pygame.time.get_ticks()
        self.lasers = self.lasers + 1
            
class Laser(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height * 0.90 / 2)
        self.rect.centerx = self.owner.rect.centerx
        self.rect.y = self.owner.rect.y - 20
    def update(self):
        self.rect.centerx = self.owner.rect.centerx
        self.rect.bottom = self.owner.rect.y 
            
class Forcefield(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.image = forcefield
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height * 0.90 / 2)
        self.rect.centerx = self.owner.rect.centerx
        self.rect.y = self.owner.rect.y + 20
    def update(self):
        self.rect.centerx = self.owner.rect.centerx
        self.rect.bottom = self.owner.rect.y 
        
class Meteor(pygame.sprite.Sprite): #all meteors
    def __init__(self, image_list, kind, center, rock):
        super().__init__()
        self.image_orig = random.choice(image_list)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.90 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.health = self.rect.width / 2
        self.last_update = pygame.time.get_ticks()
        self.kind = kind
        self.rock = rock
        if rock == True:
            self.health *= 2
        if kind == 'normal':
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
        elif kind == 'mini':
            self.rect.center = center
            
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -125 or self.rect.right > WIDTH + 125:
            if self.kind == 'normal':
                self.kill()
                new_meteor('lrg', 'normal', [0, 0])
            elif self.kind == 'mini':
                self.kill()
                
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            
class Pow(pygame.sprite.Sprite):
    def __init__(self, image, speed, center):
        super().__init__()
        self.type = image
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
            
class Super_Pow(Pow):
    def __init__(self, speed, center):
        image = random.choice(super_powerup_images)
        super().__init__(image, speed, center)
        

class Basic_Pow(Pow):
    def __init__(self, speed, center):
        image = random.choice(basic_powerup_images)
        super().__init__(image, speed, center)
            
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = 0
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
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
               
        
def convert_list(images_name, list_name):
    for img in images_name:
        list_name.append(pygame.image.load(path.join(img_dir, img)).convert())
        
def convert_dict(images, scale):
    i = 0
    for img in images:
        powerup_images[img] = pygame.image.load(path.join(img_dir, img + '.png')).convert()
        powerup_images[img] = pygame.transform.scale(powerup_images[img], (scale[i]))
        i += 1

def new_meteor(image_list, kind, center):
    i = random.random()
    if i >= 0.9:
        rock = True
        if image_list == 'lrg':
            image_list = meteors_rock_lrg
        elif image_list == 'med':
            image_list = meteors_rock_med
        else:
            image_list = meteors_rock_sml
    else:
        rock = False
        if image_list == 'lrg':
            image_list = meteors_dirt_lrg
        elif image_list == 'med':
            image_list = meteors_dirt_med
        else:
            image_list = meteors_dirt_sml
    m = Meteor(image_list, kind, center, rock)
    all_sprites.add(m)
    mobs.add(m)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        if i % 3 == 0:
            new_x = x
        elif i % 3 == 1:
            new_x = x + 30
        elif i % 3 == 2:
            new_x = x + 60
        if i % 3 == 0:
            y = y + 30
        img_rect.x = new_x
        img_rect.y = y
        surf.blit(img, img_rect)
    
def draw_shield_bar(surf, x, y, pot):
    if pot < 0:
        pot = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 10
    fill = (pot / 200) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
forcefield = pygame.image.load(path.join(img_dir, 'forcefield.png')).convert()
font_name = pygame.font.match_font('arial')
background = pygame.image.load(path.join(img_dir, 'back.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'player.png')).convert()
player_img.set_colorkey(BLACK)
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'bullet.png')).convert()
laser_img = pygame.transform.scale(bullet_img, (20, 400))

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = f'sonicExplosion0{i}.png'
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
    
meteors_rock_lrg = []
meteors_rock_med = []
meteors_rock_sml = []
meteors_dirt_lrg = []
meteors_dirt_med = []
meteors_dirt_sml = []
meteors_rock_lrg_images = ['meteor_rock0.png', 'meteor_rock1.png', 'meteor_rock2.png', 'meteor_rock3.png',\
                           'meteor_rock4.png', 'meteor_rock5.png',\
                           'meteor_rock6.png', 'meteor_rock7.png', 'meteor_rock8.png', 'meteor_rock9.png']
meteors_dirt_lrg_images = ['meteor_dirt0.png', 'meteor_dirt1.png', 'meteor_dirt2.png', 'meteor_dirt3.png',\
                           'meteor_dirt4.png', 'meteor_dirt5.png',\
                           'meteor_dirt6.png', 'meteor_dirt7.png', 'meteor_dirt8.png', 'meteor_dirt9.png']
meteors_rock_med_images = ['meteor_rock4.png', 'meteor_rock5.png']
meteors_dirt_med_images = ['meteor_dirt4.png', 'meteor_dirt5.png']
meteors_rock_sml_images = ['meteor_rock0.png', 'meteor_rock1.png', 'meteor_rock2.png', 'meteor_rock3.png']
meteors_dirt_sml_images = ['meteor_dirt0.png', 'meteor_dirt1.png', 'meteor_dirt2.png', 'meteor_dirt3.png']
convert_list(meteors_dirt_lrg_images, meteors_dirt_lrg)
convert_list(meteors_dirt_med_images, meteors_dirt_med)
convert_list(meteors_dirt_sml_images, meteors_dirt_sml)
convert_list(meteors_rock_lrg_images, meteors_rock_lrg)
convert_list(meteors_rock_med_images, meteors_rock_med)
convert_list(meteors_rock_sml_images, meteors_rock_sml)


powerup_images = {}
super_powerup_images = ['pow_invulnerable', 'pow_laser', 'pow_extralife']
super_powerup_scales = [[27,27], [35,20], [25,20]]
basic_powerup_images = ['pow_shield', 'pow_power', 'pow_gun']
basic_powerup_scales = [[20,20], [18,25], [25,25]]
        
convert_dict(basic_powerup_images, basic_powerup_scales)
convert_dict(super_powerup_images, super_powerup_scales)

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
offensive_power_sound = pygame.mixer.Sound(path.join(snd_dir, 'shield_sound.wav'))
defensive_power_sound = pygame.mixer.Sound(path.join(snd_dir, 'power_sound.wav'))
expl_sounds = []
for snd in ['explosion1.wav', 'explosion2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
    
POWERUP_TIME = 5000
pygame.mixer.music.play(loops=-1)
# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        player = Player()
        player_group.add(player)
        player_shield = Forcefield(player)
        player_laser = Laser(player)
        for i in range(8):
            new_meteor('lrg', 'normal', [0,0])
        score = 0
    clock.tick(FPS)
    #Input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Update
    all_sprites.update()
    player.update()
    if not player.respawn and not player.dead:
        if player.shields >= 1:
            hits = pygame.sprite.spritecollide(player_shield, mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                if hit.kind == 'normal':
                    new_meteor('lrg', 'normal', [0,0])
        else:
            hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.shield -= hit.health
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                if hit.kind == 'normal':
                    new_meteor('lrg', 'normal', [0,0])
                if player.shield <= 0:
                    death_explosion = Explosion(player.rect.center, 'player')
                    all_sprites.add(death_explosion)
                    if player.lives > 0:
                        player.kill_self()
                        player.lives -= 1
                        player.shield = 100
                    else:
                        player.kill()
                if player.lives == 0 and not death_explosion.alive():
                    game_over = True
    if not player.laser:
        hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
        dmg = player.dmg
    elif player.laser:
        hits = pygame.sprite.spritecollide(player_laser, mobs, False, False)
        dmg = player.dmg * 0.1
    for hit in hits:
        if hit.health >= dmg:
            score += int(dmg)
        else:
            score += int(hit.health)
        hit.health -= dmg
        if hit.health <= 0:
            score += int(150 - hit.rect.width)
            hit.kill()
            random.choice(expl_sounds).play()
            exp1 = Explosion(hit.rect.center, 'lg')
            all_sprites.add(exp1)
            if hit.rect.width >= 88:
                for i in range(2):
                    new_meteor('med', 'mini', hit.rect.center)
            elif hit.rect.width >= 40:
                for i in range(2):
                    new_meteor('sml', 'mini', hit.rect.center)
            if hit.kind == 'normal':
                new_meteor('lrg', 'normal', [0, 0])
            if random.random() > 0.80:
                if random.random() > 0.85:
                    pow = Super_Pow(2, hit.rect.center)
                else:
                    pow = Basic_Pow(2, hit.rect.center)
                    #pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
                
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'pow_shield':
            defensive_power_sound.play()
            player.shield += random.randrange(10, 30)
            if player.shield >= 200:
                player.shield = 200
        elif hit.type == 'pow_power':
            offensive_power_sound.play()
            player.dmg += 1
        elif hit.type == 'pow_gun':
            player.powerup()
            offensive_power_sound.play()
        elif hit.type == 'pow_extralife':
            player.lives += 1
            defensive_power_sound.play()
        elif hit.type == 'pow_invulnerable':
            player.invulnerable()
            defensive_power_sound.play()
        elif hit.type == 'pow_laser':
            offensive_power_sound.play()
            player.laser_gun()

    #Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    player_group.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, -25, player.lives, player_mini_img)
    pygame.display.flip()
    
pygame.quit()
