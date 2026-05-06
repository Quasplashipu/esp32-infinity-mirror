import machine
import neopixel
import time
import random
import utime

#notes: 
#smeni cvetowete, polzvai 0, 0, 0 za background (cherno irl)
#NEVER use full 255, 255, 255 na vsichki pixeli ednovremenno

n = 60  # Number of LEDs in your matrix
p = 15  # GPIO pin connected to Din
np = neopixel.NeoPixel(machine.Pin(p), n)

# Define the GPIO pins for the buttons
# Initialize the button pins as pull-up inputs
btn_white = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
btn_green = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
btn_red   = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
btn_grey  = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
btn_yellow = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

def set_led_color(color):
    for x in range(n):
        np[x] = color
    np.write()

def flashled(color1, delay):
    set_led_color(color1)
    time.sleep(delay)
    set_led_color((0,0,0))
    time.sleep(delay)
    set_led_color(color1)
    time.sleep(delay)
    set_led_color((0,0,0))
    time.sleep(delay)
    set_led_color(color1)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def spinLed(x, y):
    for i in range(x):
        np[i] = ((255,255,255))
        time.sleep(y)
        np.write()
        if i % 2 == 0:
            np[i] = ((255,0,0))
        else:
            np[i] = ((1,1,1))
        np[7] = ((0,255,0))
        np[37] = ((0,255,0))


def game(green_time):
    rnum_t = random.randint(2, 8)
    set_led_color((125, 125, 125))
    time.sleep(1)
    
    set_led_color((2, 2, 2))
    early_press = False
    
    for _ in range(rnum_t * 100):
        time.sleep(0.01)
        if btn_white.value() == 0:
            flashled((125, 0, 0), 0.1)
            early_press = True
            break
            
    if not early_press:
        set_led_color((0, 100, 0)) 
        start_time = utime.ticks_ms()

        while btn_white.value() == 1:
            pass 
            
        reaction_time = utime.ticks_diff(utime.ticks_ms(), start_time)
        set_led_color((0, 0, 0))
        print("Reaction:", reaction_time, "ms")
        
        # Check if the reaction was fast enough
        if reaction_time < green_time:  # Less than 500 milliseconds to win
            print("You win")
            flashled((0, 255, 0), 0.1)
        else:
            flashled((125, 0, 0), 0.1)
            
        time.sleep(0.5)
        set_led_color((0, 0, 0))
        score_leds = min(reaction_time // 10 + 1, 60)
        for i in range(score_leds):
            np[i] = (50, 50, 100)
        
        np[15] = (100, 0, 100)
        np[25] = (125, 0, 0)
        np[35] = (125, 100, 0)
        np[50] = (0, 125, 0)
        np.write()
        time.sleep(2)

#combo 2: speed game
def run_speed_game():
    set_led_color((10, 10, 10))
    time.sleep(1)
    
    while True:
        if btn_grey.value() == 0: 
            break
        elif btn_white.value() == 0:
            game(500)
            break
        elif btn_green.value() == 0:
            game(350)
            break
        elif btn_red.value() == 0:
            game(250)
            break
        elif btn_yellow.value() == 0:
            game(150)
            break

# combo 1 Set LED color based on button states
# -- COLOR CHANGE --
def run_shifter():
    r, g, b = 0, 0, 0
    time.sleep(0.5)
    
    while True:
        if btn_grey.value() == 0: 
            break
        if btn_yellow.value() == 0: 
            r, g, b = 0, 0, 0
            time.sleep(0.2)
            
        if btn_white.value() == 0:
            r = (r + 10) % 255
        if btn_green.value() == 0:
            g = (g + 10) % 255
        if btn_red.value() == 0:
            b = (b + 10) % 255
            
        set_led_color((r, g, b))
        time.sleep(0.05)

# -- RAINBOW --
def run_rainbow():
    offset = 0
    while True:
        if btn_grey.value() == 0: 
            break
            
        for i in range(n):
            pixel_index = (i * 256 // n) + offset
            np[i] = wheel(pixel_index & 255)
        np.write()
        offset = (offset + 2) & 255
        time.sleep(0.02)

# -- CLOCK --
def run_clock():
    hours = 0
    minutes = 0
    seconds = 0
    last_tick = utime.ticks_ms()
    
    time.sleep(0.5)
    
    needs_update = True # Force an initial draw
    
    while True:
        if btn_grey.value() == 0: 
            break
            
        if btn_green.value() == 0: 
            minutes = (minutes + 1) % 60
            time.sleep(0.15) 
            needs_update = True
            
        if btn_white.value() == 0: 
            hours = (hours + 1) % 12
            time.sleep(0.2)
            needs_update = True
            
        if utime.ticks_diff(utime.ticks_ms(), last_tick) >= 1000:
            seconds += 1
            last_tick = utime.ticks_ms()
            if seconds >= 60:
                seconds = 0
                minutes += 1
                if minutes >= 60:
                    minutes = 0
                    hours = (hours + 1) % 12
            needs_update = True

        if needs_update:
            # Clear the strip *without* calling np.write() immediately
            for i in range(60):
                np[i] = (0, 0, 0)
            
            # Draw static hour markers shifted to the 12 o'clock position (index 7)
            for i in range(0, 60, 5):
                np[(i + 7) % 60] = (20, 20, 20) 
                
            hour_pos = (hours * 5 + (minutes // 12) + 7) % 60
            minute_pos = (minutes + 7) % 60
            second_pos = (seconds + 7) % 60
            
            np[hour_pos] = (0, 0, 255) 
            np[minute_pos] = (255, 0, 0)
            np[second_pos] = (0, 255, 0)
            
            np.write() # Write ONLY ONCE per frame!
            needs_update = False

# -- ROULETTE --
def run_roulette():
    for i in range(60):
        if i % 2 == 0:
            np[i] = ((255,0,0))
        else:
            np[i] = ((1,1,1))
    np[7] = ((0,255,0))
    np[37] = ((0,255,0))
    np.write()

    time.sleep(1)

    rnum = random.randint(0, 60)
    print(rnum)

    spinLed(60, 0.010)
    spinLed(60, 0.035)

    if(rnum > 30):
        spinLed(rnum, 0.075)
    else:
        spinLed(rnum, 0.1)
    
    if (rnum - 1) in [7, 37]:
        flashled((0,255,0), 0.1)
    if (rnum - 1) % 2 == 0:
        flashled((255,0,0), 0.1)
    if (rnum - 1) % 2 != 0:
        flashled((25,25,25), 0.1)


set_led_color((0, 0, 0))
time.sleep(0.5)
for i in range(125):
    set_led_color((i, 0, i))
    time.sleep(0.001)
for i in range(125, 0, -1):
    set_led_color((i, 0, i))
    time.sleep(0.001)
set_led_color((0, 0, 0))


while True:
    if btn_white.value() == 0:
        run_rainbow()
        set_led_color((0, 0, 0))
        time.sleep(0.5)
        
    elif btn_green.value() == 0:
        run_clock()
        set_led_color((0, 0, 0))
        time.sleep(0.5)
        
    elif btn_red.value() == 0:
        run_roulette()
        set_led_color((0, 0, 0))
        time.sleep(0.5)
        
    elif btn_yellow.value() == 0:
        run_speed_game()
        set_led_color((0, 0, 0))
        time.sleep(0.5)
        
    elif btn_grey.value() == 0:
        run_shifter()
        set_led_color((0, 0, 0))
        time.sleep(0.5)
        
    time.sleep(0.05)
