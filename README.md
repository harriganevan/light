# lumen
lumen uses a circuit constructed with photoresistors connected to a Raspberry Pi running a program to determine how much light is directed in its direction. The data is stored in a SQL database on the Pi and can be pulled anywhere on the local network.

When the light.py file is run, it will continuously read a light value and store it in the database. This process will not end until the program is manually ended.
Once ended, the graph.py program can be run and will display the data from the database.

The images folder provides an image of the circuit used and an example of a graph created from data collected (low peaks represent low amounts of light, and high peaks represent high amounts of light).
