//SCRIPT DE NAVEGACAO PARA ROBO COM ENCODER OTICO E MOTOR DC
//Vitor Domingues
//https://github.com/vitorshaft

//diametroRoda = 38 mm
//perimetroRoda = 119,38 mm
//distancia entre rodas = 115 mm
//perimetroRadial = 722,57 mm = 6 voltas
//perimetroAxial = 361,28 mm = 3 voltas cada roda

#include <EEPROM.h>
#include <Math.h>
#include <Coordinates.h>
//instancia o obj point da lib Coordinates
Coordinates point = Coordinates();

//EEPROM.write(0,0);
//EEPROM.write(1,0);

const int stepsPR = 2048;
int endX = 0;
int endY = 1;
int endAng = 2;
int a[2] = {0,0};
float multip = 120;
int rpp = 8; //pulsos por rotação

//pinos dos encoders
#define irDir 2 //direito
#define irEsq 3 //esquerdo
//pinos de PWM - potencia dos motores
//PWM: 3,5,6,9,10,11
#define pwmDir 11
#define pwmEsq 10
//pinos do motor esquerdo
#define in1 5
#define in2 6
//pinos do motor direito
#define in3 7
#define in4 8

//variaveis para contagem de pulsos
int pDir;
int pEsq;

//retorna deslocamento absoluto do motor DIREITO
int contadorD(){
  pDir++;
  //Serial.print("Direita: ");
  //Serial.println(pDir);
  
  return pDir;
}
//retorna deslocamento absoluto do motor ESQUERDO
int contadorE(){
  pEsq++;
  //Serial.print("Esquerda: ");
  //Serial.println(pEsq);
  return pEsq;
}

float esquerdo(int d){
  pEsq = 0;
  int setPoint = d/15;
  while(pEsq <= setPoint){
    analogWrite(pwmEsq, 200);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    Serial.println(pEsq);
  }  
  analogWrite(pwmEsq, 0);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  Serial.println("parada");
}
float direito(int d){
  pDir = 0;
  int setPoint = d/15;
  while(pDir <= setPoint){
    analogWrite(pwmDir, 200);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    Serial.println(pDir);
  }
  analogWrite(pwmDir, 0);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  Serial.println(pDir);  
}

float frente(int mm){
  pEsq = 0;
  pDir = 0;
  int setPoint = mm/15;
  while(pEsq <= setPoint || pDir <= setPoint){
    char s = Serial.read();
    if (s == '9') break;
    analogWrite(pwmEsq, 200);
    analogWrite(pwmDir, 200);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    Serial.print(pEsq);
    Serial.print(",");
    Serial.println(pDir);    
  }
  analogWrite(pwmEsq, 0);
  analogWrite(pwmDir, 0);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  return mm;
}
void tras(int mm){
  pEsq = 0;
  pDir = 0;
  int setPoint = mm/15;
  while(pEsq <= setPoint || pDir <= setPoint){
    char s = Serial.read();
    if (s == '9') break;
    analogWrite(pwmEsq, 200);
    analogWrite(pwmDir, 200);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    Serial.print(pEsq);
    Serial.print(",");
    Serial.println(pDir);    
  }
  analogWrite(pwmEsq, 0);
  analogWrite(pwmDir, 0);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  return mm;
}

void esqAx(int graus){
  pEsq = 0;
  pDir = 0;
  int setPoint = graus/15;
  while(pEsq <= setPoint || pDir <= setPoint){
    char s = Serial.read();
    if (s == '9') break;
    analogWrite(pwmEsq, 150);
    analogWrite(pwmDir, 150);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    Serial.print(pEsq);
    Serial.print(",");
    Serial.println(pDir);    
  }
  analogWrite(pwmEsq, 0);
  analogWrite(pwmDir, 0);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  }

void dirAx(int graus){
  pDir = 0;
  pEsq = 0;
  int setPoint = graus/15;
  while(pDir <= setPoint || pEsq <= setPoint){
    char s = Serial.read();
    if (s == '9') break;
    analogWrite(pwmEsq, 150);
    analogWrite(pwmDir, 150);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    Serial.print(pEsq);
    Serial.print(",");
    Serial.println(pDir);    
  }
  analogWrite(pwmEsq, 0);
  analogWrite(pwmDir, 0);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  }
  
