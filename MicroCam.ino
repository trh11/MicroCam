int XMot = 2;                                                                       //set pin 2 as x pulse pin
int YMot = 6;                                                                       //set pin 6 as y pulse pin
int ZMot = 10;                                                                      //set pin 10 as z pulse pin
                                                                                    //
int XDir = 3;                                                                       //set pin 3 as x direction pin
int YDir = 7;                                                                       //set pin 7 as y direction pin
int ZDir = 11;                                                                      //set pin 11 as z direction pin
                                                                                    //
int XEn = 4;                                                                        //
int YEn = 8;
int ZEn = 12;

int Cam = 14;
int mystery = 15;
                                                                                    //
#define raster_time 1                                                               //
                                                                                    //
String commands[5];                                                                 //create length 5 array to store commands
int steps[3];                                                                       //create length 3 array to store x, y, and z steps to make
int signed long track[3] ={0,0,0};                                                  //create array of absolute steps to track movement, oriented from x:0, y:0, z:0
char mots[3] = {'x','y','z'};                                                       //create array for motor character recognition
                                                                                    //
int motor_select(char sel){                                                         //definition that selects axis motor based on serial passed characters   
  switch(sel){                                                                      //direct by variable 'sel'
    case 'x':                                                                       //
      return XMot;                                                                  //
      break;                                                                        //
    case 'y':                                                                       //
      return YMot;                                                                  //
      break;                                                                        //
    case 'z':                                                                       //
      return ZMot;                                                                  //
      break;                                                                        //
    default:                                                                        //
      return 404;                                                                   //
      break;                                                                        //
  }                                                                                 //
}                                                                                   //
                                                                                    //
int dir_select(char sel) {                                                          //definition that selects axis motor direction based on serial passed characters
  switch(sel){                                                                      //
    case 'x':                                                                       //
      return XDir;                                                                  //
      break;                                                                        //
    case 'y':                                                                       //
      return YDir;                                                                  //
      break;                                                                        //
    case 'z':                                                                       //
      return ZDir;                                                                  //
      break;                                                                        //
    default:                                                                        //
      return 404;                                                                   //
      break;                                                                        //
  }                                                                                 //
}                                                                                   //
                                                                                    //
int mot_track(char sel) {                                                           //
  switch(sel){                                                                      //
    case 'x':                                                                       //
      return 0;                                                                     //
      break;                                                                        //
    case 'y':                                                                       //
      return 1;                                                                     //
      break;                                                                        //
    case 'z':                                                                       //
      return 2;                                                                     //
      break;                                                                        //
    default:                                                                        //
      return 404;                                                                   //
      break;                                                                        //
  }                                                                                 //
}                                                                                   //

void enable() {
  digitalWrite(XEn, LOW);
  digitalWrite(YEn, LOW);
  digitalWrite(ZEn, LOW);
}

void disable() {
  digitalWrite(XEn, HIGH);
  digitalWrite(YEn, HIGH);
  digitalWrite(ZEn, HIGH);
}
                                                                                    //
void photo() {                                                                      //
  delay(500);                                                                       //
  digitalWrite(mystery,LOW);
  delay(10);
  digitalWrite(Cam,LOW);                                                            //
  delay(50);                                                                       //
  digitalWrite(Cam,HIGH);
  delay(10);
  digitalWrite(mystery,HIGH);//
  delay(2000);                                                                      //
}                                                                                   //
                                                                                    //
void z_peck(int span, int part) {                                                   //
    digitalWrite(ZDir,LOW);                                                         //
    for (int l = 0; l < span/part; l++) {                                       //
      photo();                                                                      //
      for (int k = 0; k < part; k++) {                                              //
        if (pause() == 'S') {                                                       //
          break;                                                                    //
        }                                                                           //
        digitalWrite(ZMot,HIGH);                                                    //
        delay(2);                                                                   //
        digitalWrite(ZMot,LOW);                                                     //
        delay(2);                                                                   //
        track[2]--;                                                                 //
      }                                                                             //
    }                                                                               //
    photo();                                                                        //
    digitalWrite(ZDir,HIGH);                                                        //
    for (int k = 0; k < span; k++) {                                                //
      if (pause() == 'S') {                                                       //
        break;                                                                    //
      }                                                                           //
      digitalWrite(ZMot,HIGH);                                                      //
      delay(2);                                                                     //
      digitalWrite(ZMot,LOW);                                                       //
      delay(2);                                                                     //
      track[2]++;                                                                   //
    }                                                                               //
}                                                                                   //
                                                                                    //
void report(char fin) {                                                             //
  for (int n = 0; n < 5; n++){ 
    Serial.println(String(track[0])+","+String(track[1])+","+String(track[2])+","+fin); //   
  }     
}
                                                                                    //
