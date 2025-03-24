import pygame 
from pygame.locals import  * 
import random






class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
           img = pygame.image.load(f"assets/bird{num}.png") 
           self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        
    def update(self, flying, game_over):
        
        if flying: 
        #Gravity
            self.vel += 0.2
            if self.vel > 4:
                self.vel = 4
            
            if self.rect.bottom < 197:
                self.rect.y += int(self.vel)
             
        if game_over == False:
            #Jumping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -3
            if pygame.mouse.get_pressed()[0] == 0: 
                self.clicked = False
            
            
            #Animation
            self.counter += 1
            flap_cooldown = 5
            
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images): 
                    self.index=0
                    
                self.image = self.images[self.index]
            
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            
            
            
            
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, position,pipe_gap,scroll_speed):
        self.scroll_speed = scroll_speed
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/pipe.png")
        self.rect = self.image.get_rect()
        #Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]
        
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap/2)]
            
            
    def update(self):
        self.rect.x -= self.scroll_speed
        
        if self.rect.right < 0: 
            self.kill()




class Button():
    def __init__(self, x, y, image, screen):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        return action




class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60



        #Set window heigh and width
        self.screen_width = 320
        self.screen_height = 240
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        
        
        #load header
        pygame.display.set_caption("Flappy Bird")


        #load assets
        self.bg = pygame.image.load("assets/bg.png")
        self.ground_img = pygame.image.load("assets/ground.png")
        self.button_img =  pygame.image.load("assets/restart.png")

        #define font
        self.font = pygame.font.SysFont('Bauhaus 93', 27)

        #define colours
        self.white = (255, 255, 255)

        #Game variables 

        self.ground_scroll = 0
        self.scroll_speed = 2
        self.flying = False
        self.game_over = False
        self.pipe_gap = 35
        self.pipe_frequency = 1500
        self.last_pipe = pygame.time.get_ticks() -self.pipe_frequency
        self.score = 0
        self.pass_pipe = False 
        
        
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()

        self.flappy = Bird(30, int(self.screen_height/2))

        #Instance of the button class
        self.button = Button(self.screen_width // 2 -21 , self.screen_height // 2 -10, self.button_img,self.screen)

        self.bird_group.add(self.flappy)



    #Drawing text
    def draw_text(self,text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))


    def reset_game(self):
        self.pipe_group.empty()
        self.flappy.rect.x = 30
        self.flappy.rect.y = int(self.screen_height / 2)
        self.score = 0
        self.flying = False
        self.game_over = False
        self.pass_pipe = False
        self.flappy.vel = 0
        return self.score




    def run(self):
        
        #Game loop
        run = True

        while run:
            #set fps
            self.clock.tick(self.fps)


            #Background placement
            self.screen.blit(self.bg,(0,0))
            
            #Draw bird
            self.bird_group.draw(self.screen)
            self.bird_group.update(self.flying, self.game_over)
            
            #Draw pipe 
            self.pipe_group.draw(self.screen)
            
            
            #Draw the groung 
            self.screen.blit(self.ground_img,(self.ground_scroll,197))
            
            #Check the score 
            if (len(self.pipe_group) > 0): 
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left\
                    and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right \
                        and self.pass_pipe == False:
                            self.pass_pipe = True
                if self.pass_pipe == True:
                    if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right:
                        self.score += 1
                        self.pass_pipe = False
            
            #Draw it on the screen
            self.draw_text(str(self.score), self.font, self.white, int(self.screen_width / 2), 17)

                    
                    
                    
                
            
            
            #Check for collision
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
                self.game_over = True
                
            
            #Chech if bird has hit the ground
            if self.flappy.rect.bottom >= 197:
                self.game_over = True
                self.flying = False
            
            
            if not self.game_over and self.flying == True:
                
                #Generate new pipes
                time_now = pygame.time.get_ticks() 
                if time_now - self.last_pipe > self.pipe_frequency:
                    pipe_height = random.randint(-33,20)
                
                    btm_pipe  = Pipe(self.screen_width, int(self.screen_height/2)+pipe_height, 1,self.pipe_gap,self.scroll_speed)
                    top_pipe  = Pipe(self.screen_width, int(self.screen_height/2)+pipe_height, -1,self.pipe_gap,self.scroll_speed)
                    self.pipe_group.add(btm_pipe)
                    self.pipe_group.add(top_pipe)
                    self.last_pipe = time_now
        
                
        
                
                #Group scrolling effect
                self.ground_scroll -= self.scroll_speed
                if abs(self.ground_scroll) > 10:
                    self.ground_scroll = 0
            
        
                self.pipe_group.update()
                
                
                
            #check for game over and reset
            if self.game_over == True:
                if self.button.draw() == True:
                    self.game_over = False
                    self.score = self.reset_game()
            
            
            #If exit, exit screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.flying == False and self.game_over == False:
                    self.flying = True
                    
                    
            pygame.display.update()
                    
        pygame.quit()



