import pygame
import os

class GatoPescador:
    
    def __init__(self, tela_jogo, x, y):
        self.tela = tela_jogo
        self.x = x
        self.y = y
        self.estado = "idle"

        
        self.animaçoes = {
            "sleeping": self.carregar_animaçoes("gato_sleep"),
            "waking up": self.carregar_animaçoes("gato_wake"),
            "idle": self.carregar_animaçoes("gato_idle"),
        }

        self.frame_atual = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()

        self.velocidade = {
            "idle": 400,
            "sleeping": 300,
            "waking up": 200
        }
        
        self.direcao_ping_pong = 1 
        self.tempo_ultima_atividade = pygame.time.get_ticks()
        self.tempo_para_dormir = 20000

    def carregar_animaçoes(self, nome_prefixo):
        lista_frames = []
        i = 0
        while True:
            caminhos = os.path.join("Sprites", "gato_base", f"{nome_prefixo}{i}.png")
            
            if os.path.exists(caminhos):
                img = pygame.image.load(caminhos).convert_alpha()
                img = pygame.transform.scale(img, (250, 250))
                lista_frames.append(img)
                i += 1 
            else:
                break 
                
        return lista_frames
    
    def registro_atividade(self):
        self.tempo_ultima_atividade = pygame.time.get_ticks()
        if self.estado == "sleeping":
           self.estado = "waking up"
           self.frame_atual = 0

    def atualizar(self):
        agora = pygame.time.get_ticks()

        if self.estado == "idle" and (agora - self.tempo_ultima_atividade > self.tempo_para_dormir):
            self.estado = "sleeping"
            self.frame_atual = 0
            self.direcao_ping_pong = 1

        if self.estado == "waking up":
            frames_totais = len(self.animaçoes["waking up"])
            if frames_totais > 0 and self.frame_atual >= frames_totais - 1:
                self.estado = "idle"
                self.frame_atual = 0

        velocidade_atual = self.velocidade[self.estado]
        if agora - self.tempo_ultimo_frame > velocidade_atual:
            lista_atual = self.animaçoes[self.estado]
            
            if not lista_atual:
                return

            if self.estado == "sleeping":
                self.frame_atual += self.direcao_ping_pong
                if self.frame_atual >= len(lista_atual) - 1:
                    self.frame_atual = len(lista_atual) - 1
                    self.direcao_ping_pong = -1
                elif self.frame_atual <= 0:
                    self.frame_atual = 0
                    self.direcao_ping_pong = 1

            elif self.estado == "idle":
                self.frame_atual = (self.frame_atual + 1) % len(lista_atual)

            else: # waking up
                if self.frame_atual < len(lista_atual) - 1:
                    self.frame_atual += 1

            self.tempo_ultimo_frame = agora

    def desenhar(self):
        lista_atual = self.animaçoes[self.estado]
        if lista_atual:
            sprite_atual = lista_atual[self.frame_atual]
            self.tela.blit(sprite_atual, (self.x, self.y))