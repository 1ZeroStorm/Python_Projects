import math
import random
import pygame

clock = pygame.time.Clock()

pygame.init()

debris_images = []
explosion_images = []
spacebg = None


debrisSize = (50, 50)
explosionSize = (50,50)
bulletSize = (10,10) # same as radius 5

def loadImage():

    for j in range(10):
        explosion_image_pygame = pygame.image.load(f'explosion/{j}-removebg-preview.png')
        explosion_resized_image = pygame.transform.scale(explosion_image_pygame, explosionSize)
        explosion_images.append(explosion_resized_image)
            
    for j in range(5):
        debris_image_pygame = pygame.image.load(f'debris/{j}.png')
        debris_resized_image = pygame.transform.scale(debris_image_pygame, debrisSize)
        debris_images.append(debris_resized_image)


arcade_font = pygame.font.Font('fonts/arcade_font.ttf', 10)
arcade_font_small = pygame.font.Font('fonts/arcade_font.ttf', 9)

gothic_font_small = pygame.font.Font('fonts/CenturyGothic.ttf', 10)
gothic_font_medium = pygame.font.Font('fonts/CenturyGothic.ttf', 12)
gothic_font_big = pygame.font.Font('fonts/CenturyGothic.ttf', 23)
spacebg = pygame.image.load('user_interfaces/spacebg.png')
ship_faces=[pygame.image.load('spaceship_faces/face3.png'), pygame.image.load('spaceship_faces/face3_notfly-01.png'), pygame.image.load('spaceship_faces/spacedmg-01.png')]

for j in range(1,3):
    ship_faces[j] = pygame.transform.scale(ship_faces[j], ship_faces[0].get_size())

game_title_image = pygame.image.load('user_interfaces/starwake_protocol_logo.png')
game_title_image = pygame.transform.scale(game_title_image, (game_title_image.get_size()[0] // 2, game_title_image.get_size()[1] // 2))
click_to_play_text = gothic_font_big.render('<NEW GAME>', True, (255, 255, 255))
creator_text = gothic_font_medium.render('By Yohanes Arya P.', True, (95, 158, 160))

loadImage()

incrementSize = 2.4
x_window = spacebg.get_size()[0] * incrementSize # SCREEN WIDTH
y_window = spacebg.get_size()[1]* incrementSize # SCREEN HEIGHT
windowcenterx, windowcentery = x_window//2, y_window//2

window = pygame.display.set_mode((x_window, y_window)) # width and height of window
pygame.display.set_caption('Starwake Protocol') # caption in window next to close button

resized_image_spacebg = pygame.transform.scale(spacebg, (x_window, y_window))
print(f'initialing with window size: ({resized_image_spacebg.get_size()[0]}, {resized_image_spacebg.get_size()[1]})')

print_signal = 0

enemydebounceCounter = 0
enemy_junk_list = []
global_enemy_list = []

playerCollusion = False
forcefieldcounter = 0
collusionPushPlayer = False

bullets = []
clickFire = True
clickFireCounter = 0

# Bullet class
class Bullet:
    def __init__(self, pos, target, speed, size):
        self.pos = pygame.Vector2(pos)
        direction = pygame.Vector2(target) - self.pos
        if direction.length() != 0:
            self.velocity = direction.normalize() * speed
        else:
            self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, *size)

    def update(self):
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.pos, bulletSize[0]/2)

    def is_off_screen(self):
        return not window.get_rect().colliderect(self.rect)
    
class shotgun:
    def __init__(self, pos, target, speed):
        self.image = pygame.image.load('ability_properties/blue_bullet.png')
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.pos = pygame.Vector2(pos)
        direction = pygame.Vector2(target) - self.pos

        self.angle_rad = math.atan2(dy, dx)
        self.angle_deg = -math.degrees(self.angle_rad)  # negative to rotate correctly
        self.moe_deg = self.angle_deg + random.randint(-30, 30)
        revised_radian = math.radians(-self.moe_deg)
        self.direction_revised = pygame.Vector2(math.cos(revised_radian), math.sin(revised_radian))

        self.rotated_image = pygame.transform.rotate(self.image, self.moe_deg)
        

        if self.direction_revised.length() != 0:
            self.velocity = self.direction_revised.normalize() * speed
        else:
            self.velocity = pygame.Vector2(0, 0)

        
        self.rect = pygame.Rect(self.pos.x, self.pos.y, *(50, 20))
        self.rotated_rect = self.rotated_image.get_rect(center=self.pos)
        


    def update(self):
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        

    def draw(self, surface):
        surface.blit(self.rotated_image,self.pos)
        #pygame.draw.circle(surface, (255, 255, 255), self.pos, 10)
        

    def is_off_screen(self):
        return not window.get_rect().colliderect(self.rect)

class makeShotgun:
    def __init__(self):
        self.activated = False
        self.clickFire = True
        self.bulletobjects = []
        self.clickFireCounter = 0
        self.name = 'spraybullet'
        self.card_name = 'spraybullet'
        self.usage = 20
        self.notif_toggle = False

    def draw(self, surface):
        for bullet in self.bulletobjects:
            bullet.draw(surface)
    
    def update(self):
        for bullet in self.bulletobjects:
            bullet.update()

