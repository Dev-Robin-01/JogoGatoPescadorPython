import pygame
import os
import random
import math
from raridades import raridades

class Pescar:
    def __init__(self,tela_jogo):
        self.tela = tela_jogo
        
        # 1. Primeiro CARREGAMOS as imagens do disco (repara nos parênteses no final de cada load!)
        img_fundo_crua = pygame.image.load(os.path.join("Sprites", "barra_bg.png")).convert_alpha()
        img_barra_crua = pygame.image.load(os.path.join("Sprites", "barra_player.png")).convert_alpha()
        img_peixe_crua = pygame.image.load(os.path.join("Sprites", "peixe.png")).convert_alpha()
        img_cauda_crua = pygame.image.load(os.path.join("Sprites", "cauda.png")).convert_alpha()
        img_barra_2 = pygame.image.load(os.path.join("Sprites", "barra_body.png")).convert_alpha()
        img_progresso = pygame.image.load(os.path.join("Sprites", "barra_progresso.png")).convert_alpha()
        img_coroa = pygame.image.load(os.path.join("Sprites", "coroa.png")).convert_alpha()
        

        # 2. Agora REDIMENSIONAMOS as imagens cruas e guardamos nas variáveis oficiais da classe (self)
        self.img_fundo = pygame.transform.scale(img_fundo_crua, (140, 240))
        self.img_barra = pygame.transform.scale(img_barra_crua, (140, 120))
        self.img_peixe = pygame.transform.scale(img_peixe_crua, (40, 45))
        self.img_barra_2 = pygame.transform.scale(img_barra_2, (140, 240))
        self.img_cauda = pygame.transform.scale(img_cauda_crua, (130, 190))
        self.img_progresso = pygame.transform.scale(img_progresso, (22, 180))
        self.img_coroa = pygame.transform.scale(img_coroa, (50, 50))

        

        self.fundo_rect = self.img_fundo.get_rect()
        self.barra_rect = self.img_barra.get_rect()
        self.peixe_rect = self.img_peixe.get_rect()
        self.barra_rect = self.img_barra.get_rect()
        self.cauda_rect = self.img_cauda.get_rect()
        self.progresso_rect = self.img_progresso.get_rect()
        self.coroa_rect = self.img_coroa.get_rect()

        self.fundo_rect.center = (650, 400)
#Posições X
        self.barra_rect.centerx = self.fundo_rect.centerx   
        self.peixe_rect.centerx = self.fundo_rect.centerx - 44
        self.cauda_rect.centerx = self.fundo_rect.centerx - 3
        self.progresso_rect.centerx = self.fundo_rect.centerx  - 90
        self.coroa_rect.centerx = self.fundo_rect.centerx - 90
#posiçoes Y
        self.barra_rect.bottom = self.fundo_rect.bottom - 10
        self.peixe_rect.centery = self.fundo_rect.centery
        self.cauda_rect.centery = self.fundo_rect.centery + 20 
        self.progresso_rect.centery = self.fundo_rect.centery + 20
        self.coroa_rect.centery = self.fundo_rect.centery   - 90

#Variáveis para o movimento da barra

        self.velocidade_barra = 0
        self.gravidade = 0.4
        self.forca_clique = 0.8
        self.atrito = 0.95
