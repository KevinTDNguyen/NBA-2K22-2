#IMPORTING MODULES

import pygame
import math
import random

#PYGAME INITALIZATION
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#INITIALIZING VARIABLES

game_active = False
shooting = False

shot_cooldown_og = 4
shot_cooldown = shot_cooldown_og
p1_dmg = 15
p1_kills = 0
dead = False

px = 500
py = 300
p_angle = 0

current_wave = 1
wave_adv_kreq = 20
spawn_time = 1700
show_wave = 0
store_active = False

menu_index = 0
menu_played = False


vbucks = 500

current_weapon = 1

bullet_cap = 8
bullet_remaining = 8
reload_time = 0.5
cur_reload_time = 0
reloading = False
bullet_req = 0

#INITALIZING IMAGES

store_bg = pygame.image.load("storebg.png")
store_bg_rect = store_bg.get_rect(center = (500, 300))

menu_1 = pygame.image.load("menu1.png")
menu_2 = pygame.image.load("menu2.png")

death_screen = pygame.image.load("death_screen.png")
death_screen_rect = death_screen.get_rect(center = (500, 300))

menu_image_lst = [menu_1, menu_2]

store_ak47 = pygame.image.load("shop_ak47.png")
store_ak47_select = pygame.image.load("shop_ak47_select.png")
store_ak47_bought = pygame.image.load("shop_ak47_bought.png")

store_hugh_shotty = pygame.image.load("shop_hugh's_shotty.png")
store_hugh_shotty_select = pygame.image.load("shop_hugh's_shotty_select.png")
store_hugh_shotty_bought = pygame.image.load("shop_hugh's_shotty_bought.png")

store_mp9 = pygame.image.load("shop_mp9.png")
store_mp9_select = pygame.image.load("shop_mp9_select.png")
store_mp9_bought = pygame.image.load("shop_mp9_bought.png")

store_m16 = pygame.image.load("shop_m16.png")
store_m16_select = pygame.image.load("shop_m16_select.png")
store_m16_bought = pygame.image.load("shop_m16_bought.png")

store_aa12 = pygame.image.load("shop_aa12.png")
store_aa12_select = pygame.image.load("shop_aa12_select.png")
store_aa12_bought = pygame.image.load("shop_aa12_bought.png")


#INITALIZING FONTS
font = pygame.font.SysFont("yugothicuisemilight",20)
bigfont = pygame.font.SysFont("cambria", 100)

