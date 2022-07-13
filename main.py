import utime
import _thread
import machine
from machine import I2C,Pin, ADC, Timer
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
#from gpiozero import MotionSensor
pir = Pin(28,Pin.IN,Pin.PULL_DOWN)
led_pir = machine.Pin(15, machine.Pin.OUT)
temp = 0

#Definicion de matriz y pines para cerradura
matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

keypad_rows = [9,8,7,6]
keypad_cols = [5,4,3,2]

cols_pin = []
rows_pin = []
password = []
intentos = 0

Ppin = ['1','2','3','4','5','6']
green = Pin(16,Pin.OUT)
red = Pin(17,Pin.OUT)
buzzer = Pin(18, Pin.OUT)


#Pines para temperatura
value = 0;
sensor = ADC(4)
led_red = machine.Pin(14, machine.Pin.OUT)

for x in range(0, 4):
    rows_pin.append(machine.Pin(keypad_rows[x], machine.Pin.OUT))
    rows_pin[x].value(1)
    cols_pin.append(machine.Pin(keypad_cols[x], machine.Pin.IN, machine.Pin.PULL_DOWN))
    cols_pin[x].value(0)

print("Please enter a key from the keypad")


#Dirección del I2C y tamaño del LCD
I2C_ADDR  =  0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=machine.Pin(12), scl=machine.Pin(13), freq= 200000)
i2c.scan() 
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#Dirección del I2C y tamaño del LCD grande
I2C_ADDR  =  0x27
I2C_NUM_ROWS2 = 3
I2C_NUM_COLS2 = 20
i2c2 = I2C(1, sda=machine.Pin(10), scl=machine.Pin(11), freq= 200000)
i2c2.scan() 
lcd2 = I2cLcd(i2c2, I2C_ADDR, I2C_NUM_ROWS2, I2C_NUM_COLS2)

def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)
   
def lcd_str2(message, col, row):
    lcd2.move_to(col, row)
    lcd2.putstr(message)
    


def temperatura(timer):
    #Control de temperatura
        valor = sensor.read_u16()*3.3/65535
        temp = 27 - (valor - 0.706)/0.001721
        temp = round(temp)
        print(temp)
        lcd2.clear()
        
        temp_str = str(temp)
        #print(type(temp_str))
        
        lcd_str2("Temperature: ", 0,0)
        lcd_str2(temp_str, 14,0)

        if( temp > 24):
            led_red.value(1)
        else:
            led_red.value(0)
            
timer = Timer()
timer.init(period=10000, mode = Timer.PERIODIC, callback = temperatura)

def main():
    while True:
        pass
        scankeys()

def pir_handler():
    if pir.value():
        value = 1;
        
    else:
        value = 0;
    
    return value

def second_main():
    while True:
        pir_handler()
        if pir.value():
            led_pir.value(1)
        
        else:
            led_pir.value(0)
            
        utime.sleep_ms(300)
        

_thread.start_new_thread(second_main,())
  
def scankeys():
    lcd_str("Password:", 0,0)
    
    for row in range(4):
        for col in range(4):
            rows_pin[row].high()
            key = None
            
            if cols_pin[col].value() == 1:
                
                print("You have pressed:", matrix_keys[row][col])
                
                key_press = matrix_keys[row][col]
                utime.sleep(0.3)
                password.append(key_press)
                
                lenght = len(password)
                if len(password) == 0:
                    lcd_str("*", 8,1)
                    
                elif len(password) == 1:
                    lcd_str("*", 7,1)
                    
                elif len(password) == 2:
                    lcd_str("*", 6,1)
                    
                elif len(password) == 3:
                    lcd_str("*", 5,1)
                    
                elif len(password) == 4:
                    lcd_str("*", 4,1)
                    
                elif len(password) == 5:
                    lcd_str("*", 3,1)
                
                elif len(password) == 6:
                    lcd_str("*", 2,1)
                    Check_password(password)
                    for x in range(0,6):
                        password.pop()
                             
        rows_pin[row].low()
        

def Check_password(password):
    if password == Ppin:
        lcd.clear()
        print("pass")
        lcd_str("Open", 0,0)
        green.value(1)
        utime.sleep(1)
        green.value(0)
        lcd.clear()
    else:
        lcd.clear()
        lcd_str("Denied", 0,0)
        buzzer.value(1)
        red.value(1)
        utime.sleep(2)
        red.value(0)
        buzzer.value(0)
        lcd.clear()
    


if __name__ == '__main__':
    main(),
