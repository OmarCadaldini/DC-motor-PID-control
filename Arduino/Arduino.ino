#define pin_a 2
#define pin_b 3
#define EN_pin 5
#define Ts_ms 100

int current_a;
int last_a;
int current_b;
int last_b;
volatile int32_t alpha=0;

void setup()
{
  //interrupt a
  pinMode(pin_a,INPUT_PULLUP);
  last_a=digitalRead(pin_a);
  attachInterrupt(digitalPinToInterrupt(pin_a), ISR_a, CHANGE);
  //interrupt b
  pinMode(pin_b,INPUT_PULLUP);
  last_b=digitalRead(pin_b);
  attachInterrupt(digitalPinToInterrupt(pin_b), ISR_b, CHANGE);
  //serial
  Serial.begin(500000);
  Serial.setTimeout(0.1);
  while(!Serial);
  //enable pin
  pinMode(EN_pin,INPUT_PULLUP);
}

void loop()
{
  if(digitalRead(EN_pin)==LOW)
  {
    delay(Ts_ms);
    Serial.println(alpha);
  }
  else alpha=0;
}

void ISR_a()
{
  current_b=digitalRead(pin_b);
  current_a=digitalRead(pin_a);
  if (current_a==1)//rising edge
  {
    if (current_b==0)
      alpha++;
    else
      alpha--;
  }
  else//falling edge
  {
    if (current_b==0)
      alpha--;
    else
      alpha++;
  }
  last_a=current_a;
  last_b=current_b;
}

void ISR_b()
{
  current_a=digitalRead(pin_a);
  current_b=digitalRead(pin_b);
  if(current_b==1)//rising edge
  {
    if(current_a==0)
      alpha--;
    else
      alpha++;
  }
  else//falling edge
  {
    if(current_a==0)
      alpha++;
    else
      alpha--;
  }
  last_a=current_a;
  last_b=current_b;
}
