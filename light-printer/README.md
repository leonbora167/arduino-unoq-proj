Nothing deep just trying to understand how to control the lights on the board. 

I can differentiate it into 3 zones as far as I understand:

1. The one near the type c port, dont think you can control or need to 
2. Opposite of it on the other side there are 4 lights. They are rgb so any color i presume.
3. The main thing a dot matrix of blue led lights in 8x13 formation

---

a. Two of the rgb lights can be controlled using the python code inside the app cause they are physically connected to the *Qualcomm MPU (linux)*. Don't need C++ here.

b. The other two rgb lights are connected physically to the *STM32 Microcontroller (MCU)* pins so while we can control, as in send the signals through python will still require the use a function in c++ sketch to register and light it up.

---

* **Arduino_RouterBridge.h** gives access to Bridge a.k.a the communication chanel between linux/python and the microcontroller

* **Arduino_LED_Matrix.h** provides the driver to control the 8×13 physical LED matrix.

* **uint8_t** stands for unsigned integer of 8 bits - stores from 0 to 255 

* 8x13=104. So frame_buffer is allocated a fixed block of 104 contiguous bytes in RAM and initialized with 0 for all lights off

* Lets call frame a resizable array --- std::vector is this data type.

* In C++, memset is a fast, low-level CPU command that fills a chunk of raw memory with a specific byte:
  ```cpp
  memset(destination_pointer, value_to_fill, number_of_bytes_to_fill)
  ```
  overwriting all 104 bytes of frame_buffer with 0. Gurantees no leftover pixels from a previous frame

* **matrix.draw(frame_buffer);**: Hands the 104-byte buffer to the matrix hardware timer, which multiplexes the LEDs according to their brightness values (0 = off, 7 = max brightness).

* **clear_matrix**: Empties the local buffer using memset and tells the matrix hardware driver to shut off all LEDs.

* **matrix.begin()**: Configures the STM32 GPIO pins connected to the LED matrix into output mode.

* **matrix.setGrayscaleBits(3)**: Sets the resolution of LED brightness to 3 bits. This means each LED supports 8 brightness shades: 0 (off) up to 7 (full brightness). 2^3=8

* **Bridge.begin()**: Initializes the inter-processor communication bus to listen for messages from Linux/Python.

* **Bridge.provide_safe(...)**: Registers functions as RPC (Remote Procedure Call) endpoints. It tells the Bridge: "Whenever Python calls the name 'set_frame', run my C++ function set_matrix_frame"

* In arduino **loop()** runs forever until hardware interupt. Microcontroller waits for RPC calls from python.