void esqRad(int graus){
  pEsq = 0;
  pDir = 0;
  int setPoint = graus/7.5;
  while(pDir <= setPoint){
    char s = Serial.read();
    if (s == '9') break;
    analogWrite(pwmDir, 150);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    Serial.println(pDir);    
  }
  analogWrite(pwmDir, 0);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void dirRad(int graus){
  pEsq = 0;
  pDir = 0;
  int setPoint = graus/7.5;
  while(pEsq <= setPoint){
    char s = Serial.read();
    if (s == '9') break;
    analogWrite(pwmEsq, 150);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    Serial.println(pEsq);    
  }
  analogWrite(pwmEsq, 0);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

void deslocPolar(int d, int ang){
   float xx = EEPROM.read(0);
   float yy = EEPROM.read(1);
   float alfa = EEPROM.read(2);
   alfa = alfa+ang;
   if(alfa < 0){
    alfa = 360.0-alfa;
   }
   else if(alfa > 360){
    alfa = alfa-360.0;
   }
   if(ang > 0) esqRad(ang);
   else dirRad(ang*(-1));
   delay(1000);
   float dd = (float)frente(d);
   float phi = (alfa*71)/4068.0;
   point.fromPolar(dd,phi);
   float pX = point.getX();
   float pY = point.getY();
   Serial.print("x,y calculados ");
   Serial.print(pX);
   Serial.print(",");
   Serial.println(pY);
   float xf = xx+ pX;
   float yf = yy+ pY;
   alfa = alfa-ang;
   EEPROM.write(0,xf);
   EEPROM.write(1,yf);
   EEPROM.write(2,alfa);
   //writePos(xx,yy);  
}
void pipf(float x, float y){
  float xi = (float) EEPROM.read(0);
  float yi = (float) EEPROM.read(1);
  float ang = EEPROM.read(2);
  float dx = x-xi;
  float dy = y-yi;
  point.fromCartesian(dx,dy);
  float R = 10*point.getR();
  float alfa = point.getAngle();
  float dAlfa = alfa-ang;
  R = (int) R;
  if(dAlfa > 0){
    float graus = (dAlfa*4068.0)/71;
    graus = (int) graus;
    esqAx(graus);
    frente(R);
    EEPROM.write(0,x);
    EEPROM.write(1,y);
    EEPROM.write(2,alfa);
  }
  else if(dAlfa < 0){
    float graus = (dAlfa*(-4068.0))/71;
    graus = (int) graus;
    dirAx(graus);
    frente(R);
    EEPROM.write(0,x);
    EEPROM.write(1,y);
    EEPROM.write(2,alfa);
  }
  else{
    frente(R);
    EEPROM.write(0,x);
    EEPROM.write(1,y);
    EEPROM.write(2,alfa);
  }
  
}

void setup() {
  //EEPROM.write(0,0);
  //EEPROM.write(1,0);

  pinMode(irDir,INPUT);
  pinMode(irEsq,INPUT);
  pinMode(13,OUTPUT);

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(pwmEsq, OUTPUT);
  pinMode(pwmDir, OUTPUT);
  
  //adiciona detecção de interrupção a cada sinal MUDANDO nos pinos 2 e 3
  //LOW, CHANGE, RISING, FALLING;
  attachInterrupt(digitalPinToInterrupt(2), contadorD, CHANGE);
  attachInterrupt(digitalPinToInterrupt(3), contadorE, CHANGE);
  
  // Begin Serial communication at a baud rate of 9600:
  Serial.begin(9600);
  //esquerdo(1);
  //direito(1);
  //frente(1);
}

void loop() {
  // Step one revolution in one direction:
  
  if(Serial.available()){
    
    int ler = Serial.read();
    Serial.println(ler);
    if(ler == '0'){
    //Serial.println("frente");
    frente(150);
    delay(500);
    }
    else if(ler == '1'){
    // Step one revolution in the other direction:
    //Serial.println("tras");
    tras(150);
    delay(500);
    }
    else if(ler == '2'){
      //Serial.println("esquerda");
      esqRad(8);
      Serial.print('a');
      
      delay(500);
    }
    else if(ler == '3'){
      Serial.println("direita");
      dirRad(8);
      delay(500);
    }
    
    else if(ler == '4'){
      //int r,s = readPos();
      float r = EEPROM.read(0);
      float s = EEPROM.read(1);
      Serial.print(r);
      Serial.print(',');
      Serial.println(s);
      deslocPolar(90,45);
      //r,s = readPos();
      r = EEPROM.read(0);
      s = EEPROM.read(1);
      Serial.print(r);
      Serial.print(',');
      Serial.println(s);
      delay(1500);
    }
    
    else if(ler == '5'){
      float r = EEPROM.read(0);
      float s = EEPROM.read(1);
      float t = EEPROM.read(2);
      Serial.print(r);
      Serial.print(',');
      Serial.print(s);
      Serial.print(',');
      Serial.println(t);
      deslocPolar(90,-30);
      r = EEPROM.read(0);
      s = EEPROM.read(1);
      Serial.print(r);
      Serial.print(',');
      Serial.print(s);
      Serial.print(',');
      Serial.println(t);
      //multip = multip+60;
      delay(1500);
    }
    
    else if(ler == '7'){
      EEPROM.write(0,0);
      EEPROM.write(1,0);
      EEPROM.write(2,0);
      //Serial.println("EEPROM zerada");
    }
    else if(ler = '8'){
      Serial.println(EEPROM.read(0));
      Serial.println(EEPROM.read(1));
      Serial.println(EEPROM.read(2));
      Serial.println(pEsq);
      Serial.println(pDir);
    }
    else{
      //Serial.write("nenhum comando recebido");
      delay(500);
    }
  
  }
}