class Enemy:
    def __init__(self, player_pos, x_window, y_window):
        self.speed = 5
        self.lifespanCounter = 0
        self.lifespanEnd = 10000
        self.image = debris_images[random.randint(0, len(debris_images)-1)]
        self.distanceFromplayer_x =0
        self.distanceFromplayer_y =0
        self.direction = None

        # Random movement type
        self.direction_type = random.choice(['linear', 'targetplayer'])

        # Choose random border: top, bottom, left, right
        side = random.choice(['top', 'bottom', 'left', 'right'])

        if side == 'left':
            self.pos = [0, random.randint(0, y_window)]
        elif side == 'right':
            self.pos = [x_window, random.randint(0, y_window)]
        elif side == 'top':
            self.pos = [random.randint(0, x_window), 0]
        elif side == 'bottom':
            self.pos = [random.randint(0, x_window), y_window]

        self.pos = pygame.Vector2(self.pos)

        if self.direction_type == 'linear':
            # Go toward center of screen
            center = pygame.Vector2(x_window // 2, y_window // 2)
            self.direction = center - self.pos
        else:
            # Track the player
            self.direction = pygame.Vector2(player_pos) - self.pos

        # Normalize direction and apply speed
        if self.direction.length() != 0:
            self.velocity = self.direction.normalize() * self.speed
        else:
            self.velocity = pygame.Vector2(0, 0)

        # Rectangle for drawing or collision
        self.rect = pygame.Rect(int(self.pos.x), int(self.pos.y), *(debrisSize))  # Size of the enemy


    def update(self):
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.lifespanCounter += 1

    def draw(self, surface):
        window.blit(self.image, self.pos)
        #pygame.draw.circle(surface, (255, 255, 0), self.pos, 15)

    def freeze(self):
        self.velocity = pygame.Vector2(0, 0)
    
    def unfreeze(self):
        self.velocity = self.direction.normalize() * self.speed

explosionList = []

class ExplosionEffect:
    def __init__(self, pos):
        

        self.pos = pos
        self.imageIteration = 0

    def draw(self, surface):
        surface.blit(explosion_images[self.imageIteration], self.pos)
        self.imageIteration += 1

class player_spaceship:
    def __init__(self):
        self.vel = 5
        self.vel_up = 0
        self.vel_down = 0
        self.vel_right = 0
        self.vel_left = 0
        self.playerPoints = 0
        
        self.size = ship_faces[1].get_size()
        self.face = ship_faces[1]
        self.C_effect_face = ship_faces[2]

        self.x = windowcenterx - self.size[0]/2
        self.y = windowcentery + 100


width,height = (ship_faces[1].get_size()[0], ship_faces[1].get_size()[1])


player = player_spaceship()

#_________________________ability: blue plasma laser________________________________________

class blueLaser:
    def __init__(self, dx, dy):
        self.name = 'laser'
        self.card_name = 'laser'
        self.usage = 2
        self.activated = False
        self.shoot = False
        self.charge = False
        self.lasetransparencyCounter = 255
        self.chargeFrameCount = 0
        self.laserFrameCount = 0
        self.image_radius = 0
        
        self.angle_rad = 0
        self.angle_deg = -math.degrees(self.angle_rad)  # negative to rotate correctly
        self.slope = 0

        

        #load images and store on a list
        self.laserList = []
        
        for j in range(3):
            real_laserSize = pygame.image.load(f"laser_ability/laser{j +1}.png").convert_alpha()
            real_laserSize = pygame.transform.scale(real_laserSize, (real_laserSize.get_size()[0] - 40, real_laserSize.get_size()[1] - 60))
            self.laserList.append(real_laserSize)

        self.laserload_img = pygame.image.load("laser_ability/laserLoad.png").convert_alpha()
        self.laserload_img.set_alpha(128)
        self.laserload_img = pygame.transform.scale(self.laserload_img, (1000, 300))
                
        # load charge image
        self.chargeimg = pygame.image.load(f"laser_ability/charge1.png").convert_alpha()
        self.chargeimg = pygame.transform.scale(self.chargeimg, (30, 30))

#_________________________ability: hack________________________________________
glitch_img_list = []
for j in range(4):
    glitch_img = pygame.image.load(f'glitch_effects/{j + 1}.png')
    glitch_img = pygame.transform.scale(glitch_img, debrisSize)
    glitch_img_list.append(glitch_img)

class hack:
    def __init__(self, playerpos, playercenterpos, playersize):
        self.name = 'hack'
        self.card_name = 'disruption'
        self.usage = 3
        self.activate = False
        self.spawndb = False
        self.activationCounter = 0
        self.base_radius = 40      # starting radius
        self.num_circles = 3       # number of concentric circles
        self.radius_gap = 30       # distance between each circle
        self.thickness = 4         # outline thickness
        self.color = (0, 255, 0)   # green
        self.enemiesinBound = {}

        

        self.centerpos = pygame.Vector2(playercenterpos)
        self.update_surface()

    def update_surface(self):
        max_radius = self.base_radius + self.radius_gap * (self.num_circles - 1)
        diameter = max_radius * 2
        self.hack_img = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

        center = (max_radius, max_radius)
        for i in range(self.num_circles):
            radius = self.base_radius + i * self.radius_gap
            pygame.draw.circle(self.hack_img, self.color, center, radius, self.thickness)

        self.pos = pygame.Vector2(self.centerpos.x - max_radius, self.centerpos.y - max_radius)

    def draw(self):
        window.blit(self.hack_img, self.pos)

    def increase_size(self, playercenterpos):
        self.base_radius += 5
        if not self.spawndb:
            self.centerpos = pygame.Vector2(playercenterpos)
            self.spawndb = True
        self.update_surface()

    def draw_glitch(self, pos): # pos should be vector 2, tuple or pygame rect
        window.blit(glitch_img_list[random.randint(0, len(glitch_img_list) - 1)], pos)
        
#______________________________________space snipers__________________________________________________________


class spacesnipers:
    def __init__(self):
        self.name = 'spacesnipers'
        self.flying = False
        self.size = (100, 100)
        self.original_image = pygame.image.load('ability_properties/spacesniper.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.laser_img = pygame.image.load('ability_properties/sniperlaser.png').convert_alpha()
        self.initsizex_laserImg = self.laser_img.get_size()[0]
        self.initsizey_laserImg = 30
        self.laser_img = pygame.transform.scale(self.laser_img, (self.initsizex_laserImg, self.initsizey_laserImg))
        self.lockenemy = None

        self.base_speed = 6  # base speed to be scaled by deceleration
        self.velocity = pygame.Vector2(0, 0)

        self.waitCounter = 0

        self.x_window = x_window
        self.y_window = y_window

        # Choose a side to spawn from
        self.spawn_side = random.choice(['left', 'right', 'top', 'bottom'])
        if self.spawn_side == 'left':
            self.pos = pygame.Vector2(-self.size[0], random.randint(0, y_window))
        elif self.spawn_side == 'right':
            self.pos = pygame.Vector2(x_window + self.size[0], random.randint(0, y_window))
        elif self.spawn_side == 'top':
            self.pos = pygame.Vector2(random.randint(0, x_window), -self.size[1])
        else:  # bottom
            self.pos = pygame.Vector2(random.randint(0, x_window), y_window + self.size[1])

        

        # Define movement path: 2 random positions + back to off-screen exit
        self.path = [
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            self.get_exit_point()  # return to offscreen
        ] # getting copy
        
        self.path_index = 0
        self.target = self.path[self.path_index]
        self.velocity = self.get_velocity()
        

    def get_exit_point(self):
        if self.spawn_side == 'left':
            return pygame.Vector2(int(-self.size[0]), int(random.randint(0, self.y_window)))
        elif self.spawn_side == 'right':
            return pygame.Vector2(int(self.x_window + self.size[0]), int(random.randint(0, self.y_window)))
        elif self.spawn_side == 'top':
            return pygame.Vector2(int(random.randint(0, self.x_window)), int(-self.size[1]))
        else:
            return pygame.Vector2(int(random.randint(0, self.x_window)), int(self.y_window + self.size[1]))

    def get_velocity(self):
        direction = self.target - self.pos
        if direction.length() != 0:
            return direction.normalize() * 6
        return pygame.Vector2(0, 0)

    def update(self):
        if self.path_index < len(self.path):
            self.flying = True
            direction = self.target - self.pos
            distance = direction.length()

            if self.waitCounter <= 0:
                if distance > 2 : # flying
                    # Recalculate velocity toward the target and apply deceleration factor
                    deceleration_factor = min(1.0, distance / 50)  # the closer, the slower (range ~0–1)
                    velocity = direction.normalize() * self.base_speed * deceleration_factor
                    self.pos += velocity
                    self.velocity = velocity  # store for rotation
                else: #stationary

                    def findEnemy():
                        for enemy in enemy_junk_list:
                            if 20 < enemy.pos.x < x_window and 20 < enemy.pos.y < y_window:
                                #print(enemy.pos)
                                return enemy

                    self.lockenemy = findEnemy()
                    self.waitCounter = 100
                    # Snap to target and go to next point
                    self.pos = self.target
                    self.path_index += 1
                    if self.path_index < len(self.path):
                        self.target = self.path[self.path_index]
                    self.velocity = pygame.Vector2(0, 0)
                    
            else:
                self.waitCounter -= 1
                #print(self.target)
        else:
            self.flying = False
            

    def draw(self):
        # Rotate the image to face direction of movement
        if self.velocity.length() > 0:
            angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))  # Negative y because pygame y is downward
            rotated_image = pygame.transform.rotate(self.original_image, angle+270)
            rect = rotated_image.get_rect(center=self.pos)
            window.blit(rotated_image, rect.topleft)
            self.laser_img = pygame.transform.scale(self.laser_img, (self.initsizex_laserImg, self.initsizey_laserImg))

        else:
            if self.path_index <= len(self.path) - 1:
                # Calculate direction vector
                if not (self.lockenemy):
                    d = pygame.Vector2(windowcenterx, windowcentery) - self.pos
                else:
                    d = self.lockenemy.rect.center - self.pos

                # Calculate angle in degrees (atan2 uses y first)
                angle_rad = math.atan2(d.y, d.x)
                angle_deg = -math.degrees(angle_rad)

                # Get laser offset (rotate 90° to face forward)
                image_radius = self.laser_img.get_size()[0] / 2
                offset_x = math.cos(angle_rad) * image_radius
                offset_y = math.sin(angle_rad) * image_radius

                # Final laser orbit position based on player position and angle
                orbit_pos = self.pos + pygame.Vector2(offset_x, offset_y)
                rotated_laser = pygame.transform.rotate(self.laser_img, angle_deg)
                rotated_rect = rotated_laser.get_rect(center=orbit_pos)

                # Draw  the laser
                window.blit(rotated_laser, rotated_rect)

                # rotate spaceship
                rotated_image = pygame.transform.rotate(self.original_image, angle_deg+270)
                rect = rotated_image.get_rect(center=self.pos)
                window.blit(rotated_image, rect.topleft)
                
                # reducing laser size
                if self.laser_img.get_size()[1] > 1:
                    self.laser_img = pygame.transform.scale(self.laser_img, (self.initsizex_laserImg, self.laser_img.get_size()[1] - .2))

                # hitbox system
                margin = 40
                
                for enemy in enemy_junk_list:
                    d_enemy = pygame.Vector2(enemy.rect.center[0], enemy.rect.center[1]) - self.pos # self.pos is the center of spaceship
                    if not (d.x == 0) and not (d.y == 0):
                        slope = d.y/d.x
                        
                        if slope * d_enemy.x- margin <= d_enemy.y <= slope * d_enemy.x + margin:
                            

                            if d.x > 0 and d.y < 0 and d_enemy.x > 0 and d_enemy.y < 0 : #first quadrant
                                eliminate_with_explosion(enemy, enemy.rect.center)
                            elif d.x < 0 and d.y < 0 and d_enemy.x < 0 and d_enemy.y < 0 : #second quadrant
                                eliminate_with_explosion(enemy, enemy.rect.center)
                            elif d.x < 0 and d.y > 0 and d_enemy.x < 0 and d_enemy.y > 0 : #third quadrant
                                eliminate_with_explosion(enemy, enemy.rect.center)
                            elif d.x > 0 and d.y > 0 and d_enemy.x > 0 and d_enemy.y > 0 : #fou rth quadrant
                                eliminate_with_explosion(enemy, enemy.rect.center)
                            
                    elif d.x == 0 and -margin <= enemy.rect.centerx <= margin:
                        if enemy.rect.centery <= 0:
                            eliminate_with_explosion(enemy, enemy.rect.center)
                        elif enemy.rect.centery >= 0:
                            eliminate_with_explosion(enemy, enemy.rect.center)
                    elif d.y == 0 and -margin <= enemy.rect.centery <= margin:
                        if enemy.rect.centerx >= 0:
                            eliminate_with_explosion(enemy, enemy.rect.center)
                        elif enemy.rect.centerx <= 0:
                            eliminate_with_explosion(enemy, enemy.rect.center)

amountcallsnipers = 1

class many_spacesnipers:
    def __init__(self):
        self.name = 'manyspacesnipers'
        self.card_name = 'backstrike'
        self.usage = 2
        
        self.spawnEnabled = True
        self.pilot_one = spacesnipers()
        self.pilot_two = spacesnipers()

    def update(self):
        self.pilot_one.update()
        self.pilot_two.update()
        

    def draw(self):
        self.pilot_one.draw()
        self.pilot_two.draw()
        

    def reset(self):
        self.pilot_one.path = [
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            self.pilot_one.get_exit_point()  # return to offscreen
        ]
        self.pilot_two.path = [
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            pygame.Vector2(int(random.randint(50, x_window - 50)), int(random.randint(50, y_window - 50))),
            self.pilot_two.get_exit_point()  # return to offscreen
        ]
        self.pilot_one.path_index = 0
        self.pilot_two.path_index = 0

        self.pilot_one.target = self.pilot_one.path[self.pilot_one.path_index]
        self.pilot_two.target = self.pilot_two.path[self.pilot_two.path_index]
        self.pilot_one.velocity = self.pilot_one.get_velocity()
        self.pilot_two.velocity = self.pilot_two.get_velocity()


blackhole_particle_images = []
for j in range(4):
    img = pygame.image.load(f'black_particle/{j+1}.png')
    img = pygame.transform.scale(img, (30, 30))
    blackhole_particle_images.append(img)

blackhole_images = []
for j in range(2):
    img = pygame.image.load(f'black_hole/{j+1}.png')
    img = pygame.transform.scale(img, (100, 100))
    blackhole_images.append(img)



class blackhole:
    def __init__(self):
        self.toggleactive = True
        self.usage = 3
        self.blackholeobject = []
        
        self.name = 'blackhole'
        self.card_name = 'blackhole'
        self.active = False
        self.spawnDebounce = True
        self.time_earlier = pygame.time.get_ticks() // 1000


class blackhole_particle:
    def __init__(self, blackholepos_Start):
        self.pos = pygame.Vector2(blackholepos_Start.x + random.randint(-100, 100), blackholepos_Start.y + random.randint(-100, 100))
        self.eased_pos = pygame.Vector2(0,0)
        self.t = 0
        self.image_frame = 0  # Animation frame index
        self.frame_counter = 0  # Counts update calls for frame timing

        self.frames_total = 4  # Number of animation frames
        self.frame_duration = 5  # How many update() calls each frame lasts
        self.current_image = blackhole_particle_images[0]
        

    def getglitchluck(self):
        rand = random.randint(0, 20)
        if rand == 0 :
            return True
        else:
            return False


    def update(self, currentblackholepos):
        if self.t < 1.0:
            self.t += 0.02
            if self.t > 1.0:
                self.t = 1.0

        # Animation frame update: all frames last the same period
        if self.image_frame < self.frames_total:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_duration:
                self.image_frame += 1
                self.frame_counter = 0

        # Quadratic ease-in for position
        eased_progress = self.t ** 2
        self.eased_pos = self.pos.lerp(currentblackholepos, eased_progress)

        self.angle_rad = -math.atan2(self.eased_pos.y - currentblackholepos.y, self.eased_pos.x - currentblackholepos.x)
        self.angle_deg = math.degrees(self.angle_rad)
        


    def draw(self):
        # All frames appear for the same period of time
        if self.image_frame < self.frames_total:
            self.current_image = blackhole_particle_images[self.image_frame]
            self.current_image = pygame.transform.rotate(self.current_image, self.angle_deg)
            window.blit(self.current_image, self.eased_pos)
        elif self.t < 1.0:
            # After animation, hold last frame until t >= 1.0
            self.current_image = blackhole_particle_images[self.frames_total - 1]
            self.current_image = pygame.transform.rotate(self.current_image, self.angle_deg)
            window.blit(self.current_image, self.eased_pos)
        
        if self.getglitchluck():
            window.blit(glitch_img_list[random.randint(0, len(glitch_img_list) - 1)], self.eased_pos)