#PLAYER CLASS
class Player(pygame.sprite.Sprite): #A sprite class makes us able to combine rectangles and images into one (much easier for collision as well)

    def __init__(self):
        super().__init__() #initalizes pygame sprite tools into the initialization method
        self.pistol_image = pygame.image.load("p1.png").convert_alpha() #converts our image into a more usable format for pygame (less laggy)


        self.ak_image = pygame.image.load("p1_ak.png").convert_alpha()


        self.hugh_image = pygame.image.load("p1_hugh_shotty.png").convert_alpha()


        self.mp9_image = pygame.image.load("p1_mp9.png").convert_alpha()


        self.m16_image = pygame.image.load("p1_m16.png").convert_alpha()


        self.aa12_image = pygame.image.load("p1_aa12.png").convert_alpha()


        self.og_image = self.pistol_image #og_image allows us to properly rotate the image according to the mouse (without it the current "rotated" sprite would continue to rotate more than expected)

        self.image = self.pistol_image


        self.angle = 0 #initializes our self.angle variable
        self.rect = self.image.get_rect(center=(500, 300)) #sets our player in the middle of the screen at the start

        self.hp = 200 #initalizes player health

    def key_input(self):
        global shot_cooldown, shot_cooldown_og, p1_dmg, keys, current_weapon, bullet_remaining, bullet_cap, reload_time, reloading, cur_reload_time, bullet_req

        #the WASD input moves the player rectangle (which the player image is on)
        if keys[pygame.K_d]:
            self.rect.centerx += 1
        if keys[pygame.K_a]:
            self.rect.centerx -= 1
        if keys[pygame.K_w]:
            self.rect.centery -= 1
        if keys[pygame.K_s]:
            self.rect.centery += 1

        #Initiates a reload
        if keys[pygame.K_r]:
            cur_reload_time = reload_time #resets the current reload time to the proper value before reloading
            bullet_remaining = 0 #this line is required in order to ensure the reload animation work properly (doesn't overshoot the white barrier)
            reloading = True

        #Next inputs are for changing weapons
        if keys[pygame.K_1]:
            p1_dmg = 10
            self.og_image = self.pistol_image

            reload_time = 0.5
            bullet_cap = 10
            bullet_remaining = 0

            current_weapon = 1
            shot_cooldown_og = 4
            shot_cooldown = shot_cooldown_og

            cur_reload_time = reload_time
            reloading = True

        elif keys[pygame.K_2] and hugh_shotty_bought: #makes sure that the weapon is bought in the shop
            p1_dmg = 50
            self.og_image = self.hugh_image

            reload_time = 0.5
            bullet_cap = 2
            bullet_remaining = 0

            current_weapon = 2
            shot_cooldown_og = 2
            shot_cooldown = shot_cooldown_og

            cur_reload_time = reload_time
            reloading = True

        elif keys[pygame.K_3] and ak_47_bought:
            p1_dmg = 15
            self.og_image = self.ak_image

            reload_time = 1
            bullet_cap = 30
            bullet_remaining = 0

            current_weapon = 3
            shot_cooldown_og = 1
            shot_cooldown = shot_cooldown_og

            cur_reload_time = reload_time
            reloading = True

        elif keys[pygame.K_4] and mp9_bought:
            p1_dmg = 10
            self.og_image = self.mp9_image

            reload_time = 2
            bullet_cap = 45
            bullet_remaining = 0

            current_weapon = 4
            shot_cooldown_og = 0.5
            shot_cooldown = shot_cooldown_og

            cur_reload_time = reload_time
            reloading = True

        elif keys[pygame.K_5] and m16_bought:
            p1_dmg = 15
            self.og_image = self.m16_image

            reload_time = 2
            bullet_cap = 30
            bullet_remaining = 0

            current_weapon = 5
            shot_cooldown_og = 0.2
            shot_cooldown = shot_cooldown_og

            cur_reload_time = reload_time
            reloading = True

        elif keys[pygame.K_6] and aa12_bought:
            p1_dmg = 25
            self.og_image = self.aa12_image

            reload_time = 3
            bullet_cap = 20
            bullet_remaining = 0

            current_weapon = 6
            shot_cooldown_og = 1
            shot_cooldown = shot_cooldown_og

            cur_reload_time = reload_time
            reloading = True



    def mouse_input(self): #this is for player rotation according to mouse movement
        global mouse_pos, p_angle

        x_dist = mouse_pos[0] - self.rect.centerx #finds the distance between our player and the cursor along the x-axis
        y_dist = -(mouse_pos[1] - self.rect.centery) #finds the distance between our player and the cursor along the y-axis (the value must be negative because pygame doesn't use the cartesian plane)
        self.angle = math.degrees(math.atan2(y_dist, x_dist)) #calculates the angle of our player using trig. (tan. inverse) --> (y_dist is opp., x_dist is adj)
        p_angle = self.angle #stores this as a global variables to be used outside the class
        self.image = pygame.transform.rotate(self.og_image, self.angle)  #rotates our sprite towards the cursor
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery)) #resets the x and y position of our rectangles (our rectangle moves during the rotation step above)

    def hit(self):
        global enemy, dead
        if pygame.sprite.spritecollide(self, enemy, False, pygame.sprite.collide_mask): #makes player and enemy collision between masks instead of rects (much better hitboxes)
            self.hp -= 1
            if self.hp <= 0:
                dead = True
                self.kill()

    def health_bar(self):

        pygame.draw.polygon(screen, "green", ((17, 10), (10, 25), (self.hp + 10, 25), (self.hp + 17, 10)))
        pygame.draw.polygon(screen, (0, 160, 0), ((13, 20), (10, 25), (self.hp + 10, 25), (self.hp + 13, 20)))
        pygame.draw.polygon(screen, "white", ((17, 10), (10, 25), (210, 25), (217, 10)), 2)

    def ammo_bar(self):
        global bullet_remaining, bullet_cap
        pygame.draw.rect(screen, "yellow", ((17, 580), (bullet_remaining * 200/bullet_cap, 15))) #bullet_remaning is divided by bullet_cap to maintain the same size for every gun (ratios)
        pygame.draw.rect(screen, "white", ((17, 580), (200, 15)), 2)




    def update(self): #combines all methods in the class into one that can be used in the game loop (much cleaner and organized)
        global px, py
        self.mouse_input()
        self.key_input()
        self.hit()
        self.health_bar()
        self.ammo_bar()
        px = self.rect.centerx #stores player rectangle coordinate values as a global variable for external use
        py = self.rect.centery


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        global current_wave

        self.normal_image = pygame.image.load("zombie.png").convert_alpha()
        self.normal_image = pygame.transform.rotozoom(self.normal_image, -90, 0.2)

        self.scooter_image = pygame.image.load("zombie_scooter.png").convert_alpha()
        self.scooter_image = pygame.transform.rotozoom(self.scooter_image, -90, 0.2)

        self.brute_image = pygame.image.load("zombie_brute.png").convert_alpha()
        self.brute_image = pygame.transform.rotozoom(self.brute_image, -90, 0.2)

        self.mega_brute_image = pygame.image.load("zombie_mega_brute.png").convert_alpha()
        self.mega_brute_image = pygame.transform.rotozoom(self.mega_brute_image, -90, 0.2)

        image_lst = [self.normal_image]

        #Enemy variation and possibility (wave based)
        if current_wave >= 2:
            image_lst += [self.scooter_image]
        if current_wave >= 5:
            image_lst += [self.brute_image]
        if current_wave >= 10:
            image_lst += [self.mega_brute_image]

        zombie_type = random.randint(0, len(image_lst)-1) #chooses randomly what the spawn enemy type is

        #initialize enemy stats
        if zombie_type == 0:
            self.speed = 1
            self.hp = 30

        elif zombie_type == 1:
            self.speed = 1.5
            self.hp = 15

        elif zombie_type == 2:
            self.speed = 0.75
            self.hp = 50

        elif zombie_type == 3:
            self.speed = 0.5
            self.hp = 100

        self.og_image = image_lst[zombie_type]

        self.image = self.og_image

        self.mask = pygame.mask.from_surface(self.image)

        #random spawn point generation
        spawn_point = random.choice(["top", "bottom", "left", "right"])
        if spawn_point == "top":
            self.rect = self.image.get_rect(center = (random.randint(0,1000), 0))
        elif spawn_point == "bottom":
            self.rect = self.image.get_rect(center = (random.randint(0,1000), 600))
        elif spawn_point == "left":
            self.rect = self.image.get_rect(center = (0, random.randint(0,600)))
        elif spawn_point == "right":
            self.rect = self.image.get_rect(center = (1000, random.randint(0,600)))




        self.x = self.rect.centerx
        self.y = self.rect.centery



    def chase(self):
        global px, py
        enemy_dx = px - self.rect.centerx #finds the distance between our enemy and the player along the x-axis
        enemy_dy = py - self.rect.centery #finds the distance between our enemy and the player along the y-axis
        enemy_angle = math.atan2(enemy_dx, enemy_dy) #calculates the enemy angle using trig. (identical to player angle calculations)
        mvx = math.sin(enemy_angle) #calculates the amount the enemy needs to move along the x-axis
        mvy = math.cos(enemy_angle) #calculates the amount the enemy needs to move along the y-axis

        self.image = pygame.transform.rotate(self.og_image, math.degrees(enemy_angle))
        self.x += mvx*self.speed
        self.y += mvy*self.speed

        self.rect = self.image.get_rect(center = (self.x, self.y))

    def hit(self):
        global bullet, p1_dmg, p1_kills, vbucks
        if pygame.sprite.spritecollide(self, bullet, True, pygame.sprite.collide_mask):
            self.hp -= p1_dmg
            if self.hp <= 0:
                p1_kills += 1
                vbucks += 5
                self.kill()

    def update(self):
        self.chase()
        self.hit()





