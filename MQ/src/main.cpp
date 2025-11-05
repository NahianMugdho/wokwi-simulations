#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
}
void loop() {
  int gasvalue = analogRead(4);
  Serial.print("Gas Sensor Value: ");
  Serial.print(gasvalue);

  delay(2000); 
}

