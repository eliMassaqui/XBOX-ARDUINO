import pygame
import serial
import time

# Configuração Serial - Ajuste a porta COM conforme seu Gerenciador de Dispositivos
try:
    ser = serial.Serial('COM4', 115200, timeout=0.1)
    time.sleep(2) 
except:
    print("Erro: Arduino não encontrado. Verifique a porta COM.")
    exit()

pygame.init()
pygame.joystick.init()
controle = pygame.joystick.Joystick(0)
controle.init()

print("Controlando Arduino via Xbox Controller...")

try:
    while True:
        pygame.event.pump()

        # --- LÓGICA DO SERVO (RT) ---
        # RT no Pygame vai de -1 (solto) a 1 (pressionado)
        rt_raw = controle.get_axis(5)
        # Mapeia -1...1 para 0...180 graus
        servo_pos = int(((rt_raw - 1) / 2) * 180)
        ser.write(f"S{servo_pos}\n".encode())

        # --- LÓGICA DOS BOTÕES (A e B) ---
        for evento in pygame.event.get():
            if evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == 0: # Botão A
                    ser.write(b"A1\n")
                if evento.button == 1: # Botão B
                    ser.write(b"B1\n")
            
            if evento.type == pygame.JOYBUTTONUP:
                if evento.button == 0: # Botão A solto
                    ser.write(b"A0\n")
                if evento.button == 1: # Botão B solto
                    ser.write(b"B0\n")

        time.sleep(0.02) # ~50Hz é suficiente para servos e estável para a serial

except KeyboardInterrupt:
    ser.close()
    pygame.quit()