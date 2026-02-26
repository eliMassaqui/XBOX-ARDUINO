# 🎮 ARDUINO XBOX BRIDGE + SERVO 🤖

## Objetivo
Controlar Arduino via Xbox Controller.

## Funcionalidades
- **RT** → Acelera / **LT** → Ré  
- **Botão A** → LED Azul  
- **Botão B** → LED Vermelho  
- **Servo:** 0°–180° baseado em gatilhos  
- Comunicação Serial robusta (~60Hz)

---

## 🛠 Configuração Serial / Python
- **Porta COM do Arduino:** `'COM3'` (alterar conforme necessário)  
- **Baudrate:** 115200  
- **Bibliotecas Python:** `pygame`, `serial`  
- Deadzone e normalização aplicada aos gatilhos  

**Exemplo de mapeamento:**
- RT: soma +90°  
- LT: subtrai -90°  
- 90° = centro

---

## 📜 Código Python (Bridge)

```python
import pygame
import serial
import time
import sys

# ───── SERIAL ─────
try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    time.sleep(2)
except:
    print("Erro: Arduino não encontrado.")
    sys.exit()

# ───── INICIALIZAÇÃO PYGAME ─────
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Nenhum controle encontrado.")
    sys.exit()

controle = pygame.joystick.Joystick(0)
controle.init()
print(f"--- Bridge Iniciada: {controle.get_name()} ---")

try:
    while True:
        pygame.event.pump()

        # ───── GATILHOS ─────
        lt = (controle.get_axis(4) + 1) / 2
        rt = (controle.get_axis(5) + 1) / 2
        posicao_servo = 90 + (rt*90) - (lt*90)
        posicao_servo = max(0, min(180, int(posicao_servo)))
        ser.write(f"S{posicao_servo}\n".encode())

        # ───── BOTÕES ─────
        for evento in pygame.event.get():
            if evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == 0:
                    ser.write(b"A1\n"); print("A: LED Azul ON")
                if evento.button == 1:
                    ser.write(b"B1\n"); print("B: LED Vermelho ON")
            if evento.type == pygame.JOYBUTTONUP:
                if evento.button == 0: ser.write(b"A0\n")
                if evento.button == 1: ser.write(b"B0\n")

        time.sleep(0.015)  # ~60Hz

except KeyboardInterrupt:
    print("Encerrando...")
    ser.close()
    pygame.quit()
```

```cpp
#include <Servo.h>

Servo meuServo;
const int pinServo = 6;
const int pinAzul = 9;
const int pinVermelho = 10;

void setup() {
  Serial.begin(115200);
  meuServo.attach(pinServo);
  pinMode(pinAzul, OUTPUT);
  pinMode(pinVermelho, OUTPUT);

  // Centro + Feedback visual
  meuServo.write(90);
  digitalWrite(pinAzul, HIGH);
  digitalWrite(pinVermelho, HIGH);
  delay(500);
  digitalWrite(pinAzul, LOW);
  digitalWrite(pinVermelho, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando == 'S') {
      int valor = Serial.parseInt();
      meuServo.write(valor);
    } 
    else if (comando == 'A') {
      int estado = Serial.parseInt();
      digitalWrite(pinAzul, estado);
    } 
    else if (comando == 'B') {
      int estado = Serial.parseInt();
      digitalWrite(pinVermelho, estado);
    }
  }
}
```