class blackhole_army(blackhole):
    def __init__(self, playercenterpos, randomblackholepos):
        self.randomblackholepos = randomblackholepos
        self.growth_progress = 0.0  # 0.0=start, 1.0=full size at random pos
        self.playercenterpos = playercenterpos
        self.lifespan = 1000
        self.lifespan_counter = 0
        self.lifespan_timeearlier = pygame.time.get_ticks() // 1000
        self.particleobject = []
       
        self.image_index = 0
        self.imageiterationCounter = 0
        self.lerpedPos = pygame.Vector2(0,0)
        self.centerlerpedPos = pygame.Vector2(0,0)
        self.absorbtion_center = pygame.Vector2(0,0)
        self.centerforhitbox = pygame.Vector2(0,0)
        
        # Shrink variables
        self.shrink_progress = 0.0  # 0.0=start shrinking, 1.0=fully shrunk
        self.is_shrinking = False
        self.max_size = 150  # Store the maximum size before shrinking

    def update(self):
        
        # Progress the growth (tweak speed as needed)
        if self.growth_progress < 1.0:
            self.growth_progress += 0.02
            if self.growth_progress > 1.0:
                self.growth_progress = 1.0
        # Do not deactivate when fully grown; stays at target and keeps switching images

    def start_shrink(self):
        """Start the shrinking process with quadratic easing"""
        self.is_shrinking = True
        self.shrink_progress = 0.0
        self.max_size = 150  # Store current max size

    def shrink(self):
        """Shrink the blackhole with quadratic ease-in (starts slow, accelerates)"""
        if not self.is_shrinking:
            return
            
        # Progress the shrinking with quadratic ease-in
        if self.shrink_progress < 1.0:
            self.shrink_progress += 0.03  # Adjust speed as needed
            if self.shrink_progress > 1.0:
                self.shrink_progress = 1.0
                
        # Quadratic ease-in: t² (starts slow, accelerates)
        eased_shrink = self.shrink_progress ** 2
        
        # Calculate new size: from max_size down to 0
        new_size = int(self.max_size * (1 - eased_shrink))
        
        return new_size

    def draw(self):

        # Apply quadratic ease-out to position (starts fast, ends slow)
        # Use 1 - (1-t)^2 for quadratic ease-out - starts fast, decelerates
        eased_progress = 1 - (1 - self.growth_progress) ** 2
        
        # Interpolate position with quadratic easing
        self.lerpedPos = self.playercenterpos.lerp(self.randomblackholepos, eased_progress)
        self.centerlerpedPos = self.lerpedPos + pygame.Vector2(blackhole_images[0].get_size()[0]/2, blackhole_images[0].get_size()[1]/2)
        self.absorbtion_center = self.lerpedPos - pygame.Vector2(20, 20)
        self.centerforhitbox = self.absorbtion_center + pygame.Vector2(20, 20)
        
        # Calculate size based on growth and shrinking
        if self.is_shrinking:
            # Use shrink method for size calculation
            size = self.shrink()
        else:
            # Apply quadratic ease-out to size (starts fast, ends slow)
            # Use 1 - (1-t)^2 for quadratic ease-out - starts fast, decelerates
            if self.lifespan_counter < self.lifespan:
                size = int(1 + 149 * eased_progress)  # from 1 to 150 with quad ease-out
            else:
                size = 150

        # Alternate between blackhole_images[0] and blackhole_images[1] every call
        if len(blackhole_images) > 1:
            img = blackhole_images[self.image_index % 2]
            self.imageiterationCounter += 1
            if self.imageiterationCounter >= 5:
                if self.image_index == 2:
                    self.image_index = 0
                else:
                    self.image_index += 1
                self.imageiterationCounter = 0
        else:
            img = blackhole_images[0]

        scaled_img = pygame.transform.scale(img, (size, size))
        rect = scaled_img.get_rect(center=(int(self.lerpedPos.x), int(self.lerpedPos.y)))
        window.blit(scaled_img, rect)


bomberplane_image = pygame.image.load('ability_properties/bomberplane.png').convert_alpha()
bomberplane_image = pygame.transform.scale(bomberplane_image, (300, 300))

spacebomb_image = pygame.image.load('ability_properties/spacebomb.png').convert_alpha()
spacebomb_image = pygame.transform.scale(spacebomb_image, (50, 50))

blue_explosion_size = (100, 100)
blue_explosionList = []
for j in range(10):
    explosion = pygame.image.load(f'blue_explosion/{j+1}-01.png').convert_alpha()
    explosion = pygame.transform.scale(explosion, (blue_explosion_size[0] * 1.02 * (j), blue_explosion_size[1] * 1.02 * (j)))
    blue_explosionList.append(explosion)

class spacebomb:
    def __init__(self, startpos, targetpos):
        self.startpos = pygame.Vector2(*startpos)
        self.targetpos = pygame.Vector2(*targetpos)
        self.currentpos = pygame.Vector2(*self.startpos)
        self.rect = pygame.Rect(self.currentpos.x, self.currentpos.y, 50, 50)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 8
        self.done = False  # done doing the animation, not explosion
        self.explosion_done = False  # done doing the explosion
        self.rectsize = (50, 50)
        direction = self.targetpos - self.startpos
        if direction.length() != 0:
            self.velocity = direction.normalize() * self.speed
        else:
            self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(self.startpos.x, self.startpos.y, *self.rectsize)
        self.t = -10
        self.bombstationaryduration = 0
        self.explosion_counter_enabled = True

        self.rotated_spacebomb_image = pygame.transform.rotate(spacebomb_image, random.randint(0, 360))
        self.rotated_spacebomb_image_rect = self.rotated_spacebomb_image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def update(self):
        # Only move and slow down if not at target
        if not self.done:
            # Check if currentpos is close enough to targetpos
            if (self.currentpos - self.targetpos).length() > 0.1:
                self.currentpos += self.velocity
                self.rect.topleft = (int(self.currentpos.x), int(self.currentpos.y))
                # Subtract 0.2 from velocity in the direction of movement until reaching target
                if self.velocity.length() > 0.2:
                    self.velocity = self.velocity - self.velocity.normalize() * 0.2
                else:
                    self.velocity = pygame.Vector2(0, 0)
            else:
                # Snap to target and start stationary duration
                self.currentpos = self.targetpos
                self.rect.topleft = (int(self.currentpos.x), int(self.currentpos.y))
                self.velocity = pygame.Vector2(0, 0)
                
            if self.bombstationaryduration < 100:
                self.bombstationaryduration += 1
            if self.bombstationaryduration >= 100:
                self.done = True

        if self.done and self.t < 9:
            self.t += 1

        if self.t >= 9:
            self.explosion_done = True

    def draw(self):
        if not (self.done):
            window.blit(self.rotated_spacebomb_image, self.rect)
            
        else:
            equation = math.floor(-abs(self.t) + 10)
            image = blue_explosionList[equation-1]
            window.blit(image, self.rect.topleft - pygame.Vector2(image.get_size()[0] / 2, image.get_size()[1] / 2))
            
    
    def cleanup(self):
        """Clean up resources when bomb is done"""
        self.rotated_spacebomb_image = None
        self.rotated_spacebomb_image_rect = None

class bomber:
    def __init__(self):
        self.rectsize = (300, 300)
        self.speed = 8
        self.startpos = pygame.Vector2(-self.rectsize[0], random.randint(0, y_window))
        self.currentpos = self.startpos
        self.randomcenterpos = pygame.Vector2(random.randint(windowcenterx-30, windowcenterx + 30), random.randint(windowcentery-30, windowcentery + 30))
        self.slope = (self.randomcenterpos.y - self.startpos.y) / (self.randomcenterpos.x - self.startpos.x)
        self.y_intercept = self.startpos.y - self.slope * self.startpos.x
        self.endpos = pygame.Vector2(x_window + self.rectsize[0], self.use_linear_equation(x_window + self.rectsize[0]))
        direction = self.endpos - self.startpos
        if direction.length() != 0:
            self.velocity = direction.normalize() * self.speed
        else:
            self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(self.startpos.x, self.startpos.y, *self.rectsize) 

        
        self.angle_rad = -math.atan2(self.velocity.y, self.velocity.x)
        self.angle_deg = math.degrees(self.angle_rad)
        self.rotated_bomber_plane_image = pygame.transform.rotate(bomberplane_image, self.angle_deg-90)
        self.rotated_bomber_plane_image_rect = self.rotated_bomber_plane_image.get_rect(center=(self.rect.centerx, self.rect.centery))
        
        self.early_time = pygame.time.get_ticks()
        self.bomb_storage = []
        self.amountbombs = 0

    def use_linear_equation(self, x_given):
        return self.slope * x_given + self.y_intercept
    
    def update(self):
        self.currentpos += self.velocity
        self.rect.topleft = (int(self.currentpos.x), int(self.currentpos.y))
        self.rotated_bomber_plane_image_rect.topleft = (int(self.currentpos.x), int(self.currentpos.y))

        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.early_time >= 300 and self.amountbombs <= 10:
            self.early_time = self.current_time
            self.amountbombs += 1
            randomspawnfromcenter = pygame.Vector2(random.randint(self.rect.centerx - 30, self.rect.centerx + 30), random.randint(self.rect.centery - 30, self.rect.centery + 30))
            self.bomb_storage.append(spacebomb(self.rect.center, randomspawnfromcenter))
            #print('bomb added')


    def draw(self, surface):
        surface.blit(self.rotated_bomber_plane_image, self.rect)
        #pygame.draw.rect(window, (0, 0, 255), self.rect, 1)
    
    def cleanup(self):
        """Clean up bomber resources"""
        self.rotated_bomber_plane_image = None
        self.rotated_bomber_plane_image_rect = None
        # Clean up all bombs
        for bomb in self.bomb_storage:
            bomb.cleanup()
        self.bomb_storage.clear()
    
    def is_off_screen(self):
        """Check if bomber is off screen"""
        return (self.currentpos.x < -self.rectsize[0]-400 or 
                self.currentpos.x > x_window + self.rectsize[0]+400 or
                self.currentpos.y < -self.rectsize[1]-400 or 
                self.currentpos.y > y_window + self.rectsize[1]+400)


        
class makeBomber:
    def __init__(self):
        self.name = 'bomber'
        self.card_name = 'bomber'
        self.usage = 2
        self.bomberobject = []
        self.last_spawn_time = 0
        self.spawnDebounce = True
    
    def cleanup(self):
        """Clean up all bomber resources"""
        for bomber in self.bomberobject:
            bomber.cleanup()
        self.bomberobject.clear()

# -------------------------ability checker------------------------
remaining_abilityList = []
abilityList = []
def checkAbility(name):
    exist = False
    for ability in abilityList:
        if ability.name == name:
            exist = True
    return exist

def getAbility(name):
    obj = None
    for ability in abilityList:
        if ability.name == name:
            obj = ability
    return obj

def check_ability_front(name):
    if len(abilityList)> 0:
        if abilityList[0].name == name:
            return True
        else:
            return False
    else:
        return False

def get_ability_front(name):
    if len(abilityList)> 0:
        if abilityList[0].name == name:
            return abilityList[0]
        else:
            return None
    else:
        return None

def clean_ability_front():
    if abilityList[0].name == 'hack':
        for enemy in enemy_junk_list:
            enemy.unfreeze()

    abilityList.pop(0)

#_____________________________insert ability_________________________________________________

