#define ENCODE_PIN_A 2
#define ENCODE_PIN_B 3

volatile unsigned int counter;

void setup() {
  Serial.begin(9600);
  
  // set encoder pins
  pinMode(ENCODE_PIN_A, INPUT);
  pinMode(ENCODE_PIN_B, INPUT);

  // turn on pull up resistors
  digitalWrite(ENCODE_PIN_A, HIGH); 
  digitalWrite(ENCODE_PIN_B, HIGH);

  // set interrupts for rising pulses sent from encoder
  attachInterrupt(0, a_pin_trigger, RISING);
  attachInterrupt(2, b_pin_trigger, RISING);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(counter);
}

float calc_speed(){
  return 0;
}

void a_pin_trigger() {
  
  // determine direction
  if( digitalRead(ENCODE_PIN_B) == LOW ) {
    counter++;
  } else {
    counter--;
  }
}

void b_pin_trigger() {
  
  if( digitalRead(ENCODE_PIN_A == LOW)) {
    counter--;
  } else {
    counter++;
  }
}
