# Arduino Xbox Controller Bridge 🎮 🤖

Este projeto permite controlar um Arduino Uno utilizando um controle Xbox (ou compatíveis como o BSP-G6) via Bluetooth, utilizando Python como ponte (bridge) de comunicação Serial.

O diferencial deste projeto é o mapeamento realista que trata gatilhos analógicos, zonas mortas (deadzones) e a conversão de sinais para o padrão PWM do Arduino.

---

## 🚀 Funcionalidades

- **Mapeamento Fiel:** Identificação de todos os botões (A, B, X, Y, LB, RB, Start, Select).  
- **Analógicos Graduais:** Conversão de eixos (-1.0 a 1.0) para valores de 8 bits (0 a 255).  
- **Tratamento de Gatilhos:** Escalonamento dos gatilhos LT e RT de 0% a 100%.  
- **Comunicação Serial Robusta:** Protocolo de mensagens curtas para baixa latência.  
- **Filtro de Deadzone:** Evita movimentos involuntários causados por ruídos nos analógicos.

---

## 🛠️ Requisitos

### Hardware
- Arduino Uno (ou qualquer placa compatível)  
- Controle Xbox com suporte a Bluetooth (ou modo X-Input)  
- Cabo USB para conexão Arduino-PC  

### Software
- Python 3.x  
- Biblioteca **Pygame**: `pip install pygame`  
- Biblioteca **PySerial**: `pip install pyserial`  

---

## 🎮 Configuração do Controle

Para que o mapeamento funcione corretamente, o controle deve ser reconhecido pelo Windows como **Xbox Wireless Controller**.

1. Desligue o controle.  
2. Segure **RB + HOME** (ou a combinação específica do seu modelo) para entrar no modo X-Input.  
3. No Windows, execute `joy.cpl` para verificar se os botões respondem corretamente.

**Como resolver o modo do controle no BSP-G6:**

1. Desligue o Bluetooth do PC.  
2. Desligue o controle.  
3. Segure o botão **RB (R1)** e, enquanto segura, aperte **HOME** para ligar (as luzes devem piscar de forma diferente).  
4. Ligue o Bluetooth do PC e procure por um novo dispositivo. Se aparecer **Xbox Wireless Controller**, está pronto.

---

## 📜 Código Python: Mapeamento Realista

```python
import pygame
import sys

# Inicialização
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Erro: Nenhum controle de Xbox encontrado.")
    sys.exit()

controle = pygame.joystick.Joystick(0)
controle.init()

print(f"--- Mapeamento Xbox Realista: {controle.get_name()} ---")

# Dicionários de Tradução (Nomes reais do Controle)
MAPA_BOTOES = {
    0: "A", 1: "B", 2: "X", 3: "Y",
    4: "LB (Left Bumper)", 5: "RB (Right Bumper)",
    6: "BACK/VIEW", 7: "START/MENU",
    8: "L3 (Click Analógico Esq)", 9: "R3 (Click Analógico Dir)",
    10: "XBOX GUIDE"
}

try:
    while True:
        pygame.event.pump()

        # 1. ANALÓGICOS (Eixos)
        deadzone = 0.15

        # Analógico Esquerdo (Movimento)
        lx = controle.get_axis(0)
        ly = controle.get_axis(1)
        if abs(lx) > deadzone or abs(ly) > deadzone:
            print(f"Stick Esquerdo -> X: {lx:.2f} | Y: {ly:.2f}")

        # Analógico Direito (Câmera/Mira)
        rx = controle.get_axis(2)
        ry = controle.get_axis(3)
        if abs(rx) > deadzone or abs(ry) > deadzone:
            print(f"Stick Direito  -> X: {rx:.2f} | Y: {ry:.2f}")

        # 2. GATILHOS (LT e RT)
        lt = (controle.get_axis(4) + 1) / 2  # 0.0 a 1.0
        rt = (controle.get_axis(5) + 1) / 2  # 0.0 a 1.0
        
        if lt > 0.1: print(f"Gatilho LT: {int(lt*100)}%")
        if rt > 0.1: print(f"Gatilho RT: {int(rt*100)}%")

        # 3. BOTÕES DIGITAIS (Eventos)
        for evento in pygame.event.get():
            if evento.type == pygame.JOYBUTTONDOWN:
                nome_botao = MAPA_BOTOES.get(evento.button, f"Desconhecido ({evento.button})")
                print(f"Botão Pressionado: {nome_botao}")

            # 4. D-PAD (Setas/Hat)
            if evento.type == pygame.JOYHATMOTION:
                x, y = evento.value
                direcao = ""
                if y == 1: direcao = "Cima"
                elif y == -1: direcao = "Baixo"
                if x == 1: direcao += " Direita"
                elif x == -1: direcao += " Esquerda"
                if direcao: print(f"D-Pad: {direcao}")

        pygame.time.wait(10)  # 100 FPS para resposta imediata

except KeyboardInterrupt:
    print("\nMapeamento encerrado.")
    pygame.quit()
