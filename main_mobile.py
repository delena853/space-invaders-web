import pygame
import random
import asyncio

pygame.init()
pygame.mixer.init()
tir_sound=pygame.mixer.Sound("tir.wav")
explosion_sound=pygame.mixer.Sound("explosion.wav")
game_over_sound=pygame.mixer.Sound("game_over.wav")

# ==========================================
# FENÊTRE
# ==========================================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

# ==========================================
# COULEURS
# ==========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# ==========================================
# IMAGES
# ==========================================

background = pygame.image.load("background.png").convert()
print("Taille background :", background.get_size())
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (70, 55))

alien_img = pygame.image.load("alien.png").convert_alpha()
alien_img = pygame.transform.scale(alien_img, (55, 45))

alien2_img=pygame.image.load("alien2.png").convert_alpha()
alien2_img=pygame.transform.scale(alien2_img, (55, 45))

alien3_img=pygame.image.load("alien3.png").convert_alpha()
alien3_img=pygame.transform.scale(alien3_img, (55, 45))
shield_img=pygame.image.load("shield.png").convert_alpha()
shield_img=pygame.transform.scale(shield_img, (90, 60))

shield_damage1_img=pygame.image.load("shield_damage1.png").convert_alpha()
shield_damage1_img=pygame.transform.scale(shield_damage1_img, (90, 60))

shield_damage2_img=pygame.image.load("shield_damage2.png").convert_alpha()
shield_damage2_img=pygame.image.load("shield_damage2.png").convert_alpha()

boss_img=pygame.image.load("boss.png").convert_alpha()
boss_img=pygame.transform.scale(boss_img, (120, 90))

laser_img = pygame.image.load("laser.png").convert_alpha()

# Recadrage autour du laser
laser_img = laser_img.subsurface((400, 380, 220, 780)).copy()

# Taille du laser dans le jeu
laser_img = pygame.transform.scale(laser_img, (18, 55))
#images de l'explosion
explosion_images=[]

for i in range(1,7):
    image=pygame.image.load(f"explosion{i}.png").convert_alpha()
    image=pygame.transform.scale(image, (70,70))
    explosion_images.append(image)
explosions=[]
# ==========================================
# POLICE
# ==========================================

font = pygame.font.SysFont("Arial", 30)
button_font = pygame.font.SysFont("Arial", 24)

# ==========================================
# JOUEUR
# ==========================================