class Bullet(pygame.sprite.Sprite):

    def __init__(self, angle):
        global px, py
        super().__init__()
        self.og_image = pygame.image.load("bullet.png").convert_alpha()
        self.og_image = pygame.transform.rotozoom(self.og_image, -90, 0.17)

        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.og_image, -90, 0.17)

        self.angle = angle + 90
        self.rect = self.image.get_rect(center=(px, py))

        self.mask = pygame.mask.from_surface(self.image)

        self.x = self.rect.centerx
        self.y = self.rect.centery

    def shoot(self):

        mvx = math.sin(math.radians(self.angle)) #calculates the required movement along the x-axis
        mvy = math.cos(math.radians(self.angle)) #calculates the required movement along the y-axis
        self.image = pygame.transform.rotozoom(self.og_image, self.angle, 0.17) #rotates the sprite
        self.x += mvx*25
        self.y += mvy*25
        self.rect = self.image.get_rect(center = (self.x, self.y))


    def update(self):
        self.shoot()





class Shop_Item(pygame.sprite.Sprite):
    def __init__(self, surface, surface_select, surface_bought, x, y, item_name, price, bought_text):
        global font
        super().__init__()
        self.image_og = surface
        self.image = self.image_og
        self.image_select = surface_select #image that is shown when the cursor is hover over the item in the shop
        self.image_bought = surface_bought #image that is shown when the player already bought the item


        self.rect = self.image.get_rect(center = (x, y))

        self.item_name = item_name

        self.text = font.render(item_name, True, "white") #text shows what weapon is being sold above the item
        self.text_rect = self.text.get_rect(center = (x, y - 135))

        self.bought_text = font.render(bought_text, True, "white") #text shows what key to press in order to use the item
        self.bought_text_rect = self.bought_text.get_rect(center=(x, y - 65))

        self.price = price
        self.bought = False


    def display_text(self):
        screen.blit(self.text, self.text_rect)
        if self.bought:
            pygame.draw.rect(screen, "black", self.bought_text_rect, )
            screen.blit(self.bought_text, self.bought_text_rect)

    def select(self): #shows image with white outline when mouse is hovering over item
        global mouse_pos
        if self.bought == False:
            if self.rect.collidepoint(mouse_pos):
                self.image =  self.image_select

            else:
                self.image = self.image_og

    def purchase(self):
        global vbucks, ak_47_bought, hugh_shotty_bought, mp9_bought, m16_bought, aa12_bought
        if self.rect.collidepoint(mouse_pos):
            if vbucks >= self.price: #checks if the amount of vbucks is enough to buy the item
                if self.item_name == "Make Great 47 (115 V)" and ak_47_bought == False: #changes the bought status of thw weapon to True
                    self.bought = True
                    self.image = self.image_bought
                    ak_47_bought = True
                    vbucks -= self.price
                if self.item_name == "HUGH'S DB [nerfed] (50 V)" and hugh_shotty_bought == False:
                    self.bought = True
                    self.image = self.image_bought
                    hugh_shotty_bought = True
                    vbucks -= self.price
                if self.item_name == "Ryan's Toys Review 9 (80 V)" and mp9_bought == False:
                    self.bought = True
                    self.image = self.image_bought
                    mp9_bought = True
                    vbucks -= self.price
                if self.item_name == "Mr Beast (150 V)" and m16_bought == False:
                    self.bought = True
                    self.image = self.image_bought
                    m16_bought = True
                    vbucks -= self.price
                if self.item_name == "Miniou-12 [w/ switch] (350 V)" and aa12_bought == False:
                    self.bought = True
                    self.image = self.image_bought
                    aa12_bought = True
                    vbucks -= self.price


    def update(self):
        self.display_text()
        self.select()










