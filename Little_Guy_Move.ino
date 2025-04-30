// ELEGOO Conqueror Tank: Arduino Serial Motor Control
// Matches Pi Python test script (sending F, B, L, R, S)

const int ENB = 5;    // Left motor speed control (PWM)
const int ENA = 6;    // Right motor speed control (PWM)
const int IN1 = 7;    // Right motor direction
const int IN2 = 8;    // Left motor direction
const int STBY = 3;   // Motor driver standby control

const int SPEED = 100; // PWM Speed (0–255)

void setup() {
  // Set pin modes
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(STBY, OUTPUT);

  Serial.begin(115200);
  while (!Serial);  // Wait for Serial (optional)

  // Enable motor driver
  digitalWrite(STBY, HIGH);
  stopMotors();
  Serial.println("Arduino ready");  // Respond for Pi auto-detect
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.length() == 0) return;

    char c = cmd.charAt(0);
    switch (c) {
      case 'F': moveForward(); Serial.println("ACK F"); break;
      case 'B': moveBackward(); Serial.println("ACK B"); break;
      case 'L': turnLeft(); Serial.println("ACK L"); break;
      case 'R': turnRight(); Serial.println("ACK R"); break;
      case 'S': stopMotors(); Serial.println("ACK S"); break;
      case '?': Serial.println("ACK ?"); break;  // Pi probe response
      default: Serial.println("ERR"); break;
    }
  }
}

// Movement functions
void moveForward() {
  digitalWrite(IN1, HIGH);  // Right motor forward
  digitalWrite(IN2, HIGH);  // Left motor forward
  analogWrite(ENA, SPEED);
  analogWrite(ENB, SPEED);
}

void moveBackward() {
  digitalWrite(IN1, LOW);   // Right motor backward
  digitalWrite(IN2, LOW);   // Left motor backward
  analogWrite(ENA, SPEED);
  analogWrite(ENB, SPEED);
}

void turnLeft() {
  digitalWrite(IN1, LOW);   // Right motor backward
  digitalWrite(IN2, HIGH);  // Left motor forward
  analogWrite(ENA, SPEED);
  analogWrite(ENB, SPEED);
}

void turnRight() {
  digitalWrite(IN1, HIGH);  // Right motor forward
  digitalWrite(IN2, LOW);   // Left motor backward
  analogWrite(ENA, SPEED);
  analogWrite(ENB, SPEED);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}