#Variáveis para o movimento do peixe
        self.velocidade_peixe = 2
        self.raridade_taxa_ganho = 0.5
        self.raridade_taxa_perda = 0.7

        self.direção_peixe = 1
        self.tempo = pygame.time.get_ticks()

        

        self.progresso = 30.0
        self.estado_jogo = "jogando"
        self.peixe_pescado = None
        self.peixe_pescado_rect = None
        self.estrela_pescado = None
        self.estrela_pescado_rect = None
        self.raridade_pescada = None
        self.esperar_soltar_rato = False

    def atualizar(self):
        if self.estado_jogo == "resultado":
            rato_pressionado = pygame.mouse.get_pressed()[0]
            if self.esperar_soltar_rato:
                if not rato_pressionado:
                    self.esperar_soltar_rato = False
            elif rato_pressionado:
                self.estado_jogo = "fechado"
            return

        if self.estado_jogo != "jogando":
            return
        
        if pygame.mouse.get_pressed()[0]:
            self.velocidade_barra -= self.forca_clique  
        else:
            self.velocidade_barra += self.gravidade  # somar Y

        # criar atrito
        self.velocidade_barra *= self.atrito
        self.barra_rect.y += self.velocidade_barra

        # limitar a barra
        if self.barra_rect.top < self.fundo_rect.top - 14:
            self.barra_rect.top = self.fundo_rect.top - 14
            self.velocidade_barra = 0
        if self.barra_rect.bottom > self.fundo_rect.bottom + 47:
            self.barra_rect.bottom = self.fundo_rect.bottom + 47
            self.velocidade_barra = 0

        # randomizar o movimento do peixe
        agora = pygame.time.get_ticks()
        if agora - self.tempo > random.randint(1000, 2000): 
            self.direção_peixe = random.choice([-1, 1, 0 -1.5, 1.5, 0.5])
            self.tempo = agora

        self.peixe_rect.y += self.velocidade_peixe * self.direção_peixe

        # limitar o peixe
        if self.peixe_rect.top < self.fundo_rect.top:
            self.peixe_rect.top = self.fundo_rect.top 
            self.direção_peixe = 1
        if self.peixe_rect.bottom > self.fundo_rect.bottom:
            self.peixe_rect.bottom = self.fundo_rect.bottom 
            self.direção_peixe = -1


        if self.barra_rect.colliderect(self.peixe_rect):
           
            self.progresso += self.raridade_taxa_ganho
        else:
            self.progresso -= self.raridade_taxa_perda

        if self.progresso >= 100:
            self.progresso = 100
            self.mostrar_peixe_pescado()
            print("Parabéns! Você pescou um peixe!")

        if self.progresso <= 0:
            self.progresso = 0
            self.estado_jogo = "perdeu"
            print("Oh não! O peixe escapou!")
        





    def mostrar_peixe_pescado(self):
        self.raridade_pescada, nome_peixe = raridades()
        imagem = pygame.image.load(os.path.join("Sprites", nome_peixe)).convert_alpha()
        centro_resultado = self.tela.get_rect().center
        area_visivel = imagem.get_bounding_rect()
        imagem = imagem.subsurface(area_visivel).copy()
        tamanho_peixe = int(imagem.get_width() * 4)
        tamanho_estrela = 400
        self.peixe_pescado = pygame.transform.scale(imagem, (tamanho_peixe, tamanho_peixe))
        self.peixe_pescado_rect = self.peixe_pescado.get_rect(center=centro_resultado)
        self.estrela_pescado = self.criar_estrela(tamanho_estrela)
        self.estrela_pescado_rect = self.estrela_pescado.get_rect(center=centro_resultado)
        self.estado_jogo = "resultado"
        self.esperar_soltar_rato = True

    def criar_estrela(self, tamanho):
        cores_por_raridade = {
            "Comum": (0, 190, 70),
            "Raro": (40, 120, 255),
            "Épico": (150, 60, 220),
            "Lendário": (255, 220, 0),
        }

        superficie = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        centro = tamanho / 2
        raio_externo = tamanho * 0.48
        raio_interno = tamanho * 0.22
        pontos = []

        for i in range(10):
            angulo = math.radians(-90 + i * 36)
            raio = raio_externo if i % 2 == 0 else raio_interno
            x = centro + math.cos(angulo) * raio
            y = centro + math.sin(angulo) * raio
            pontos.append((x, y))

        cor = cores_por_raridade[self.raridade_pescada]
        pygame.draw.polygon(superficie, cor, pontos)
        return superficie

    def desenhar(self):
        if self.estado_jogo == "resultado":
            if self.estrela_pescado is not None:
                self.tela.blit(self.estrela_pescado, self.estrela_pescado_rect)
            if self.peixe_pescado is not None:
                self.tela.blit(self.peixe_pescado, self.peixe_pescado_rect)
            return

        if self.estado_jogo != "jogando":
            return

        self.tela.blit(self.img_cauda, self.cauda_rect)
        self.tela.blit(self.img_fundo, self.fundo_rect)
        self.tela.blit(self.img_barra, self.barra_rect)
        self.tela.blit(self.img_peixe, self.peixe_rect)
        self.tela.blit(self.img_barra_2, self.fundo_rect)
        self.tela.blit(self.img_progresso, self.progresso_rect)
        self.tela.blit(self.img_coroa, self.coroa_rect)

        if self.progresso >= 0:
            
            largura_branca = 14
            altura_maxima = 172
            altura_atual =  int((self.progresso / 100) * altura_maxima)

            x_branco = self.progresso_rect.centerx - largura_branca // 2
            y_branco = self.progresso_rect.bottom - altura_atual - 4
            rect_branco = pygame.Rect(x_branco, y_branco, largura_branca, altura_atual)

            pygame.draw.rect(self.tela, (255, 255, 255), rect_branco)
