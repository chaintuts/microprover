## General
____________

### Author
* Josh McIntyre

### Website
* jmcintyre.net

### Overview
* MicroProver helps users visualize proof-of-work algorithms on the Adafruit Circuit Playground Express

## Development
________________

### Git Workflow
* master for releases (merge development)
* development for bugfixes and new features

### Building
* make build
Build the application
* make clean
Clean the build directory

### Features
* A programmable visualization tool for mock proof-of-work - set difficulty from 1-7
* Visualize work being done by displaying each 8 bit hash as LEDs on the board 

### Requirements
* Requires Python 3 and CircuitPython

### Platforms
* Adafruit Circuit Playground Express

## Usage
____________

### General usage
* Rename the desired module to "code.py" and copy to the root directory
* Set the difficulty rating from 1-7 by pressing the B button. The difficulty will be displayed by the LEDs
* Press A to start hashing - each 8-bit hash value will be shown with the board LEDs. RED == 0, GREEN == 1
* The final solution (hash value) will be displayed by the LEDs
* Press A to restart hashing, or B to return to the difficulty programming menu

