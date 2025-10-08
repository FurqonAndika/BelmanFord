
#define SENSOR_PIN 1

float sensorValue = 0.0;
float temp =0; 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(SENSOR_PIN, INPUT);
}

void loop() {
  // // put your main code here, to run repeatedly:
  //   for (int i = 0; i < 50; i++) {
  //     temp += analogRead(SENSOR_PIN);
  //     delay(1);
  //   }
  //   sensorValue = temp / 50.0;
  //   temp =0;
  //   delay(5);
  Serial.println("hello");
}   



