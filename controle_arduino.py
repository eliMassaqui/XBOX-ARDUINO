import pygame
import serial
import time
import sys

# Configuração Serial
try:
    # Altere 'COM3' para a porta onde seu Arduino está conectado
    ser = serial.Serial('COM4', 115200, timeout=0.1)
    time.sleep(2) 
except:
    print("Erro: Arduino não encontrado. Verifique a porta COM no Gerenciador de Dispositivos.")
    sys.exit()

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Erro: Nenhum controle encontrado.")
    sys.exit()

controle = pygame.joystick.Joystick(0)
controle.init()

print(f"--- Bridge Iniciada: {controle.get_name()} ---")
print("RT: Acelera (Direita) | LT: Ré (Esquerda) | A: Led Azul | B: Led Vermelho")

try:
    while True:
        pygame.event.pump()

        # --- LÓGICA REALISTA DOS GATILHOS (RT e LT) ---
        # No Xbox, eixos 4 e 5: -1.0 (solto) a 1.0 (pressionado)
        lt = (controle.get_axis(4) + 1) / 2 # Normaliza 0.0 a 1.0
        rt = (controle.get_axis(5) + 1) / 2 # Normaliza 0.0 a 1.0

        # Cálculo de direção: 90° é o centro. 
        # RT soma até +90°, LT subtrai até -90°
        posicao_servo = 90 + (rt * 90) - (lt * 90)
        posicao_servo = max(0, min(180, int(posicao_servo))) # Garante limite de 0-180

        # Envia comando do Servo (Ex: S120)
        ser.write(f"S{posicao_servo}\n".encode())

        # --- LÓGICA DOS BOTÕES (A e B) ---
        for evento in pygame.event.get():
            if evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == 0: # Botão A
                    ser.write(b"A1\n")
                    print("Botão A: LED Azul ON")
                if evento.button == 1: # Botão B
                    ser.write(b"B1\n")
                    print("Botão B: LED Vermelho ON")
            
            if evento.type == pygame.JOYBUTTONUP:
                if evento.button == 0: # Botão A Solto
                    ser.write(b"A0\n")
                if evento.button == 1: # Botão B Solto
                    ser.write(b"B0\n")

        time.sleep(0.015) # ~60Hz para resposta imediata e estável

except KeyboardInterrupt:
    print("\nEncerrando...")
    ser.close()
    pygame.quit()