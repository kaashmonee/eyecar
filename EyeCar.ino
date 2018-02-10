#define MOTORPIN1 3
#define MOTORPIN2 6

void setup() {
  pinMode(MOTORPIN1, OUTPUT);
  pinMode(MOTORPIN2, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  digitalWrite(13, HIGH);
  digitalWrite(12, LOW);
}

void loop() {
  analogWrite(MOTORPIN1, 220);
  analogWrite(MOTORPIN2, 220);
  delay(3000);
  analogWrite(MOTORPIN1, 0);
  analogWrite(MOTORPIN2, 0);
  delay(1000);
}
