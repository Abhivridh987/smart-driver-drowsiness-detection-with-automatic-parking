
void setup() {
  Serial.begin(115200);

  int a = 10;
  int b = 20;
  int sum = a + b;

  Serial.print("First number: ");
  Serial.println(a);

  Serial.print("Second number: ");
  Serial.println(b);

  Serial.print("Sum = ");
  Serial.println(sum);

  
}

void loop() {
}