def insertability(name):
    if name == 'laser':
        newlaser = blueLaser(dx, dy)
        abilityList.append(newlaser)
    elif name == 'disruption':
        newhack = hack((player.x, player.y), (x_center, y_center), player.size)
        print('hack activated')
        abilityList.append(newhack)
    elif name == 'backstrike':
        newspacesnipers = many_spacesnipers()
        abilityList.append(newspacesnipers)
    elif name == 'spraybullet':
        sprayBullet = makeShotgun()
        abilityList.append(sprayBullet)
    elif name == 'blackhole':
        blackhole_ability = blackhole()
        abilityList.append(blackhole_ability)
    elif name == 'bomber':
        bomber_ability = makeBomber()
        abilityList.append(bomber_ability)
    mycardorganizer.add_card_to_selection(name)
    
# _______________________________ point organizer______________________________________
def eliminate_with_explosion(object_to_remove, explosion_pos): # pygame rect for position
    if explosion_pos != None:
        newExplosion = ExplosionEffect(explosion_pos)
        explosionList.append(newExplosion)
    enemy_junk_list.remove(object_to_remove)
    player.playerPoints += 2

# _______________________________ player timeline organizer______________________________________
sequence = ['prologue', 'ingame', 'lootbox','ending', 'game_title']
current_sequence = sequence[4] #default is 4
targetScore = 600


prologue_dialogue = [
    f"Welcome aboard, pilot. Your identification code is {random.randint(1000, 9999)}.",
    "You might be wondering — that code serves as your unique identity within our fleet.",
    "As discussed in your briefing, your mission is to help clear the space debris orbiting Earth.",
    "In addition, our research division will occasionally ask for your input regarding operational preferences during cleanup.",
    "These preferences include selecting from advanced weapon modules. Some of this junk can be stubborn — you'll need the firepower.",
    "Use the left mouse button to fire your standard-issue weapon. It's your fallback when no special modules are equipped.",
    "use the key [W,A,S,D] to move left, right, back and front.",
    "You'll also be issued 'cards' — specialized weapons. you will need to click in order to select them as needed.",
    'Use right mouse button to fire the specialized weapons.',
    f"Reach a score of {targetScore}, and you'll qualify for evaluation — where your performance and preferences will be reviewed.",
    "<click anywhere to start the game>",
    f"congratulations pilot, you have reached {targetScore} points, you are now qualified for evaluation.",
    "Evaluation report is given. Your class is considered on how you picked your cards. Thank you for playing."
]

import sys

