#include "DHT.h"

#define DHTPIN 16
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  // Send as JSON-like string
  Serial.print("{\"temp\":");
  Serial.print(temp);
  Serial.print(",\"hum\":");
  Serial.print(hum);
  Serial.println("}");

  delay(2000);
}
