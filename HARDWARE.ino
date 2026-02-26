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