class makeTween():
    def __init__(self, image, start = None, target = None, tween_speed = 70):
        
        self.tween_speed = tween_speed
        self.image = image
        self.divider = 10
        self.start = pygame.Vector2(windowcenterx - self.image.get_size()[0]//2, 0)
        self.target = pygame.Vector2(windowcenterx - self.image.get_size()[0]//2, windowcentery - self.image.get_size()[1]//2)
        if not (start == None):
            self.start = start
        if not (start == None):
            self.target = target

        self.duration = 2.0  # seconds
        self.elapsed_time = 0.0
        self.current_pos = pygame.Vector2(0,0)
        self.t = 0
    def draw(self):
        self.elapsed_time += clock.get_time() / 1000.0
        self.t = min(self.elapsed_time / self.duration, 1.0)  # Normalize time (0 to 1)

        # Quadratic ease-out formula
        eased_t = self.t * (2 - self.t)
        self.current_pos = self.start + (self.target - self.start) * eased_t

        window.blit(self.image, self.current_pos)

    def reset(self):
        self.elapsed_time = 0.0
        self.current_pos = pygame.Vector2(0,0)

class make_transparency:
    def __init__(self, image, position):
        self.image = image
        self.current_pos = position
        self.alpha = 0  
        self.fade_speed = 5 
        self.fade_direction = 1 
        
    def update_transparency(self):
        # Update alpha based on direction
        self.alpha += self.fade_speed * self.fade_direction
        
        # Clamp alpha between 0 and 255
        self.alpha = max(0, min(255, self.alpha))
        
    def draw(self):
        # Create a copy of the image with current alpha
        temp_surface = self.image.copy()
        temp_surface.set_alpha(int(self.alpha))
        window.blit(temp_surface, self.current_pos)
        
    def fade_in(self):
        self.fade_direction = 1
        
    def fade_out(self):
        self.fade_direction = -1
        
    def is_fade_complete(self):
        return (self.fade_direction == 1 and self.alpha >= 255) or (self.fade_direction == -1 and self.alpha <= 0)

class tweenWide:
    def __init__(self,image, position):
        
        self.start_size_x = 1
        self.variable_size_x = 1
        
        self.image = image
        self.original_size = image.get_size()
        
        self.current_size = pygame.Vector2(self.variable_size_x, image.get_size()[1])
        self.target_size_x = image.get_size()[0]
        
        # Animation timing
        self.duration = 1.0  # seconds
        self.elapsed_time = 0.0
        self.t = 0.0

        self.current_pos = position + pygame.Vector2(image.get_size()[0]//2 - self.start_size_x, 0)
        self.target_pos = position
    
    def draw(self):
        newimage = pygame.transform.scale(self.image, (self.variable_size_x, self.image.get_size()[1]))
        window.blit(newimage, self.current_pos)

    def update(self):
        if self.variable_size_x < self.original_size[0]:
            # Update timing
            self.elapsed_time += clock.get_time() / 1000.0
            self.t = min(self.elapsed_time / self.duration, 1.0)  # Normalize time (0 to 1)
            
            # Cubic ease-in-out formula (starts slow, fast in middle, ends slow)
            if self.t < 0.5:
                eased_t = 4 * self.t * self.t * self.t
            else:
                eased_t = 1 - pow(-2 * self.t + 2, 3) / 2
            
            # Apply easing to size
            self.variable_size_x = self.start_size_x + (self.target_size_x - self.start_size_x) * eased_t
            
            # Update position to keep the image centered as it grows
            self.current_pos.x = self.target_pos.x + (self.original_size[0] - self.variable_size_x) // 2

        

class makeClassification:
    def __init__(self, image):
        
        self.img = image
        self.img = pygame.transform.scale(self.img, (self.img.get_size()[0]//6, self.img.get_size()[1]//6))
        self.targetpos = pygame.Vector2(windowcenterx - self.img.get_size()[0]//2 , 140)
        self.startpos = pygame.Vector2(windowcenterx- self.img.get_size()[0]//2, -self.img.get_size()[1])
        self.tweenClass = makeTween(self.img, target=self.targetpos, start = self.startpos)
        self.transparency = make_transparency(self.img, self.targetpos)

    def update_transparency(self):
        self.transparency.update_transparency()

    def draw(self):
        self.tweenClass.draw()
        self.transparency.draw()

    def reset(self):
        self.tweenClass.reset()
        
        

classification_img = {
    'commander': makeClassification(pygame.image.load('classification/commander.png').convert_alpha()),
    'raycaster': makeClassification(pygame.image.load('classification/raycaster.png').convert_alpha()),
    'hacker': makeClassification(pygame.image.load('classification/hacker.png').convert_alpha()),
    'codewarden': makeClassification(pygame.image.load('classification/codewarden.png').convert_alpha()),
    'spacewarrior': makeClassification(pygame.image.load('classification/spacewarrior.png').convert_alpha()),
    'voidbreaker': makeClassification(pygame.image.load('classification/voidbreaker.png').convert_alpha()),
}


perform_report = pygame.image.load('user_interfaces/perform_report-01.png').convert_alpha()
perform_report = pygame.transform.scale(perform_report, (perform_report.get_size()[0]//12, perform_report.get_size()[1]//12))
#tweensys_perform_report = makeTween(perform_report, target=pygame.Vector2(windowcenterx - perform_report.get_size()[0]//2, 100), start = pygame.Vector2(windowcenterx - perform_report.get_size()[0]//2, -perform_report.get_size()[1] ))
tweensys_perform_report = tweenWide(perform_report, pygame.Vector2(windowcenterx - perform_report.get_size()[0]//2, 100))

exit_sys_ui = pygame.image.load('user_interfaces/exit_sys_ui-01.png').convert_alpha()
exit_sys_ui = pygame.transform.scale(exit_sys_ui, (exit_sys_ui.get_size()[0]//25, exit_sys_ui.get_size()[1]//25))
targetexit = pygame.Vector2(windowcenterx-exit_sys_ui.get_size()[0]//2, y_window-170)
#tweensys_exit_sys_ui = makeTween(exit_sys_ui, target=targetexit, start = pygame.Vector2(windowcenterx-exit_sys_ui.get_size()[0]//2, y_window))
tweensys_exit_sys_ui = make_transparency(exit_sys_ui, targetexit)

exit_prog_text = gothic_font_big.render(f"EXIT PROGRAM", True, (255, 255, 255))
targetexitprog = pygame.Vector2(windowcenterx - exit_prog_text.get_size()[0]//2, y_window-150)

#tweensys_exit_prog_text = makeTween(exit_prog_text, target=targetexitprog, start = pygame.Vector2(windowcenterx- exit_prog_text.get_size()[0]//2, y_window))
tweensys_exit_prog_text = make_transparency(exit_prog_text, targetexitprog)

classified_text = gothic_font_big.render(f"CLASSIFIED AS...", True, (255, 255, 255))
classified_text_pos = pygame.Vector2(windowcenterx- classified_text.get_size()[0]//2, 110)
#tweensys_classified_text = makeTween(classified_text, target=classified_text_pos, start = pygame.Vector2(windowcenterx- classified_text.get_size()[0]//2, -classified_text.get_size()[1]))
tweensys_classified_text = make_transparency(classified_text, classified_text_pos)

leftclickguide = pygame.image.load('user_interfaces/left_click_guide.png').convert_alpha()
leftclickguide = pygame.transform.scale(leftclickguide, (leftclickguide.get_size()[0]//3, leftclickguide.get_size()[1]//3))
tweensys_leftclickguide = makeTween(leftclickguide)

rightclickguide = pygame.image.load('user_interfaces/right_click_guide.png').convert_alpha()
rightclickguide = pygame.transform.scale(rightclickguide, (rightclickguide.get_size()[0]//3, rightclickguide.get_size()[1]//3))
tweensys_rightclickguide = makeTween(rightclickguide)

arrow_key_guide = pygame.image.load('user_interfaces/arrow_key_guide.png').convert_alpha()
arrow_key_guide = pygame.transform.scale(arrow_key_guide, (arrow_key_guide.get_size()[0]//3, arrow_key_guide.get_size()[1]//3))
tweensys_arrow_key_guide = makeTween(arrow_key_guide)

lootboxguide = pygame.image.load('user_interfaces/lootbox_guide.png').convert_alpha()
lootboxguide = pygame.transform.scale(lootboxguide, (lootboxguide.get_size()[0]//3, lootboxguide.get_size()[1]//3))
tweensys_lootboxguide = makeTween(lootboxguide)

dialogue_index = 0
char_index = 0
type_speed = 2
frame_counter = 0
waiting_for_click = False
if current_sequence == sequence[3]:
    dialogue_index = 11

def wrap_text_by_words(text, max_words_per_line=10):
    """Splits text into multiple lines with at most `max_words_per_line` words per line"""
    words = text.split()
    lines = []
    for i in range(0, len(words), max_words_per_line):
        line = " ".join(words[i:i+max_words_per_line])
        lines.append(line)
    return lines

def draw_text(surface, text_lines, pos, max_chars):
    """Draws multiple lines with typewriter effect"""
    x, y = pos
    chars_drawn = 0
    for line in text_lines:
        # Only draw up to max_chars total
        if chars_drawn + len(line) <= max_chars:
            visible_line = line
            chars_drawn += len(line)
        else:
            visible_line = line[:max_chars - chars_drawn]
            chars_drawn = max_chars
        rendered = arcade_font.render(visible_line, True, (255, 255, 255))
        surface.blit(rendered, (x, y))
        y += arcade_font.get_height()+10

# Create a transparent surface for the bottom gradient
gradient_height = int(y_window)
gradient_surface = pygame.Surface((x_window, gradient_height), pygame.SRCALPHA)


# Draw a top-to-bottom black gradient (fades to black)
for y in range(gradient_height):
    alpha = int(255 * (y / gradient_height))  # Fully transparent to fully black
    pygame.draw.line(gradient_surface, (0, 0, 0, alpha), (0, y), (int(x_window), y))



#_________________________fade to black_______________________________________________________

class FadeTransition:
    def __init__(self, screen_size, speed=3):
        self.surface = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.alpha = 0
        self.speed = speed
        self.mode = None  # 'in' or 'out'
        self.done = True

    def start_fade_in(self):
        self.mode = 'in'
        self.alpha = 255
        self.done = False

    def start_fade_out(self):
        self.mode = 'out'
        self.alpha = 0
        self.done = False

    def update(self):
        if self.done or self.mode is None:
            return

        if self.mode == 'in':
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.done = True

        elif self.mode == 'out':
            self.alpha += self.speed
            if self.alpha >= 100:
                self.alpha = 100
                self.done = True

        self.surface.fill((0, 0, 0, self.alpha))

    def draw(self, target_surface):
        target_surface.blit(self.surface, (0, 0))

    def is_done(self):
        return self.done
    
fade = FadeTransition(window.get_size(), speed=4)

def enablefade_once(mode):
    if mode == 'out' and fade.mode != 'out':
        fade.start_fade_out()
    if mode == 'in' and fade.mode != 'in':
        fade.start_fade_in()

#_____________________________lootbox frame__________________________________________________
class lootbox:
    def __init__(self):
        self.pygamecountermilisecs = pygame.time.get_ticks()
        self.lootboxFrameCounter = 0
        self.continueCounterlootbox = True
        self.lootboxcounter_const = 11
        self.lootboxCounterInSeconds = 11
        self.lootboxCountdown = 6
        self.enableCountdown = True 
        self.openingLootbox = False

        self.randomCardnames = []
        

lootbox_sys = lootbox()

lootbox_closedImg = pygame.image.load('user_interfaces/boxclosed_isometric.png')
lootbox_closedImg = pygame.transform.scale(lootbox_closedImg, (lootbox_closedImg.get_size()[0]//2.5, lootbox_closedImg.get_size()[1]//2.5))
endlootbox_pos = pygame.Vector2(windowcenterx - lootbox_closedImg.get_size()[0]/2, y_window- 200)
lootboxtween = makeTween(lootbox_closedImg, tween_speed =-70, start = pygame.Vector2(windowcenterx - lootbox_closedImg.get_size()[0]/2, y_window), target = endlootbox_pos)

lootbox_openImg = pygame.image.load('user_interfaces/box_open.png')
lootbox_openImg = pygame.transform.scale(lootbox_openImg, (lootbox_openImg.get_size()[0]//24, lootbox_openImg.get_size()[1]//24))

pick_card_text = arcade_font.render(f"pick a card!", True, (255, 255, 255))


#cards


class makeCard:
    def __init__(self, image, desc='', title='', subtitle=''):
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]//20, self.image.get_size()[1]//20))
        self.tweenClass = None
        self.desc = desc
        self.title = title
        self.subtitle = subtitle
        self.split_text_desc = self.desc.split(' ')
        self.amount_line_desc = 0

        self.desc_seplines = []
        self.splitTextIntoLines()
        self.descRender_sepLines = []


    def splitTextIntoLines(self):
        self.desc_seplines = []
        limit = 4
        if len(self.split_text_desc) > limit:   
            self.amount_line_desc = (len(self.split_text_desc) // limit) + 1
            for line in range(self.amount_line_desc):
                oneline = ' '.join(self.split_text_desc[line * limit: (line + 1) * limit])
                self.desc_seplines.append(oneline)
        else:
            self.desc_seplines.append(self.desc)
        
    def drawtext(self, cardcenterpos):
        for index, text in enumerate(self.desc_seplines):
            wordline_render = gothic_font_small.render(f"{text}", True, (255, 255, 255))
            width,height = gothic_font_small.size(text)
            window.blit(wordline_render, (cardcenterpos[0] - width/2, cardcenterpos[1] + 100 + 8* (index+1)))

        title_render = gothic_font_big.render(f"{self.title}", True, (255, 255, 255))
        title_render_sizex, title_render_sizey = gothic_font_big.size(self.title)
        window.blit(title_render, (cardcenterpos[0] - title_render_sizex/2, cardcenterpos[1] - 130))

        subtitle_render = gothic_font_medium.render(f"{self.subtitle}", True, (125, 125, 125))
        subtitle_render_sizex, subtitle_render_sizey = gothic_font_medium.size(self.subtitle)
        window.blit(subtitle_render, (cardcenterpos[0] - subtitle_render_sizex/2, cardcenterpos[1] - 100))



cardsList = { # pygame_image, start = None, target = None, tween_speed = 70, direct= 'down'
    'backstrike': makeCard(pygame.image.load("cards_images/backStrike_commander_card_plain.png").convert_alpha(),
                           desc='Once activated, two additional spaceships will appear on your right sideto clear nearby space debris',
                           title='BACK-UP STRIKE',
                           subtitle='COMMANDER'),
    'laser': makeCard(pygame.image.load('cards_images/blaster_laser_card_plain.png').convert_alpha(), 
                      desc='As soon as active, spaceship will generate a deadly light blue orb and lauch a laser. Will obliterate any anomalies according to mouse movement',
                      title='BLASTER', 
                      subtitle='RAYCASTER'),
    'disruption': makeCard(pygame.image.load('cards_images/hacker_disrupt_card_plain.png').convert_alpha(),
                           desc= 'As soon as active, space ship will emit disruption which will suspend any anomalies for seconds',
                           title='DISRUPTION',
                           subtitle='HACKER'),
    'spraybullet': makeCard(
        pygame.image.load('cards_images/shotgun_card.png').convert_alpha(),
        desc='Unleash a burst of piercing light blue projectiles in all directions with a single right click.',
        title='SHARD VOLLEY',
        subtitle='RAYCASTER'
    ),
    'blackhole': makeCard(
        pygame.image.load('cards_images/blackhole_card.png').convert_alpha(),
        desc='As soon as active, space ship will emit a black hole at a random location that will pull nearby anomalies towards it.',
        title='BLACK HOLE',
        subtitle='HACKER'
    ),
    'bomber': makeCard(
        pygame.image.load('cards_images/bomber_card.png').convert_alpha(),
        desc='When activated, deploys a bomber spaceship that flies across the space, dropping powerful space bombs to clear out anomalies in its path.',
        title='BOMBER',
        subtitle='COMMANDER'

    )
}

gleamcard = pygame.image.load('user_interfaces/gleamforcard.png').convert_alpha()
gleamcard= pygame.transform.scale(gleamcard, (gleamcard.get_size()[0]//19, gleamcard.get_size()[1]//19))

def get_card(name_given):
    for cardname, object in cardsList.items():
        if cardname == name_given:
            return cardsList[cardname]


ability_icons = {}

for cardname, object in cardsList.items():
    ability_icons[cardname] = pygame.image.load(f'card_queue_logos/{cardname}-01.png').convert_alpha()
    ability_icons[cardname] = pygame.transform.scale(ability_icons[cardname], (ability_icons[cardname].get_size()[0]//14, ability_icons[cardname].get_size()[1]//14))


from collections import Counter



class card_organizer:
    def __init__(self):
        
        self.alreadyorganized = False
        self.alreadygetcard_withmaxamount = False
        self.max_classification = None
        self.players_card_selection = [] #['bomber', 'laser']
        self.players_card_selection_grouping = {} # ['bomber':2, 'laser':3]
        self.players_card_selection_grouping_sorted = {}


        self.player_card_classification_selection = [] # ['commander', 'hacker']
        self.card_classification_amount = {} #{'a': 3, 'b': 3, 'c': 1}
        self.sorted_card_classification_amount = {}
        self.card_classification_amount_max = [] #['a', 'b']


    def organize_card_selection_once(self):
        if self.alreadyorganized:
            return
        self.alreadyorganized = True
        for cardname in self.players_card_selection:
            self.player_card_classification_selection.append(cardsList[cardname].subtitle)
        
        data = Counter(self.player_card_classification_selection)
        self.card_classification_amount = {item: count for item, count in data.items() if count >= 1}
        max_count = max(self.card_classification_amount.values())
        self.card_classification_amount_max = [item for item, count in self.card_classification_amount.items() if count == max_count]

        data_2 = Counter(self.players_card_selection)
        self.players_card_selection_grouping = {item: count for item, count in data_2.items() if count >= 1}
        
    
    def add_card_to_selection(self, cardname):
        self.players_card_selection.append(cardname)

    def sort_card_selection(self):
        self.sorted_card_classification_amount = dict(sorted(self.card_classification_amount.items(), key=lambda item : item[1], reverse = True))
        self.players_card_selection_grouping_sorted = dict(sorted(self.players_card_selection_grouping.items(), key=lambda item : item[1], reverse = True))
mycardorganizer = card_organizer()

anime_images = [pygame.image.load(f'user_interfaces/anime_general{j+1}.png').convert_alpha() for j in range(2)]
anime_images = [pygame.transform.scale(anime, (anime.get_size()[0]//6, anime.get_size()[1]//6)) for anime in anime_images]
randomChar = anime_images[1]

#______________________________notif system______________________________________________

class create_text:
    def __init__(self, text, color_rgb=(255,255,255)):
        self.text = text
        self.color_rgb = (255, 255, 224)
        self.duration = 100

class createNotif_system:
    def __init__(self):
        self.queue = []

    def addtext_to_queue(self, the_text, color_rgb=(255,255,255)):
        self.queue.append(create_text(the_text, color_rgb))

    def draw(self):
        for index, object in enumerate(self.queue):
            notif_text = arcade_font.render(object.text, True, object.color_rgb)
            window.blit(notif_text, (windowcenterx - notif_text.get_size()[0]//2, 100 + (index * 20)))
            if object.duration > 0:
                object.duration -= 1
            else:
                self.queue.remove(object)



notif_sys = createNotif_system()

#_______________________________run_________________________________________________________
right_click_triggered = False
run = True
while run:
    #pygame.time.delay(waitsec) #.1 second, 100 milisec
    dt = clock.tick(60)
    
    # mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    

    # center spaceship coords
    x_center = player.x + (ship_faces[1].get_size()[0]/2) 
    y_center = player.y + (ship_faces[1].get_size()[1]/2)
    
    # loading spaceship images
    image_center = pygame.Vector2(x_center, y_center)

    # Calculate angle from image center to mouse
    dx = mouse_x - image_center.x
    dy = mouse_y - image_center.y
    angle = -math.degrees(math.atan2(dy, dx))  # Negative for clockwise correction


    for event in pygame.event.get(): #getting list of all event that happens, have to be looped
        if event.type == pygame.QUIT: # Xbutton is pressed: break the while loop
            run = False
        if event.type == pygame.KEYDOWN and current_sequence == sequence[1]:
            if event.key == pygame.K_g:
                insertability('laser')
                
            elif event.key == pygame.K_h:
                insertability('disruption')
            elif event.key == pygame.K_j:
                insertability('backstrike')
            elif event.key == pygame.K_k:
                insertability('spraybullet')
            elif event.key == pygame.K_l:
                insertability('blackhole')
            elif event.key == pygame.K_m:
                insertability('bomber')
                    
            if event.key == pygame.K_p:
                print('all abilities deactivated')
                for ability in abilityList:
                    abilityList.remove(ability)

    #__________________________________key systems______________________________
    keys = pygame.key.get_pressed() # if key is hold
    mousepress = pygame.mouse.get_pressed()

    # keyboard trigger for moving spaceship

    if player.x > 0:
        player.x -= player.vel_left
    else:
        player.x = 0 # prevent player from moving left

    # WASD movement instead of arrow keys

    # Move left (A)
    if keys[pygame.K_a] and current_sequence == sequence[1]:
        if player.vel_left < 10:
            player.vel_left += 1
        else:
            player.vel_left = 10
    else:
        if player.vel_left > 0:
            player.vel_left -= .2
        else:
            player.vel_left = 0

    if player.x < x_window - player.size[0]:
        player.x += player.vel_right
    else:
        player.x = x_window - player.size[0] # prevent player from moving right

    # Move right (D)
    if keys[pygame.K_d] and current_sequence == sequence[1]:
        if player.vel_right < 10:
            player.vel_right += 1
        else:
            player.vel_right = 10
    else:
        if player.vel_right > 0:
            player.vel_right -= .2
        else:
            player.vel_right = 0

    if player.y > 0:
        player.y -= player.vel_up
    else:
        player.y = 0 # prevent player from moving up

    # Move up (W)
    if keys[pygame.K_w] and current_sequence == sequence[1]:
        if player.vel_up < 10:
            player.vel_up += 1
        else:
            player.vel_up = 10
    else:
        if player.vel_up > 0:
            player.vel_up -= .2
        else:
            player.vel_up = 0

    if player.y < y_window - player.size[1]:
        player.y += player.vel_down
    else:
        player.y = y_window - player.size[1] # prevent player from moving down

    # Move down (S)
    if keys[pygame.K_s] and current_sequence == sequence[1]:
        if player.vel_down < 10:
            player.vel_down += 1
        else:
            player.vel_down = 10
    else:
        if player.vel_down > 0:
            player.vel_down -= .2
        else:
            player.vel_down = 0


    #PUT DRAWINGS BELOW TISSS ----------------------------------------------------------------
    window.blit(resized_image_spacebg, (0,0)) 
                    
    #_______________________________bullet mechanism_____________________________
    player_pos = pygame.Vector2(x_center, y_center)
    mouse_pos = pygame.mouse.get_pos()

    # shooting trigger
    if mousepress[0] and current_sequence == sequence[1]:
        if clickFire:
            clickFire = False
            
            
            bullet = Bullet(player_pos, mouse_pos, 10, (8,4))
            bullets.append(bullet)
        

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(window)
        if bullet.is_off_screen():
            bullets.remove(bullet)

    #gun Click debouce
    if not clickFire:
        clickFireCounter += 1
        if clickFireCounter % 20 == 0:
            clickFireCounter = 0
            clickFire = True
    #_______________________________shotgun mechanism_____________________________
    
    if check_ability_front('spraybullet'):
        sprayBullet = get_ability_front('spraybullet')

        if mousepress[2] and sprayBullet.usage > 0 and current_sequence == sequence[1]:
            if sprayBullet.notif_toggle == False:
                notif_sys.addtext_to_queue(f'[ability: {sprayBullet.card_name} activated!]')
                sprayBullet.notif_toggle = True

            if sprayBullet.clickFire:
                sprayBullet.clickFire = False
                mousepos = pygame.mouse.get_pos()
                for j in range(5):
                    sprayBullet.bulletobjects.append(shotgun(player_pos, mousepos, speed=10))

                sprayBullet.usage -= 1

        if sprayBullet.usage == 0:
            if len(sprayBullet.bulletobjects) == 0:
                clean_ability_front()         
        
        for bullet in sprayBullet.bulletobjects:
            if current_sequence == sequence[1]:
                bullet.update()
            bullet.draw(window)
            if bullet.is_off_screen():
                sprayBullet.bulletobjects.remove(bullet)

        if not sprayBullet.clickFire:
            sprayBullet.clickFireCounter += 1
            if sprayBullet.clickFireCounter % 20 == 0:
                #print(sprayBullet.clickFireCounter)

                sprayBullet.clickFireCounter = 0
                sprayBullet.clickFire = True

        # collusion
        for bullet in sprayBullet.bulletobjects: 
            topleftCoord_bullet = bullet.rect.topleft
            for junk in enemy_junk_list:
                topleftCoord_junk = junk.rect.topleft
                if (topleftCoord_junk[1] <= topleftCoord_bullet[1] <= topleftCoord_junk[1] + debrisSize[1]) and (topleftCoord_junk[0] <= topleftCoord_bullet[0] <= topleftCoord_junk[0] + debrisSize[0]):
                    
                    eliminate_with_explosion(junk, topleftCoord_junk)
                    if bullet in sprayBullet.bulletobjects:
                        sprayBullet.bulletobjects.remove(bullet)

    #____________________________game title_____________________________
    if current_sequence == sequence[4]:
        window.blit(game_title_image, (windowcenterx - game_title_image.get_size()[0]/2, 170))
        window.blit(creator_text, (windowcenterx - creator_text.get_size()[0]/2, 340))
        
        #pygame.draw.rect(window, (0, 183, 235), (click_to_play_text.get_rect().topleft[0], click_to_play_text.get_rect().topleft[1], click_to_play_text.get_size()[0], click_to_play_text.get_size()[1]))
        if (windowcenterx - click_to_play_text.get_size()[0]/2 <= mouse_x <=windowcenterx + click_to_play_text.get_size()[0]/2 and 
            400 <= mouse_y <= 400 + click_to_play_text.get_size()[1]):
            
            click_to_play_text = gothic_font_big.render('<NEW GAME>', True, (0, 183, 235))
            window.blit(click_to_play_text, (windowcenterx - click_to_play_text.get_size()[0]/2, 400))
            if mousepress[0]:
                current_sequence = sequence[0]
        else:
            click_to_play_text = gothic_font_big.render('<NEW GAME>', True, (255, 255, 255))
            window.blit(click_to_play_text, (windowcenterx - click_to_play_text.get_size()[0]/2, 400))

    #_______________________________other stuff_____________________________

    # get distance of enemy: junk
    for iterated_enemy_junk in enemy_junk_list:
        iterated_enemy_junk.distanceFromplayer_x = iterated_enemy_junk.rect.centerx - x_center
        iterated_enemy_junk.distanceFromplayer_y = iterated_enemy_junk.rect.centery - y_center
    # enemies
    enemydebounceCounter += 1
    if current_sequence != sequence[1]:
        enemydebounceCounter = 1
    if enemydebounceCounter % 20 == 0:
        enemydebounceCounter == 0
        newjunk_enemy = Enemy((x_center, y_center), x_window, y_window)
        enemy_junk_list.append(newjunk_enemy)
    
    for enemy_junk in enemy_junk_list:
        enemy_junk.draw(window)

        if current_sequence == sequence[1]:
            enemy_junk.update()
            if enemy_junk.lifespanCounter >= enemy_junk.lifespanEnd:
                enemy_junk_list.remove(enemy_junk)

    #enemy collusion with bullet
    for bullet in bullets:
        topleftCoord_bullet = bullet.rect.topleft
        for junk in enemy_junk_list:
            topleftCoord_junk = junk.rect.topleft
            if (topleftCoord_junk[1] <= topleftCoord_bullet[1] <= topleftCoord_junk[1] + debrisSize[1]) and (topleftCoord_junk[0] <= topleftCoord_bullet[0] <= topleftCoord_junk[0] + debrisSize[0]):
                
                eliminate_with_explosion(junk, junk.rect.topleft)
                if bullet in bullets:
                    bullets.remove(bullet)

    

    # explosion drawing
    for expl in explosionList:
        expl.draw(window)
        if expl.imageIteration == 10:
            explosionList.remove(expl)

    # collusion with plr
    for junk in enemy_junk_list:
        topleftCoord_junk = junk.rect.topleft
        centerCoord_junk = (junk.rect.topleft[0] + debrisSize[0]/2, junk.rect.topleft[1] + debrisSize[1]/2)
        if player.x <= centerCoord_junk[0] <= player.x + width and  player.y<= centerCoord_junk[1] <= player.y + height and playerCollusion == False:
            playerCollusion = True
            player.vel_right += random.choice([-10, 10]) 
            player.vel_down += random.choice([-10,10])



    if player.vel_up > 0 or player.vel_down > 0 or player.vel_left > 0 or player.vel_right > 0:
        player.face = ship_faces[0]
    else:
        player.face  = ship_faces[1]

    # Rotate the image
    rotated_image = pygame.transform.rotate(player.face.convert_alpha(), angle)
    rotated_rect = rotated_image.get_rect(center=image_center)

    # Draw the rotated image
    window.blit(rotated_image, rotated_rect)

    if playerCollusion == True:
        forcefieldcounter += 1
        if forcefieldcounter % 30 < 10:
            rotated_face_effect = pygame.transform.rotate(player.C_effect_face.convert_alpha(), angle)
            rotated_rect_face_effect = rotated_face_effect.get_rect(center=image_center)
            window.blit(rotated_face_effect, rotated_rect_face_effect)

        if forcefieldcounter >= 100:
            forcefieldcounter=0
            playerCollusion = False


    #--------------------------------laser ability-----------------------------------------------
    if check_ability_front('laser'):

        laserability = get_ability_front('laser')
        
        
        if mousepress[2] and not (laserability.activated):
            if laserability.usage > 0:
                notif_sys.addtext_to_queue(f'[ability: {laserability.card_name} activated!]')
                laserability.charge = True
                laserability.activated = True
                laserability.usage -= 1

        
        #calculation to rotate the laser
        if current_sequence == sequence[1]:
            laserability.angle_rad = math.atan2(dy, dx)
            laserability.angle_deg = -math.degrees(laserability.angle_rad)  # negative to rotate correctly
            # slope for hitbox
            
            if dx != 0:
                laserability.slope = dy/dx

        def get_orbitpos(image_radius):
            
            # position according to radius
            offset_x = math.cos(laserability.angle_rad) * image_radius
            offset_y = math.sin(laserability.angle_rad) * image_radius
            orbit_pos = image_center + pygame.Vector2(offset_x, offset_y)
            return orbit_pos


        if laserability.shoot == False:
            # making laser load
            for img in laserability.laserList:
                img.set_alpha(255)
            laserability.lasetransparencyCounter = 255
            laserability.laserFrameCount = 0

            image_radius = laserability.laserload_img.get_size()[0]/2 # distance from center
            orbit_pos = get_orbitpos(image_radius)

            # Rotate the image
            rotated_image = pygame.transform.rotate(laserability.laserload_img, laserability.angle_deg)
            rotated_rect = rotated_image.get_rect(center=orbit_pos)

            
            # Draw rotated image at offset position
            window.blit(rotated_image, rotated_rect)

            if laserability.charge: 
                image_radius = laserability.chargeimg.get_size()[0]/2 # distance from center
                orbit_pos = get_orbitpos(image_radius)

                # random rotate charge image
                rotated_chargeimage = pygame.transform.rotate(laserability.chargeimg, random.randint(0, 360))
                rotated_chargeimage_rect = rotated_chargeimage.get_rect(center=orbit_pos)

                # Draw rotated image at offset position
                window.blit(rotated_chargeimage, rotated_chargeimage_rect)

                if current_sequence == sequence[1]:
                    laserability.chargeFrameCount += 1

                if laserability.chargeFrameCount > 100:
                    laserability.chargeFrameCount = 0
                    laserability.charge = False
                    laserability.shoot = True

        elif laserability.shoot ==True:
            # iterating the laser img
            if laserability.laserFrameCount % 3 == 0:
                laserImg = laserability.laserList[0]
            elif laserability.laserFrameCount % 2 == 0:
                laserImg = laserability.laserList[1]
            elif laserability.laserFrameCount % 1 == 0:
                laserImg = laserability.laserList[2]

            image_radius = laserImg.get_size()[0]/2
            orbit_pos = get_orbitpos(image_radius)

            # Rotate the image
            rotated_image = pygame.transform.rotate(laserImg, laserability.angle_deg)
            rotated_rect = rotated_image.get_rect(center=orbit_pos)
            
            # signalling when to activate the transparency
            if laserability.laserFrameCount > 100:
                laserImg.set_alpha(laserability.lasetransparencyCounter)
                if laserability.lasetransparencyCounter > 0:
                    laserability.lasetransparencyCounter -= 1
                else:
                    laserability.shoot = False
                    laserability.charge = False
                    laserability.activated = False
                    if laserability.usage == 0 :
                        clean_ability_front()

            
            # mecha
            for iterated_enemy in enemy_junk_list:
                if (iterated_enemy.distanceFromplayer_y >= laserability.slope * iterated_enemy.distanceFromplayer_x - 50 and iterated_enemy.distanceFromplayer_y <= laserability.slope * iterated_enemy.distanceFromplayer_x + 50):
                    if (iterated_enemy.distanceFromplayer_y < 0 and iterated_enemy.distanceFromplayer_x > 0) and (dy < 0 and dx > 0):
                        eliminate_with_explosion(iterated_enemy, iterated_enemy.rect)
                        
                    elif (iterated_enemy.distanceFromplayer_y > 0 and iterated_enemy.distanceFromplayer_x < 0) and (dy > 0 and dx < 0):
                        eliminate_with_explosion(iterated_enemy, iterated_enemy.rect)
                    elif (iterated_enemy.distanceFromplayer_y > 0 and iterated_enemy.distanceFromplayer_x > 0) and (dy > 0 and dx > 0):
                        eliminate_with_explosion(iterated_enemy, iterated_enemy.rect)
                    elif (iterated_enemy.distanceFromplayer_y < 0 and iterated_enemy.distanceFromplayer_x < 0) and (dy < 0 and dx < 0):
                        eliminate_with_explosion(iterated_enemy, iterated_enemy.rect)

            # Draw rotated image at offset position
            window.blit(rotated_image, rotated_rect)

            # iterate laser grame
            if current_sequence == sequence[1]:
                laserability.laserFrameCount += 1

    if check_ability_front('hack'):
        hackability = get_ability_front('hack')
        

        if mousepress[2] and not hackability.activate:
            if hackability.usage >0:
                notif_sys.addtext_to_queue(f'[ability: {hackability.card_name} activated!]')
                hackability.activate = True
                hackability.usage -= 1
            

        if hackability.activate and hackability.activationCounter < 120:
            

            if current_sequence == sequence[1]:
                hackability.increase_size((x_center, y_center))
                
                hackability.activationCounter += 1

                max_radius = hackability.base_radius + hackability.radius_gap * (hackability.num_circles - 1)

                for enemies_junk in enemy_junk_list:
                    dist = hackability.centerpos.distance_to(enemies_junk.rect.center)

                    if dist <= max_radius:
                        if not (enemies_junk in hackability.enemiesinBound):
                            hackability.enemiesinBound[enemies_junk] = 0 # glitch duration counter
                            pass # enemies that included
            hackability.draw()

        if hackability.activationCounter >= 120:
            hackability.activationCounter = 0
            hackability.base_radius = 40
            hackability.spawndb = False
            hackability.activate = False
            if hackability.usage == 0:
                
                clean_ability_front()
            #hackability.enemiesinBound = []


        enemiestoDelete = []
        if current_sequence == sequence[1]:
            for enemies, glitch_counter in hackability.enemiesinBound.items():
                
                if glitch_counter >= 150 or not (enemies in enemy_junk_list):
                    
                    enemies.unfreeze()
                    enemiestoDelete.append(enemies)
                elif glitch_counter < 150:
                    hackability.draw_glitch(enemies.rect)
                    enemies.freeze()
                    hackability.enemiesinBound[enemies] += 1
  
        for enemies in enemiestoDelete:
            del hackability.enemiesinBound[enemies]
            enemiestoDelete.remove(enemies)
    else:
        for enemy in enemy_junk_list:
            enemy.unfreeze()

    def iterate_spacesniper_operation(spacesniperAbility):
        if spacesniperAbility.spawnEnabled == False:
                
                if current_sequence == sequence[1]:
                    spacesniperAbility.update() # flying false? No
                spacesniperAbility.draw()
                
        if spacesniperAbility.pilot_one.flying == False and spacesniperAbility.pilot_two.flying == False and spacesniperAbility.spawnEnabled == False: 
            spacesniperAbility.spawnEnabled = True
            #print('pilots are landed, ending spaceship ability')

    if check_ability_front('manyspacesnipers'):
        spacesniperAbility = get_ability_front('manyspacesnipers') 
        if spacesniperAbility.usage == 0:
            remaining_abilityList.append(spacesniperAbility)
            
            
            clean_ability_front()
        if mousepress[2]:
            if spacesniperAbility.spawnEnabled == True :
                if spacesniperAbility.usage > 0:
                    notif_sys.addtext_to_queue(f'[ability: {spacesniperAbility.card_name} activated!]')
                    spacesniperAbility.spawnEnabled = False
                    spacesniperAbility.reset()
                    spacesniperAbility.usage -= 1
                
        iterate_spacesniper_operation(spacesniperAbility)

    def iterate_blackholearmy_operation(blackholeAbility):
        for army in blackholeAbility.blackholeobject:
            army.update()
            army.draw()
            
            if current_sequence == sequence[1]:
                if army.lifespan_counter >= army.lifespan:
                    army.lifespan_counter = army.lifespan
                    if army.is_shrinking == False:
                        army.start_shrink()
                else:
                    army.lifespan_counter += 1

                if army.shrink_progress >= 1.0:
                    blackholeAbility.blackholeobject.remove(army)
                    print('black hole removed')

                if army.imageiterationCounter*3 >= 12:
                    newparticle = blackhole_particle(army.absorbtion_center)
                    army.particleobject.append(newparticle)
                    

                for particle in army.particleobject:
                    particle.update(army.absorbtion_center)
                    particle.draw()

                    if particle.t >= 1.0:
                        army.particleobject.remove(particle)

                
                for enemy in enemy_junk_list:
                    if army.centerforhitbox.x - 150 <= enemy.rect.center[0] <= army.centerforhitbox.x + 150 and army.centerforhitbox.y - 150 <= enemy.rect.center[1] <= army.centerforhitbox.y + 150:
                        d = army.centerforhitbox - enemy.rect.center 
                        if d != pygame.Vector2(0,0):
                            enemy.direction = d
                            enemy.speed += 0.01
                        if army.centerforhitbox.x - 50 <= enemy.rect.center[0] <= army.centerforhitbox.x+50 and army.centerforhitbox.y - 50 <= enemy.rect.center[1] <= army.centerforhitbox.y +50 :
                            eliminate_with_explosion(enemy, None)

    if check_ability_front('blackhole'):
        blackholeAbility = get_ability_front('blackhole')
        if blackholeAbility.usage == 0:
            remaining_abilityList.append(blackholeAbility)
            
            clean_ability_front()

        if mousepress[2] and current_sequence == sequence[1]:

            time_now = pygame.time.get_ticks() // 1000
            
            if blackholeAbility.spawnDebounce and blackholeAbility.usage > 0:
                blackholeAbility.time_earlier = time_now
                notif_sys.addtext_to_queue(f'[ability: {blackholeAbility.card_name} activated!]')
                newblackHole = blackhole_army(player_pos, pygame.Vector2(random.randint(0, x_window), random.randint(0, y_window)))
                blackholeAbility.blackholeobject.append(newblackHole)
                #print('new black hole spawned')
                blackholeAbility.spawnDebounce = False
                blackholeAbility.usage -= 1


        if not blackholeAbility.spawnDebounce:
            if time_now - blackholeAbility.time_earlier >= 1:
                blackholeAbility.spawnDebounce = True
                #print('spawn debounce reset')

        iterate_blackholearmy_operation(blackholeAbility)

    def iterate_bomber_operation(ability):
        bomberAbility = ability
        # Clean up off-screen bombers
        bombers_to_remove = []
        for bomber_object in bomberAbility.bomberobject:
            if current_sequence == sequence[1]:
                bomber_object.update()
            bomber_object.draw(window)

            # Clean up completed bombs
            bombs_to_remove = []
            for spacebomb_object in bomber_object.bomb_storage:

                if current_sequence == sequence[1]:
                    spacebomb_object.update()
                spacebomb_object.draw()

                if spacebomb_object.done and not (spacebomb_object.explosion_done):
                    for enemy in enemy_junk_list:
                        if spacebomb_object.rect.topleft[0] - 200 <= enemy.rect.topleft[0] <= spacebomb_object.rect.topleft[0] + 200 and spacebomb_object.rect.topleft[1] - 200 <= enemy.rect.topleft[1] <= spacebomb_object.rect.topleft[1] + 200:
                            eliminate_with_explosion(enemy, None)
                
                # Mark bombs for removal if explosion is done
                if spacebomb_object.explosion_done:
                    bombs_to_remove.append(spacebomb_object)
            
            # Remove completed bombs and clean up their resources
            for bomb in bombs_to_remove:
                bomb.cleanup()
                bomber_object.bomb_storage.remove(bomb)
            
            # Mark bombers for removal if off-screen
            if bomber_object.is_off_screen():
                bombers_to_remove.append(bomber_object)
        
        # Remove off-screen bombers and clean up their resources
        for bomber in bombers_to_remove:
            bomber.cleanup()
            bomberAbility.bomberobject.remove(bomber)

    if check_ability_front('bomber'):
        bomberAbility = get_ability_front('bomber')
        if bomberAbility.usage == 0:
            remaining_abilityList.append(bomberAbility)
            print('bomber ability migrated to remaining ability list')
            clean_ability_front()

        if mousepress[2] and current_sequence == sequence[1]:
            current_time = pygame.time.get_ticks() // 1000
            if bomberAbility.usage > 0 and bomberAbility.spawnDebounce:
                bomberAbility.usage -= 1
                newBomber = bomber()
                bomberAbility.bomberobject.append(newBomber)
                bomberAbility.last_spawn_time = current_time
                
                bomberAbility.spawnDebounce = False

        if not bomberAbility.spawnDebounce:
            if current_time - bomberAbility.last_spawn_time >= 3:
                bomberAbility.spawnDebounce = True

        iterate_bomber_operation(bomberAbility)
                            

    #__________________________________ability that remains _________________________________
    for ability in remaining_abilityList:
        if ability.name == 'manyspacesnipers':
            spacesniperAbility = ability
            iterate_spacesniper_operation(spacesniperAbility)

            if spacesniperAbility.spawnEnabled == True:
                remaining_abilityList.remove(spacesniperAbility)
               # print('spaceship ability removed from remaining ability list')

        if ability.name == 'blackhole':
            blackholeAbility = ability
            iterate_blackholearmy_operation(blackholeAbility)
            if len(blackholeAbility.blackholeobject) == 0:
                remaining_abilityList.remove(blackholeAbility)
                #print('black hole ability removed from remaining ability list')
            
        if ability.name == 'bomber':
            bomberAbility = ability
            iterate_bomber_operation(bomberAbility)
            # Clean up if no more bombers
            if len(bomberAbility.bomberobject) == 0:
                bomberAbility.cleanup()
                remaining_abilityList.remove(bomberAbility)
                print('bomber ability removed from remaining ability list')
    
     #_____________________________power up display queue_____________________________
    
    for index, object in enumerate(abilityList):
        cardicon = ability_icons[object.card_name]
        cardicon_topleft = (20 + (cardicon.get_size()[0] + 10) * index, y_window - cardicon.get_size()[1] - 10)
        window.blit(cardicon, cardicon_topleft)
        usage_displayer = arcade_font_small.render(f"x{object.usage}", True, (255, 255, 255))
        window.blit(usage_displayer, (cardicon_topleft[0]+ 15, cardicon_topleft[1] - 17))

    # -----------------------------------score displayer--------------------------------------- 
    scoreFont_render = arcade_font.render(f"score: {player.playerPoints}", True, (255, 255, 255))
    
    window.blit(scoreFont_render, (20, 20))
    


    #__________________________________player timeline system___________________
    if player.playerPoints >= targetScore and not (current_sequence == sequence[3]):
        current_sequence = sequence[3]
        dialogue_index = 11

    if current_sequence == sequence[0] or current_sequence == sequence[3]:
        # all asteroid must be stopped
        window.blit(gradient_surface, (0, 0))  # Apply gradient at the bottom half
        window.blit(randomChar, (0, y_window - randomChar.get_size()[1]))

        if mousepress[0] and not (dialogue_index == len(prologue_dialogue) - 1):
            if waiting_for_click:
                dialogue_index += 1
                char_index = 0
                randomChar = anime_images[random.randint(0,1)]
                waiting_for_click = False
                if dialogue_index == 10:
                    current_sequence = sequence[1]
        
        if dialogue_index < len(prologue_dialogue):
            full_text = prologue_dialogue[dialogue_index]
            wrapped_lines = wrap_text_by_words(full_text, 10)
            total_length = len(full_text)

            if char_index < total_length:
                frame_counter += 1
                if frame_counter % type_speed == 0:
                    char_index += 1
            else:
                waiting_for_click = True


            draw_text(window, wrapped_lines, (200, y_window - 80), char_index)

        if waiting_for_click and not (dialogue_index == len(prologue_dialogue) - 1):
            clickanywhere = arcade_font.render(f"<click anywhere to continue>", True, (255, 254, 198))
            window.blit(clickanywhere, (200, y_window - 110))

    
    
    # ___________________________________other prioritized images____________________________
    if dialogue_index == 5:
        tweensys_leftclickguide.draw()
    elif dialogue_index == 6:
        tweensys_arrow_key_guide.draw()
    elif dialogue_index == 7:
        tweensys_lootboxguide.draw()
    elif dialogue_index == 8:
        tweensys_rightclickguide.draw()
    elif dialogue_index == len(prologue_dialogue)-1:
        tweensys_perform_report.update()
        tweensys_perform_report.draw()

        tweensys_classified_text.update_transparency()
        tweensys_classified_text.draw()

        tweensys_exit_sys_ui.draw()
        tweensys_exit_sys_ui.update_transparency()
        tweensys_exit_prog_text.draw()
        tweensys_exit_prog_text.update_transparency()

        mycardorganizer.organize_card_selection_once()
        mycardorganizer.sort_card_selection()
        list_card_with_max_amount = mycardorganizer.card_classification_amount_max
        
        
        if 'COMMANDER' in list_card_with_max_amount and 'HACKER' in list_card_with_max_amount:
            classification_img['codewarden'].transparency.update_transparency()
            classification_img['codewarden'].transparency.draw()
        elif 'COMMANDER' in list_card_with_max_amount and 'RAYCASTER' in list_card_with_max_amount:
            classification_img['spacewarrior'].transparency.update_transparency()
            classification_img['spacewarrior'].transparency.draw()
        elif 'HACKER' in list_card_with_max_amount and 'RAYCASTER' in list_card_with_max_amount:
            classification_img['voidbreaker'].transparency.update_transparency()
            classification_img['voidbreaker'].transparency.draw()
        else:
            if 'COMMANDER' in list_card_with_max_amount:
                classification_img['commander'].transparency.update_transparency()
                classification_img['commander'].transparency.draw()
            elif 'HACKER' in list_card_with_max_amount:
                classification_img['hacker'].transparency.update_transparency()
                classification_img['hacker'].transparency.draw()
            elif 'RAYCASTER' in list_card_with_max_amount:
                classification_img['raycaster'].transparency.update_transparency()
                classification_img['raycaster'].transparency.draw()  

        if mousepress[0]:
            if tweensys_exit_sys_ui.current_pos.x <= mouse_x <=  tweensys_exit_sys_ui.current_pos.x + exit_sys_ui.get_size()[0] and tweensys_exit_sys_ui.current_pos.y <= mouse_y <=  tweensys_exit_sys_ui.current_pos.y + exit_sys_ui.get_size()[1]: 
                run = False
        
        for index, (cardName, amount) in enumerate(mycardorganizer.players_card_selection_grouping_sorted.items()):
            image = ability_icons[cardName]
            image = pygame.transform.scale(image, (image.get_size()[0]//1.5, image.get_size()[1]//1.5))
            classification = cardsList[cardName].subtitle
            
            currentpos = None
            if index <= 2:
                
                currentpos = (tweensys_perform_report.target_pos + pygame.Vector2(60, 210 + (image.get_size()[1] + 5) * index))

            else:
                currentpos = (tweensys_perform_report.target_pos + pygame.Vector2(190, 210 + (image.get_size()[1] + 5) * (index-3)))
            
            amount_card_text = gothic_font_medium.render(f"x{amount}", True, (255, 255, 255))
            classification_text = gothic_font_small.render(f"[{classification}]", True, (128, 128, 128))
            window.blit(image, currentpos)
            window.blit(amount_card_text, currentpos + pygame.Vector2(image.get_size()[1] + 10, 0))
            window.blit(classification_text, currentpos + pygame.Vector2(image.get_size()[1] + 10, 20))
                            


    # __________________________lootbox mechanism___________________________
    currentTimeInMilisecs = 0

    if lootbox_sys.continueCounterlootbox and current_sequence == sequence[1]:
        currentTimeInMilisecs = pygame.time.get_ticks()

    if currentTimeInMilisecs - lootbox_sys.pygamecountermilisecs >= 1000 and lootbox_sys.enableCountdown: # 1 sec
        
        lootbox_sys.pygamecountermilisecs = currentTimeInMilisecs

        lootbox_sys.lootboxCounterInSeconds -= 1
    
    if lootbox_sys.lootboxCounterInSeconds == 0:
        lootbox_sys.lootboxCounterInSeconds = 0
        lootbox_sys.enableCountdown = False
        current_sequence = sequence[2]
        enablefade_once('out')
        fade.update()
        fade.draw(window)
        if lootboxtween.elapsed_time <= 2:
            lootboxtween.draw()
        else:
            def gambleCard():
                pick = random.choice(list(cardsList.keys()))
                if not (pick in lootbox_sys.randomCardnames):
                    return pick
                else:
                    return gambleCard()
            
            window.blit(lootbox_openImg, endlootbox_pos)
            window.blit(pick_card_text, endlootbox_pos + pygame.Vector2(30, 0))


            if len(lootbox_sys.randomCardnames) == 0:
                # Pick 3 unique random cards from all cards in cardsList
                lootbox_sys.randomCardnames = random.sample(list(cardsList.keys()), 3)
            else:
                for index,cardNames in enumerate(lootbox_sys.randomCardnames):
                    cardObject = cardsList[cardNames]
                    cardSize = cardObject.image.get_size()
                    
                    targetposition = pygame.Vector2(windowcenterx - cardSize[0]/2 - (cardSize[0] + 30) * (1-index), windowcentery-cardSize[1]/2-100  )
                    startposition = pygame.Vector2(windowcenterx - cardSize[0]/2 - (cardSize[0] + 30) * (1-index), y_window)
                    if cardObject.tweenClass == None:
                        
                        cardObject.tweenClass = makeTween(image=cardObject.image,start=startposition, target=targetposition)
                    else:
                        #print(cardObject.title, 'position reset')
                        cardObject.tweenClass.startpos = startposition
                        cardObject.tweenClass.target = targetposition

                    toprightcard  = cardObject.tweenClass.current_pos
                    centercard = toprightcard + pygame.Vector2(cardSize[0]//2, cardSize[1]//2)
                    if toprightcard.x <= mouse_pos[0] <=  toprightcard.x + cardSize[0] and toprightcard.y <= mouse_pos[1] <=  toprightcard.y + cardSize[1]:
                        difsize = (pygame.Vector2(*gleamcard.get_size()) - pygame.Vector2(*cardSize))/2
                        window.blit(gleamcard, toprightcard-difsize)
                        if mousepress[0]:
                            print(cardNames, 'picked')
                            insertability(cardNames)
                            
                            lootbox_sys.enableCountdown = True
                            lootbox_sys.lootboxCounterInSeconds = math.floor(lootbox_sys.lootboxcounter_const * 1.1)
                            lootbox_sys.lootboxcounter_const = math.floor(lootbox_sys.lootboxcounter_const * 1.1)
                            enablefade_once('in')
                            
                            lootboxtween.reset()
                            lootbox_sys.randomCardnames = []
                        
                            current_sequence = sequence[1]
                            
                            
                                
                    
                    if not (cardObject.tweenClass == None):
                        cardObject.tweenClass.draw()
                        cardObject.drawtext(centercard)

    if lootbox_sys.enableCountdown == True and current_sequence == sequence[1]:
        countdown = arcade_font.render(f"specialized weapon quiz in {lootbox_sys.lootboxCounterInSeconds}", True, (255, 255, 255))
        window.blit(countdown, (windowcenterx- countdown.get_size()[0]//2, y_window - 100))

    notif_sys.draw()
    

    pygame.display.update() # updating the window or else the rect won't be displayed

pygame.quit()
    


    
