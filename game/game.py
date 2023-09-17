import pygame
from sys import exit
from random import randint

def anim(anim_lst,display_idx):
    return anim_lst[int(display_idx)]
def display_score():
    current_time = pygame.time.get_ticks() - game_timer
    score_surf = font.render(f'Score:{current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (450,80))
    my_screen.blit(score_surf,score_rect)
game_active = True
pygame.init()
my_screen = pygame.display.set_mode((924,520)) #screen size
pygame.display.set_caption("Minotaur") #title of the application
icon = pygame.image.load("graphics/Minotaur_2/PNG/Vector Parts/Head.png") #icon of the application
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
bridge_background = pygame.image.load("graphics/background/1.png").convert()
font = pygame.font.Font("font/Pixeltype.ttf", 50)

#Background music
pygame.mixer.music.load("audio/music.wav")
pygame.mixer.music.play(-1)

#Restart Window
restart = pygame.image.load("reset.png")

#PLAYER CONFIG
player1 = pygame.image.load("graphics/player/1.png").convert_alpha()
player2 = pygame.image.load("graphics/player/2.png").convert_alpha()
player3 = pygame.image.load("graphics/player/3.png").convert_alpha()
player4 = pygame.image.load("graphics/player/4.png").convert_alpha()
player_anim_list = [player1,player2,player3,player4]
player_idx = 0
player_rect = player_anim_list[int(player_idx)].get_rect(topleft = (50,340))

# BlueFly CONFIG
bluefly1 = pygame.image.load("graphics/Fly/BlueFly1.png").convert_alpha()
bluefly2 = pygame.image.load("graphics/Fly/BlueFly2.png").convert_alpha()
bluefly_anim_lst = [bluefly1,bluefly2]
bluefly_idx = 0
bluefly_pos = randint(1000,1400)
bluefly_rect = bluefly_anim_lst[bluefly_idx].get_rect(topright = (bluefly_pos,300))

# FLY CONFIG
fly1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_anim_lst = [fly1,fly2]
fly_idx = 0
fly_pos = 1200
fly_rect = fly_anim_lst[fly_idx].get_rect(topright = (fly_pos,300))

gravity = 0
clock_cnt = 0.001
game_timer = 0


# Inside the game loop
while True:
    clock_cnt+=0.001
    if game_active:
        my_screen.blit(bridge_background, (0, 0))  # Background picture
        # Blit the fly image onto its rectangle
        my_screen.blit(anim(fly_anim_lst,fly_idx),fly_rect)
        # Blit the blue fly image onto its rectangle
        my_screen.blit(anim(bluefly_anim_lst,bluefly_idx),bluefly_rect)
        # Blit the player image onto its rectangle
        my_screen.blit(anim(player_anim_list,player_idx), player_rect)
        display_score()
        # Fly anim
        fly_idx += 1
        if fly_idx > len(fly_anim_lst) - 1:
            fly_idx = 0

        # blue Fly anim
        bluefly_idx += 1
        if bluefly_idx > len(bluefly_anim_lst) - 1:
            bluefly_idx = 0

        # Fly Movement
        fly_rect.right -= (2.5 + clock_cnt)
        if fly_rect.right < -50:
            fly_rect.right = randint(1000,1300)
        # Fly Movement
        bluefly_rect.right -= (2 + clock_cnt)
        if bluefly_rect.right < -50:
            bluefly_rect.right = randint(1000,1300)

        # Apply gravity to the player
        gravity += 0.9
        player_rect.y += gravity
        if player_rect.bottom >= 340:
            player_rect.bottom = 340

        # Player anim
        player_idx += 0.12
        if player_idx > len(player_anim_list) - 1:
            player_idx = 0

        # Player movement
        if player_rect.x < 0: player_rect.x = 0
        if player_rect.x > 850: player_rect.x = 850
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= 3
        elif keys[pygame.K_RIGHT]:
            player_rect.x += 3

         # Check for collision
        if player_rect.colliderect(bluefly_rect) or player_rect.colliderect(fly_rect):
            game_active = False
            lost_sound = pygame.mixer.Sound("audio/lost.wav")
            lost_sound.play()
            
    else:
        # Display restart screen
        my_screen.blit(restart,(300,150))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Jump animation
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and player_rect.bottom == 340 :
                gravity = -20
                jump_sound = pygame.mixer.Sound("audio/jump.mp3")
                jump_sound.play()
        else:
        # Restart game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bluefly_rect.right = 1200
                fly_rect.right = 1200
                player_rect.right = 50
                health = 3
                clock_cnt = 0
                game_timer = pygame.time.get_ticks()
                game_active = True
    pygame.display.update()
    clock.tick(80)