def wave():
    global current_wave, wave_adv_kreq, p1_kills, spawn_time, show_wave

    if p1_kills >= wave_adv_kreq:
        current_wave += 1
        wave_adv_kreq += 10
        spawn_time -= 100
        show_wave = 1
        pygame.time.set_timer(enemy_spawn, spawn_time)
    
    wave_text = bigfont.render("WAVE "+str(current_wave), True, "black")
    wave_text_rect = wave_text.get_rect(center = (500, 300))

    if show_wave > 0:
        pygame.draw.rect(screen, "white", wave_text_rect)
        pygame.draw.rect(screen, "black", wave_text_rect, 4)
        screen.blit(wave_text, wave_text_rect)
        show_wave -= 0.01




def shop():
    global keys, game_active, store_bg, store_bg_rect, store_active

    if game_active:
        game_active = False
        store_active = True
    else:
        game_active = True
        store_active = False

    if store_active:
        screen.blit(store_bg, store_bg_rect)



def main_menu():
    global game_active, menu_played, menu_index, menu_image_lst, menu_1, menu_2
    if menu_played == False:
        menu_rect = menu_image_lst[menu_index].get_rect(center = (500, 300))
        screen.blit(menu_image_lst[menu_index], menu_rect)





player = pygame.sprite.GroupSingle()
player.add(Player())

