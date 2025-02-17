const int analogPin = A3;
const int numReadings = 50;
const unsigned long interval = 10; // Interval between serial transmissions
unsigned long previousMillis = 0;

int readings[numReadings];
int readIndex = 0;
int total = 0;
int average = 0.0;

void setup() {
  Serial.begin(115200); // Initialize serial communication at 9600 baud rate
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0; // Initialize all readings to 0
  }
  pinMode(analogPin, INPUT);
}

void loop() {
  int sensorValue = analogRead(analogPin);
  total = total - readings[readIndex] + sensorValue;
  readings[readIndex] = sensorValue;
  readIndex = (readIndex + 1) % numReadings;

  average = total / numReadings;

  // Send the averaged value to the serial port at 100 Hz
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    Serial.println(average);
  }
}