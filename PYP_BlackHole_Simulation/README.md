**Just a fun experiment in combining General Relativity concepts with Pygame. This script simulates a Schwarzschild-style black hole with a rotating accretion disk, a glowing photon ring, and a starfield background. It uses some 3D-to-2D projection math and depth sorting to make everything look right on a flat screen.**



* **Rodrigues' Rotation:** Handles the camera movement (yaw/pitch) so you can fly around the black hole in 3D space.



* **Accretion Disk:** Thousands of particles orbiting the center with varying velocities.



* **The Glow Effect:** Uses per-pixel alpha transparency (SRCALPHA) to create that soft, cinematic bloom around the event horizon.



* **Painter’s Algorithm:** A depth-sorting fix that ensures distant stars stay behind the black hole while close particles correctly overlap it.



* **Dynamic UI:** Includes a real-time overlay showing FPS, particle counts, and camera coordinates.





##### **Files Content**

* **Black\_Hole.py -**  The main engine. It handles the physics loops, particle updates, and the Pygame rendering window.
* **Black Hole Simulation.docx -** A breakdown of the math and logic used, including references to the physics constants (like the Schwarzschild Radius $R\_s$).





##### **Controls**

* **Mouse: Click and drag to orbit the camera.**



* **Scroll: Zoom in and out.**



* **ESC: Quit the simulation.**





##### **Note to Self**

* **The starfield is static but rotates relative to the camera to give the illusion of infinite space.**



* **If the FPS drops, lower the NUM\_DISK\_PARTICLES constant at the top of the script.**



* **The Infall Velocity makes the disk look like it's actually being sucked in over time.**

