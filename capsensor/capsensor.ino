// Pins for the capacitive sensors
int capSensePins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10};
int numSensors = 9;

void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop() {
  String output = ""; // Initialize an empty string to store the output

  for (int i = 0; i < numSensors; i++) {
    // Read the capacitance value from the current sensor
    int capacitanceValue = readCapacitivePin(capSensePins[i]);

    // Append the pin number and measurement to the output string
    if (i > 0) {
      output += ","; // Add a comma before each additional sensor reading
    }
    output += "pin" + String(capSensePins[i]) + ":" + String(capacitanceValue);
  }

  // Send the formatted string to the serial monitor
  Serial.println(output);

  delay(20); // Small delay between readings
}

// Simplified function to measure capacitance on a given pin
uint16_t readCapacitivePin(int pinToMeasure) {
  uint16_t cycles = 0;

  // Discharge the capacitor
  pinMode(pinToMeasure, OUTPUT);
  digitalWrite(pinToMeasure, LOW);
  delayMicroseconds(10); // Ensure the capacitor is fully discharged

  // Allow the capacitor to charge
  pinMode(pinToMeasure, INPUT);

  // Measure how long it takes for the pin to reach HIGH
  while (digitalRead(pinToMeasure) == LOW && cycles < 1000) {
    cycles++;
    delayMicroseconds(1); // Wait 1 microsecond per cycle
  }

  // Discharge the capacitor again
  pinMode(pinToMeasure, OUTPUT);
  digitalWrite(pinToMeasure, LOW);

  return cycles;
}