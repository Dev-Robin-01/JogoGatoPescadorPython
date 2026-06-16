import pygame, sys
import button
from pesca import Pescar 
from animações import GatoPescador

pygame.init()

screen = pygame.display.set_mode((800,800))
Clock = pygame.time.Clock()
pygame.display.set_caption('CatFishing')

game_started = False
jogo_pesca = None 

icon_surface = pygame.image.load('Sprites/Icon.png')
pygame.display.set_icon(icon_surface)

test_surface = pygame.image.load('Sprites/image-11.png')  
test_surface = pygame.transform.scale(test_surface,(802,803)).convert()

title_placa = pygame.transform.scale(pygame.image.load('Sprites/Title.png'), (600,150)).convert_alpha()
start_placa = pygame.transform.scale(pygame.image.load('Sprites/Start.png'), (400,100)).convert_alpha()
exit_placa = pygame.transform.scale(pygame.image.load('Sprites/Exit.png'), (300,100)).convert_alpha()
defi_placa = pygame.transform.scale(pygame.image.load("Sprites/Defi.png"), (80,80)).convert_alpha()
backpack_icon = pygame.transform.scale(pygame.image.load("Sprites/Backpack_Icon.png"), (200,200)).convert_alpha()
shop_icon = pygame.transform.scale(pygame.image.load("Sprites/Shop_Icon.png"), (200,200)).convert_alpha()

# Cria os botões
start_button = button.Button(200, 300, start_placa, 1)
exit_button = button.Button(250, 450, exit_placa, 1)
defi_button = button.Button(730, 10, defi_placa, 0.7)
backpack_button = button.Button(590, -50, backpack_icon, 1)
shop_button = button.Button(535, -48, shop_icon, 0.8)

gato = GatoPescador(screen,200, 414)
game_started = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if game_started: 
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                gato.registro_atividade()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_started:
                game_started = False
                jogo_pesca = None
            if event.key == pygame.K_SPACE and game_started and jogo_pesca is None:
                jogo_pesca = Pescar(screen)


    screen.blit(test_surface, (-2, -3))  

    if not game_started:
        # TELA DE MENU
        screen.blit(title_placa, (100, 100))
        
        if start_button.draw(screen):
            game_started = True  
            jogo_pesca = None
            
        if exit_button.draw(screen):
            pygame.quit()
            sys.exit()
    else:

        gato.atualizar()
        gato.desenhar()
        
    
        if jogo_pesca is not None:
            jogo_pesca.atualizar()
            jogo_pesca.desenhar()
            if jogo_pesca.estado_jogo in ["fechado", "perdeu"]:
                jogo_pesca = None
        
        # Botões de interface adicionais
        if defi_button.draw(screen):
            pass # Coloque aqui o que o botão de Definições deve fazer
        if backpack_button.draw(screen):
            pass
        if shop_button.draw(screen):
            pass    

    pygame.display.update()
    Clock.tick(60)