char pause() {                                                                    //
  char check = Serial.read();
  if (check == 'P') {                                                               //
    bool pause = true;                                                              //
    report('s');                                                                    //
    while (pause == true){                                                          //
      char check2 = Serial.read();
      if (check2 == 'U'){                                                           //
        pause = false;                                                              //
      }                                                                             //
      if (check2 == 'S') {                                                          //
        pause = false;                                                              //
        return 'S';                                                                 //
      }                                                                             //
    }                                                                               //
  }                                                                                 //
  else if (check == 'S') {                                                          //
    return 'S';                                                                     //
  }                                                                                 //
  else {                                                                            //
    return 'U';                                                                     //
  }                                                                                 //
}                                                                                   //
                                                                                    //
void setup() {                                                                      //
  pinMode(XMot,OUTPUT);                                                             //
  pinMode(YMot,OUTPUT);                                                             //
  pinMode(ZMot,OUTPUT);                                                             //
  pinMode(XDir,OUTPUT);                                                             //
  pinMode(YDir,OUTPUT);                                                             //
  pinMode(ZDir,OUTPUT);                                                             //
  pinMode(XEn,OUTPUT);                                                              //
  pinMode(YEn,OUTPUT);                                                              //
  pinMode(ZEn,OUTPUT);                                                              //
  pinMode(Cam,OUTPUT);
  pinMode(mystery,OUTPUT);
  digitalWrite(Cam,HIGH);//
  digitalWrite(mystery,HIGH);
  Serial.begin(9600);                                                               //
  Serial.setTimeout(120);                                                           //
}                                                                                   //
                                                                                    //
