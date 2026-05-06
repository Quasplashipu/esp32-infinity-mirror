# esp32-infinity-mirror
Older project for an ESP32 using neopixel LED strip for a infinite mirror.
Using Micropython.
I did a little fixing up for 2026, but code is pretty old.
Here is the project visualized in WOKWI:
https://wokwi.com/projects/462931134977924097

## Button Map

### Main Menu 
*(When the matrix is blank/waiting)*

*   ⚪ **White Button:** Starts **Rainbow Mode**
*   🟢 **Green Button:** Starts **Clock Mode**
*   🔴 **Red Button:** Starts **Roulette Mode**
*   🟡 **Yellow Button:** Starts **Speed Game**
*   🔘 **Grey Button:** Starts **Color Shifter**

---

### Rainbow Mode

*   🔘 **Grey Button:** Exit back to Main Menu

---

### Clock Mode

*   🟢 **Green Button:** Add +1 Minute *(Hold to scroll fast)*
*   ⚪ **White Button:** Add +1 Hour *(Hold to scroll fast)*
*   🔘 **Grey Button:** Exit back to Main Menu

---

### Roulette Mode

*   **No buttons needed.** It spins, lands on a color, flashes, and automatically exits back to the Main Menu.

---

### Speed Game

*   **Step 1 (Choose Difficulty):** 
    *   ⚪ **White:** Easy
    *   🟢 **Green:** Medium
    *   🔴 **Red:** Hard
    *   🟡 **Yellow:** Insane
    *   🔘 **Grey:** Exit to Menu
*   **Step 2 (Play):** Wait for the lights to go dark. The exact millisecond they turn **Green**, press the ⚪ **White** button!

---

### Color Shifter

*   ⚪ **White Button:** Add +10 to Red value
*   🟢 **Green Button:** Add +10 to Green value
*   🔴 **Red Button:** Add +10 to Blue value
*   🟡 **Yellow Button:** Reset color back to Black `(0, 0, 0)`
*   🔘 **Grey Button:** Exit back to Main Menu