player = pygame.Rect(WIDTH // 2 - 35, HEIGHT - 80, 70, 55)
player_speed = 6

# ==========================================
# BOUTONS TACTILES (VERSION MOBILE)
# ==========================================
left_button = pygame.Rect(20, 525, 70, 55)
right_button = pygame.Rect(100, 525, 70, 55)
fire_button = pygame.Rect(WIDTH - 90, 525, 70, 55)

touches = {}
last_mobile_shot = 0

# bouclier
shields=[
    {"rect": pygame.Rect(120, 440, 90, 60),"life":3},
    {"rect": pygame.Rect(355, 440, 90, 60),"life":3},
    {"rect": pygame.Rect(590, 440, 90, 60),"life":3}
]
# ==========================================
# BALLES
# ==========================================

bullets = []
enemy_bullets=[]
enemy_shoot_timer=0
bonuses=[]
# ==========================================
# ENNEMIS
# ==========================================

enemies = []

for i in range(8):

    enemy_type = random.randint(1, 3)

    enemy = {
        "rect": pygame.Rect(
            random.randint(40, WIDTH - 80),
            random.randint(-300, -50),
            55,
            45
        ),
        "type": enemy_type,
        "life": 1
    }

    if enemy_type == 3:
        enemy["life"] = 2

    enemies.append(enemy)

enemy_speed = 2

# ==========================================
# SCORE
# ==========================================

score = 0
try:
    with open ("best_score.txt", "r") as file:
        best_score=int(file.read())
except:
    best_score=0
lives=3
game_over=False
level=1
enemy_speed=2
rapid_fire=False
double_laser=False
rapid_timer=0
double_timer=0
rapid_shoot_timer=0
# ==========================================
# BOUCLE PRINCIPALE
# ==========================================

running = True

async def main():
    global running, game_over, score, lives, shields, level, enemy_speed
    global rapid_fire, double_laser, rapid_timer, double_timer, rapid_shoot_timer
    global enemy_shoot_timer, best_score, touches, last_mobile_shot

    while running:
    
        # Si le jeu est terminé
        if game_over:
            screen.fill(BLACK)

            game_over_text = font.render("GAME OVER", True, RED)

            screen.blit(
                game_over_text,
                (
                    WIDTH // 2 - game_over_text.get_width() // 2,
                    HEIGHT // 2 - 80
                )
            )

            score_text = font.render(f"Score : {score}", True, WHITE)

            screen.blit(
                score_text,
                (
                    WIDTH // 2 - score_text.get_width() // 2,
                    HEIGHT // 2 - 20
                )
            )

            new_game_text = font.render(
                "ENTREE = Nouvelle partie",
                True,
                WHITE
            )

            screen.blit(
                new_game_text,
                (
                    WIDTH // 2 - new_game_text.get_width() // 2,
                    HEIGHT // 2 + 40
                )
            )

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
    
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:

                        score = 0
                        lives = 3
                        game_over = False
                    
                        shields=[
                            {"rect": pygame.Rect(120, 440, 90, 60), "life": 3},
                            {"rect": pygame.Rect(355, 440, 90, 60), "life": 3},
                            {"rect": pygame.Rect(590, 440, 90, 60), "life": 3}
                        ] 

                        player.x = WIDTH // 2 - 25
                        player.y = HEIGHT - 60

                        bullets.clear()
                        enemy_bullets.clear()

                        for enemy in enemies:
                       
                         if enemy["rect"].top>HEIGHT:
                           
                               enemy["rect"].x=random.randint(40, WIDTH-80)
                               enemy["rect"].y=random.randint(-300, -50)

            clock.tick(60)
            await asyncio.sleep(0)
            continue
    
        # ======================================
        # ÉVÉNEMENTS
        # ======================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                    
                        tir_sound.play()

    
                        if double_laser:
                            bullets.append(
                                pygame.Rect(
                                    player.left + 12,
                                    player.top,
                                    6,
                                    15
                                )
                            )

                            bullets.append(
                                pygame.Rect(
                                    player.right - 18,
                                    player.top,
                                    6,
                                    15
                                )
                          )

                        else:
                            bullets.append(
                                 pygame.Rect(
                                     player.centerx - 3,
                                     player.top,
                                     6,
                                     15
                                 )
                            )
                    
                    
            # --------------------------------------
            # COMMANDES TACTILES / SOURIS
            # --------------------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and fire_button.collidepoint(event.pos):
                    now = pygame.time.get_ticks()
                    if now - last_mobile_shot > 120:
                        last_mobile_shot = now
                        tir_sound.play()

                        if double_laser:
                            bullets.append(
                                pygame.Rect(
                                    player.left + 12,
                                    player.top,
                                    6,
                                    15
                                )
                            )
                            bullets.append(
                                pygame.Rect(
                                    player.right - 18,
                                    player.top,
                                    6,
                                    15
                                )
                            )
                        else:
                            bullets.append(
                                pygame.Rect(
                                    player.centerx - 3,
                                    player.top,
                                    6,
                                    15
                                )
                            )

            if event.type == pygame.FINGERDOWN:
                finger_pos = (int(event.x * WIDTH), int(event.y * HEIGHT))
                touches[event.finger_id] = finger_pos

                if fire_button.collidepoint(finger_pos):
                    now = pygame.time.get_ticks()
                    if now - last_mobile_shot > 120:
                        last_mobile_shot = now
                        tir_sound.play()

                        if double_laser:
                            bullets.append(
                                pygame.Rect(
                                    player.left + 12,
                                    player.top,
                                    6,
                                    15
                                )
                            )
                            bullets.append(
                                pygame.Rect(
                                    player.right - 18,
                                    player.top,
                                    6,
                                    15
                                )
                            )
                        else:
                            bullets.append(
                                pygame.Rect(
                                    player.centerx - 3,
                                    player.top,
                                    6,
                                    15
                                )
                            )

            if event.type == pygame.FINGERMOTION:
                touches[event.finger_id] = (
                    int(event.x * WIDTH),
                    int(event.y * HEIGHT)
                )

            if event.type == pygame.FINGERUP:
                if event.finger_id in touches:
                    del touches[event.finger_id]

        # ======================================
        # CLAVIER
        # ======================================

        keys = pygame.key.get_pressed()

        mobile_left = False
        mobile_right = False
        mobile_fire = False

        # Souris : utile pour tester les boutons sur ordinateur
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            mobile_left = left_button.collidepoint(mouse_pos)
            mobile_right = right_button.collidepoint(mouse_pos)
            mobile_fire = fire_button.collidepoint(mouse_pos)

        # Doigts sur téléphone / tablette
        for touch_pos in touches.values():
            if left_button.collidepoint(touch_pos):
                mobile_left = True
            if right_button.collidepoint(touch_pos):
                mobile_right = True
            if fire_button.collidepoint(touch_pos):
                mobile_fire = True

        if rapid_fire and (keys[pygame.K_SPACE] or mobile_fire):

            rapid_shoot_timer += 1

            if rapid_shoot_timer >= 8:
                rapid_shoot_timer = 0

                tir_sound.play()

                if double_laser:
                    bullets.append(
                        pygame.Rect(
                            player.left + 12,
                            player.top,
                            6,
                            15
                        )
                    )

                    bullets.append(
                        pygame.Rect(
                            player.right - 18,
                            player.top,
                            6,
                            15
                        )
                    )

                else:
                    bullets.append(
                        pygame.Rect(
                            player.centerx - 3,
                            player.top,
                            6,
                            15
                        )
                    )

        else:
            rapid_shoot_timer = 0
        if (keys[pygame.K_LEFT] or mobile_left) and player.left > 0:
            player.x -= player_speed

        if (keys[pygame.K_RIGHT] or mobile_right) and player.right < WIDTH:
            player.x += player_speed

        # ======================================
        # DÉPLACEMENT DES LASERS
        # ======================================

        for bullet in bullets[:]:

            bullet.y -= 10

            if bullet.bottom < 0:
                bullets.remove(bullet)
            
        # tire des ennemis
        enemy_shoot_timer+=1
    
        if enemy_shoot_timer >=60:
            enemy_shoot_timer=0
        
            if enemies:
                enemy=random.choice(enemies)
            
                enemy_bullets.append(
                    pygame.Rect(
                        enemy["rect"].centerx-3,
                        enemy["rect"].bottom,
                        6,
                        15
                    )
                )
    
        # déplacement des tirs ennemis
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.y+=6
        
            if enemy_bullet.top>HEIGHT:
                enemy_bullets.remove(enemy_bullet)
        # DéPLACEMENT DES BONUS
        for bonus in bonuses[:]:
            bonus["rect"].y += 3
        
            if bonus["rect"].top>HEIGHT:
                bonuses.remove(bonus)
        # collision joueur/bonus
        for bonus in bonuses[:]:
            if player.colliderect(bonus["rect"]):
                if bonus["type"]=="rapid":
                    rapid_fire=True
                    rapid_timer=7200
                elif bonus["type"]=="double":
                    double_laser = True
                    double_timer = 7200
                
                bonuses.remove(bonus)
        #durée des bonus
        if rapid_fire:
            rapid_timer-=1
        
            if rapid_timer<=0:
                rapid_fire=False
            
        if double_laser:
            double_timer -=1
        
            if double_timer <=0:
                double_laser=False
        # ======================================
        # DÉPLACEMENT DES ENNEMIS
        # ======================================

        for enemy in enemies:
         
            if enemy["type"] == 4:

        
                if enemy["rect"].y < 80:
                    enemy["rect"].y += 2
            else:
            
                enemy["rect"].y += enemy_speed
    
                if enemy["rect"].top > HEIGHT:
                    enemy["rect"].x = random.randint(40, WIDTH - 80)
                    enemy["rect"].y = random.randint(-300, -50)
        # collisions entre les tirs ennemis et les boucliers
   
        for enemy_bullet in enemy_bullets[:]:
            for shield in shields[:]:
                if enemy_bullet.colliderect(shield["rect"]):
                    if enemy_bullet in enemy_bullets:
                        enemy_bullets.remove(enemy_bullet)

                    shield["life"] -= 1

                    if shield["life"] <= 0:
                        shields.remove(shield)

                    break
                
        # collisions entre les tirs ennemis et le joueur
        for enemy_bullet in enemy_bullets[:]:
            if enemy_bullet.colliderect(player):
                enemy_bullets.remove(enemy_bullet)
                lives -= 1
            
                if lives<0:
                    lives=0
                    game_over=True
                    if score > best_score:
                        best_score = score
                    
                        with open("best_score.txt", "w") as file:
                            file.write(str(best_score))
                    game_over_sound.play()
                
            
                player.x=WIDTH//2-25
                player.y=HEIGHT-60
    
    
    
    

        # ======================================
        # explosion
        # ======================================
        for bullet in bullets[:]:

            for enemy in enemies[:]:

                if bullet.colliderect(enemy["rect"]):
        
                    if bullet in bullets:
                        bullets.remove(bullet)

                    enemy["life"] -= 1

                    if enemy["life"] <= 0:

                        explosions.append({
                            "x": enemy["rect"].centerx,
                            "y": enemy["rect"].centery,
                            "frame": 0
                        })
                    
                        if random.randint(1, 5) == 1:

                            bonus_type = random.choice(["rapid", "double"])

                            bonuses.append({
                                "rect": pygame.Rect(
                                   enemy["rect"].centerx - 15,
                                   enemy["rect"].centery - 15,
                                   30,
                                   30
                                ),
                                "type": bonus_type
                             })
                        
                        if enemy in enemies:
                            enemies.remove(enemy)

                        score += 1
                        explosion_sound.play()

                    break
            # Passage au niveau suivant
            if len(enemies) == 0:
                level += 1
                enemy_speed += 1
            
                if level % 5 == 0:

                    boss = {
                        "rect": pygame.Rect(
                             WIDTH // 2 - 60,
                             -100,
                            120,
                            90
                        ),
                        "type": 4,
                        "life": 20
                     }
        
                    enemies.append(boss)
                else:
            
                    for i in range(8 + level * 2):

                        enemy_type = random.randint(1, 3)

                        enemy = {
                            "rect": pygame.Rect(
                                random.randint(40, WIDTH - 80),
                                random.randint(-300, -50),
                                55,
                                45
                            ),
                            "type": enemy_type,
                            "life": 1
                        }

                        if enemy_type == 3:
                            enemy["life"] = 2

                        enemies.append(enemy)
    
        # ======================================
        # AFFICHAGE
        # ======================================

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 240, 80))
        screen.blit(player_img, player)

        for enemy in enemies:
            if enemy["type"]==1:
                screen.blit(alien_img, enemy["rect"])
        
            elif enemy["type"]==2:
                screen.blit(alien2_img, enemy["rect"])
        
            elif enemy["type"]==3:
                screen.blit(alien3_img, enemy["rect"])
        
            elif enemy["type"]==4:
                screen.blit(boss_img, enemy["rect"])
        for explosion in explosions[:]:
            frame=explosion["frame"]
            if frame < len(explosion_images):
                image=explosion_images[frame]
                screen.blit(
                    image,
                    (
                        explosion["x"]-image.get_width()//2,
                        explosion["y"]-image.get_height()//2
                    )
                )
                
                explosion["frame"]+=1
                
            else:
                explosions.remove(explosion)

        for bullet in bullets:
            screen.blit(laser_img, bullet)
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(screen, (255, 50, 50), enemy_bullet)

        texte = font.render(f"Score : {score}", True, WHITE)
        screen.blit(texte, (10, 10))
        best_text=font.render(
            "Record : " + str(best_score),
            True,
            (255,255,255)
        )
    
        screen.blit(best_text, (10, 50)) 
        texte_vies=font.render(f"Vies:{lives}", True, WHITE)
        screen.blit(texte_vies, (10, 90))
        niveau_text=font.render(f"Niveau : {level}", True, WHITE)
        screen.blit(niveau_text, (10, 130))
        for shield in shields:
            if shield["life"]==3:
                screen.blit(shield_img, shield["rect"])
        
            elif shield["life"]==2:
                screen.blit(shield_damage1_img, shield["rect"])
        
            elif shield["life"]==1:
                screen.blit(shield_damage2_img, shield["rect"])
        for bonus in bonuses:
            if bonus["type"]=="rapid":
                pygame.draw.circle(
                    screen,
                    (255, 255, 0),
                    bonus["rect"].center,
                    15
                )
            
            elif bonus ["type"]=="double":
                pygame.draw.circle(
                    screen,
                    (0, 255, 255),
                    bonus["rect"].center,
                    15
                )
        # ==========================================
        # AFFICHAGE DES BOUTONS TACTILES
        # ==========================================
        pygame.draw.rect(screen, (30, 30, 60), left_button, border_radius=12)
        pygame.draw.rect(screen, WHITE, left_button, 2, border_radius=12)

        pygame.draw.rect(screen, (30, 30, 60), right_button, border_radius=12)
        pygame.draw.rect(screen, WHITE, right_button, 2, border_radius=12)

        pygame.draw.rect(screen, (100, 30, 30), fire_button, border_radius=12)
        pygame.draw.rect(screen, WHITE, fire_button, 2, border_radius=12)

        left_text = button_font.render("<", True, WHITE)
        right_text = button_font.render(">", True, WHITE)
        fire_text = button_font.render("TIR", True, WHITE)

        screen.blit(
            left_text,
            (
                left_button.centerx - left_text.get_width() // 2,
                left_button.centery - left_text.get_height() // 2
            )
        )

        screen.blit(
            right_text,
            (
                right_button.centerx - right_text.get_width() // 2,
                right_button.centery - right_text.get_height() // 2
            )
        )

        screen.blit(
            fire_text,
            (
                fire_button.centerx - fire_text.get_width() // 2,
                fire_button.centery - fire_text.get_height() // 2
            )
        )

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
