#define ADC_PIN 1          
#define NUM_SAMPLES 200     
#define ADC_RESOLUTION 4095 
#define VREF 3.3            

#define VOLTAGE_FACTOR 2.0  

// Koefisien kalibrasi hasil pengukuran kamu
#define CAL_A 0.85   // slope
#define CAL_B 0.22   // offset

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  Serial.println("Kalibrasi ADC dengan filter linear aktif...");
}

void loop() {
  long totalADC = 0;

  for (int i = 0; i < NUM_SAMPLES; i++) {
    totalADC += analogRead(ADC_PIN);
    delayMicroseconds(200);
  }

  float avgADC = totalADC / (float)NUM_SAMPLES;

  // Tegangan hasil pembacaan ADC
  float voltageADC = (avgADC / ADC_RESOLUTION) * VREF;
  
  // Tegangan input hasil pembagi tegangan
  float voltageMeasured = voltageADC * VOLTAGE_FACTOR;

  // Terapkan filter kalibrasi
  float voltageFiltered = (CAL_A * voltageMeasured) + CAL_B;

  // Batasi agar tidak lebih dari 4.2 V
  // if (voltageFiltered > 4.2) voltageFiltered = 4.2;
  if (voltageFiltered < 0) voltageFiltered = 0;
  

  // Serial.print("ADC: ");
  // Serial.print(avgADC);
  // Serial.print(" | Vadc: ");
  // Serial.print(voltageADC, 2);
  // Serial.print(" | Vin (measured): ");
  // Serial.print(voltageMeasured, 2);
  // Serial.print(" | Vin (filtered): ");
  
  Serial.println(voltageFiltered, 2);

  delay(10);
}