enemy = pygame.sprite.Group()

bullet = pygame.sprite.Group()
# bullet.add(Bullet())

shop_items = pygame.sprite.Group()

hugh_shotty_bought = False
shop_items.add(Shop_Item(store_hugh_shotty, store_hugh_shotty_select, store_hugh_shotty_bought, 160, 165 ,"HUGH'S DB [nerfed] (50 V)", 50, "[PRESS 2 TO USE]"))

ak_47_bought = False
shop_items.add(Shop_Item(store_ak47, store_ak47_select, store_ak47_bought, 400, 165 ,"Make Great 47 (115 V)", 115, "[PRESS 3 TO USE]"))

mp9_bought = False
shop_items.add(Shop_Item(store_mp9, store_mp9_select, store_mp9_bought, 640, 165 ,"Ryan's Toys Review 9 (80 V)", 80, "[PRESS 4 TO USE]"))

m16_bought = False
shop_items.add(Shop_Item(store_m16, store_m16_select, store_m16_bought, 160, 450 ,"Mr Beast (150 V)", 150, "[PRESS 5 TO USE]"))

aa12_bought = False
shop_items.add(Shop_Item(store_aa12, store_aa12_select, store_aa12_bought, 400, 450 ,"Miniou-12 [w/ switch] (350 V)", 350, "[PRESS 6 TO USE]"))


enemy_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawn, spawn_time)



run = True

main_menu()

#GAME LOOP
while run:

    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()


    if reloading:
        cur_reload_time -= 0.01
        bullet_remaining += bullet_cap / (reload_time * 100)
        if cur_reload_time <= 0:
            bullet_remaining = bullet_cap
            reloading = False





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            left_clicked = pygame.mouse.get_pressed()[0]
            if left_clicked:
                shooting = True
                if store_active:
                    for item in shop_items:
                        item.purchase()



        if event.type == pygame.MOUSEBUTTONUP:
            shooting = False

        if event.type == pygame.KEYDOWN:
            if menu_played:
                if event.key == pygame.K_b:
                    shop()
            if event.key == pygame.K_UP:
                menu_index = 0
                main_menu()
            if event.key == pygame.K_DOWN:
                menu_index = 1
                main_menu()
            if event.key == pygame.K_SPACE:
                if menu_index == 0 and menu_played == False:
                    game_active = True
                    menu_played = True



        if game_active:
            if event.type == enemy_spawn:
                enemy.add(Enemy())


    if game_active:

        if shooting:
            if shot_cooldown <= 0 and bullet_remaining > 0 and reloading == False:
                if current_weapon == 2 or current_weapon == 6:
                    for i in range(3):
                        bullet.add(Bullet(p_angle + random.randint(-15, 15)))
                elif current_weapon == 5:
                    shot_cooldown_og = 0.2
                    if (bullet_cap - bullet_remaining) % 3 == 0 and bullet_remaining != 30:
                        shot_cooldown_og = 3
                    bullet.add(Bullet(p_angle))



                else:
                    bullet.add(Bullet(p_angle))

                shot_cooldown = shot_cooldown_og
                bullet_remaining -= 1


        shot_cooldown -= .1

        kill_text = font.render("KILLS: "+ str(p1_kills), True, "black")
        kill_text_rect = kill_text.get_rect(topleft = (10, 35))

        vbucks_text = font.render("VBUCKS: " + str(vbucks), True, "black")
        vbucks_text_rect = vbucks_text.get_rect(topleft=(10, 60))

        screen.fill("grey")


        bullet.draw(screen)
        bullet.update()

        enemy.draw(screen)
        enemy.update()

        player.draw(screen)
        player.update()

        wave()

        screen.blit(kill_text, kill_text_rect)
        screen.blit(vbucks_text, vbucks_text_rect)

    if store_active:
        shop_items.draw(screen)
        shop_items.update()
    if dead:
        screen.blit(death_screen, death_screen_rect)

    pygame.time.Clock().tick(60)
    pygame.display.flip()

pygame.quit()

