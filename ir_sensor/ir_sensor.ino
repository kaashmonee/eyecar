void setup() {
  pinMode(A0, INPUT);
  pinMode(3, OUTPUT);
  pinMode(A4, INPUT);
  pinMode(A3, INPUT);
  Serial.begin(9600);
  digitalWrite(3, HIGH);
}

void loop() {
  /*Serial.println("HIGH");
  digitalWrite(3, HIGH);
  delay(100);
  Serial.println(analogRead(0));
  delay(100);
  Serial.println("LOW");
  digitalWrite(3, LOW);
  delay(100);
  Serial.println(analogRead(0));
  delay(100);*/
  Serial.print("A0:");
  Serial.println(analogRead(A0));
  Serial.print("A4:");
  Serial.println(analogRead(A4));
  Serial.print("A3:");
  Serial.println(analogRead(A3));
  delay(100);
}

