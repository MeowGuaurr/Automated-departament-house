void setup() {
  // put your setup code here, to run once:
  
}

void loop() {
  // put your main code here, to run repeatedly:
  float temperatura, distancia, tiempo;
  int intentos_fallidos;
  bool movimiento, encendido;

  //turning on motors if temp is cool
  do 
  {
    //turn on motor
  }
  while(temperatura <= 21.00 && temperatura >= 30.00);
  

  //turning on lights if there is people inside
  if (movimiento == true)
  {
    //turn on lights 
  }
  else
  {
    //delay 10 seconds and turn off lights
  }

  //rtc management
  if((tiempo > 18.00) && (tiempo < 7.00) || (movimiento == true))
  {
     //turn on lights 
  }

  //lock management 
  if (intentos_fallidos == 3)
  {
    //block lock for 15 mins
  }

}
