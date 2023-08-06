
class Trigger {
  uint8_t pin_a;
  uint8_t pin_b;

public:
  Trigger(uint8_t _pin_a, uint8_t _pin_b) {
    pin_a = _pin_a;
    pin_b = _pin_b;
  }
  int32_t check() {
    uint32_t ts_dur = 0;
    uint32_t ts = micros();
    uint16_t a = analogRead(pin_a);
    uint16_t b = analogRead(pin_b);
    // printf("%d, %d, %d\n", a, b, ts);
    Serial.write(a>>8);
    Serial.write(a>>0);
    Serial.write(b>>8);
    Serial.write(b>>0);
    Serial.write(ts>>24);
    Serial.write(ts>>16);
    Serial.write(ts>>8);
    Serial.write(ts>>0);
    Serial.write('\n');

    return ts_dur;
  }
};

Trigger trigger(0, 1);

void setup() {
  Serial.begin(2000000);

  analogReadResolution(12);
}

void loop() {
  trigger.check();
}