void loop() {                                                                       //
  if (Serial.available() > 0){                                                      //
    String header = Serial.readStringUntil(',');                                    //
//    Serial.println(header);                                                       //
//**********************************ENABLE/DISABLE********************************* //
    if (header == "E") {
      enable();
    }
    if (header == "D") {
      disable();
    }
//************************************GO COMMANDS********************************** //     
    if (header == "G"){                                                             //
      for(int i =0; i < 5; i++){                                                    //
        String temp_cmd = Serial.readStringUntil(',');                              //
        if(temp_cmd.length()>0){                                                    //
          if (temp_cmd.charAt(0)=='@') {                                            //
            commands[3]=temp_cmd;                                                   //
          }                                                                         //
          else{                                                                     //
            commands[i]=temp_cmd;                                                   //
          }                                                                         //
        }                                                                           //
      }                                                                             //
      for (int k = 0; k < 3; k++) {                                                 //
        String temp_steps=(commands[k].substring(2));                               //
        steps[k]=temp_steps.toInt();                                                //
      }                                                                             //
                                                                                    //
      int freq = (commands[3].substring(1)).toInt();                                //
      while(steps[0] != 0 or steps[1] != 0 or steps[2] != 0) {                      //
        char check = pause();
        if (check == 'S') {                                                       //
          Serial.println(check);
          //report('s');                                                              //
          break;                                                                    //
        }                                                                           //
        for (int j = 0; j < 3; j++){                                                //
          char temp_mot = commands[j].charAt(0);                                    //
          if(commands[j].length() > 1){                                             //
            if (steps[j] != 0){                                                     //
              if (steps[j] > 0) {                                                   //
                digitalWrite(dir_select(temp_mot),HIGH);                            //
                steps[j]--;                                                         //
                track[j]++;                                                         //
              }                                                                     //
              else {                                                                //
                digitalWrite(dir_select(temp_mot),LOW);                             //
                steps[j]++;                                                         //
                track[j]--;                                                         //
              }                                                                     //
              digitalWrite(motor_select(temp_mot),HIGH);                            //
            }                                                                       //
          }                                                                         //
        }                                                                           //
        delay(500/freq);                                                            //
        for (int j = 0; j < 3; j++){                                                //
          char temp_mot = commands[j].charAt(0);                                    //
          if(commands[j].length() > 0){                                             //
            digitalWrite(motor_select(temp_mot),LOW);                               //
          }                                                                         //
        }                                                                           //
        delay(500/freq);                                                            //
      }                                                                             //
      report('s');                                                                  //
    }                                                                               //
//*******************************RASTER COMMANDS*********************************** //            
    if (header == "R") {                                                            //
      for(int n =0; n < 5; n++){                                                    //
        String temp_dem = Serial.readStringUntil(',');                              //
        if(temp_dem.length()>0){                                                    //
            commands[n]=temp_dem;                                                   //
        }                                                                           //
      }                                                                             //
      int w = commands[0].substring(2).toInt();                                     //
      int h = commands[1].substring(2).toInt();                                     //
      int d = commands[2].substring(2).toInt();                                     //
      int zs = commands[3].substring(2).toInt();                                    //
      int zd = commands[4].substring(2).toInt();                                    //
      digitalWrite(XDir, HIGH);                                                     //
      digitalWrite(YDir, HIGH);                                                     //
      int count = 0;                                                                //
      for (int j = 0; j < h/d + 1; j++) {                                           //
        for (int i = 0; i < w/d; i++) {                                             //
          z_peck(zs,zd);                                                            //
          for (int m = 0; m < d; m++) {                                             //
            if (pause() == 'S') {                                                       //
              break;                                                                    //
            }                                                                           //
            digitalWrite(XMot,HIGH);                                                //
            delay(raster_time);                                                     //
            digitalWrite(XMot,LOW);                                                 //
            delay(raster_time);                                                     //
          }                                                                         //
        }                                                                           //
        z_peck(zs,zd);                                                              //
        count++;                                                                    //
        if (j<h/d){                                                                 //
          for (int n = 0; n < d; n++) {                                             //
            if (pause() == 'S') {                                                       //
              break;                                                                    //
            }                                                                           //
            digitalWrite(YMot,HIGH);                                                //
            delay(raster_time);                                                     //
            digitalWrite(YMot,LOW);                                                 //
            delay(raster_time);                                                     //
            track[1]++;                                                             //
          }                                                                         //
        }                                                                           //
        delay(500);                                                                 //
        digitalWrite(XDir,!digitalRead(XDir));                                      //
      }                                                                             //
    digitalWrite(XDir,LOW);                                                         //
    digitalWrite(YDir,LOW);                                                         //
    digitalWrite(ZDir,LOW);                                                         //
    report('s');                                                                    //
    }                                                                               //
//*******************************MANUAL COMMANDS*********************************** //
    if (header == "M") {                                                            //qwfqf
      int flip = 0;                                                                 //
      String temp_cmd = Serial.readStringUntil(',');                                //
      char temp_dir = temp_cmd[0];                                                  //
      char temp_mot = temp_cmd[1];                                                  //
      String temp_rt = Serial.readStringUntil('*');                                 //
      int rt = temp_rt.substring(1).toInt();                                        //
      if (temp_dir == '+') {                                                        //
        digitalWrite(dir_select(temp_mot), HIGH);                                   //
        flip = 1;                                                                   //
      }                                                                             //
      else {                                                                        //
        digitalWrite(dir_select(temp_mot), LOW);                                    //
        flip = -1;                                                                  //
      }                                                                             //
      while (true) {                                                                //
        if (Serial.read() == 'S') {                                                 //
          report('s');                                                              //
          break;                                                                    //
        }                                                                           //
        digitalWrite(motor_select(temp_mot), HIGH);                                 //
        delay(500/rt);                                                              //
        digitalWrite(motor_select(temp_mot), LOW);                                  //
        delay(500/rt);                                                              //
        track[mot_track(temp_mot)] = track[mot_track(temp_mot)] + flip;             //
      }                                                                             //
    }                                                                               //
//*************************************HOME**************************************** //
    if (header == "H") {                                                            //
      for (int i = 0; i < 3; i++){                                                  //
        if (track[i] != 0){                                                         //
          steps[i] = (-1)*track[i];                                                 //
        }                                                                           //
      }                                                                             //
      while(steps[0] != 0 or steps[1] != 0 or steps[2] != 0) {                      //
        if (pause() == 'S') {                                                       //
          break;                                                                    //
        }                                                                           //
        for (int j = 0; j < 3; j++){                                                //
          if (steps[j] != 0){                                                       //
            if (steps[j] > 0) {                                                     //
              digitalWrite(dir_select(mots[j]),HIGH);                               //
              steps[j]--;                                                           //
              track[j]++;                                                           //
            }                                                                       //
            else {                                                                  //
              digitalWrite(dir_select(mots[j]),LOW);                                //
              steps[j]++;                                                           //
              track[j]--;                                                           //
            }                                                                       //
            digitalWrite(motor_select(mots[j]),HIGH);                               //  
          }                                                                         //
        }                                                                           //
        delay(2);                                                                   //
        for (int j = 0; j < 3; j++){                                                //
          digitalWrite(motor_select(mots[j]),LOW);                                  //
        }                                                                           //
        delay(2);                                                                   //
      }                                                                             //
      report('s');                                                                  //
    }                                                                               //
//*************************************ZERO**************************************** //
    if (header=="Z") {                                                              //
      for (int n = 0; n < 3; n++){                                                  //
        String temp_cmd = Serial.readStringUntil(',');                              //
        char zero = temp_cmd[0];                                                    //
        track[mot_track(zero)] = 0;                                                 //
      }                                                                             //
      report('s');                                                                  //
    }                                                                               //
//************************************CAMERA*************************************** //
    if (header=="C") {                                                              //
      photo();                                                                      //
      Serial.println("CAMERA!");
    }                                                                               //
  }                                                                                 //
}                                                                                   //
