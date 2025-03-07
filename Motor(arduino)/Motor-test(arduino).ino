int motor1 = 4;


void setup()
{
  Serial.begin (9600);
  pinMode (motor1, OUTPUT);
}



void loop()
{
  digitalWrite(motor1, HIGH);
}

