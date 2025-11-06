#include <Arduino.h>

// ===== DIY IoT Hydrometer (Sonar → °Brix) =====
// Works on ESP32 or Arduino Uno
// Sensor: HC-SR04 or HY-SRF05
// Formula: °Brix = 3.8333 * distance(cm) - 9.5

#define TRIG_PIN 5     // ESP32 GPIO 5 (or D9 for Arduino)
#define ECHO_PIN 18    // ESP32 GPIO 18 (or D10 for Arduino)

float slope = 3.8333;  // calibration slope (m)
float intercept = -9.5; // calibration intercept (c)

// Function to measure distance from sonar (in cm)
float getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  // Convert time to distance (sound speed = 0.034 cm/μs)
  float distance = duration * 0.034 / 2.0;
  return distance;
}

// Convert distance (cm) to °Brix
float distanceToBrix(float distance) {
  float brix = slope * distance + intercept;
  if (brix < 0) brix = 0;  // clamp for sanity
  return brix;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.println("DIY IoT Hydrometer - Sonar to °Brix");
}

void loop() {
  float distance = getDistance();        // cm
  float brix = distanceToBrix(distance); // °Brix
  
  Serial.print("Distance: ");
  Serial.print(distance, 2);
  Serial.print(" cm  →  ");
  Serial.print(brix, 2);
  Serial.println(" °Brix");

  delay(5000); // take a reading every 5 seconds
}
