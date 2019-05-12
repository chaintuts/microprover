# This code helps users visualize proof-of-work
# algorithm difficulty levels using LEDs
#
# Author: Josh McIntyre
#
from adafruit_circuitplayground.express import cpx
import time
import random

# This class defines functions for visualizing
# proof-of-work algorithms and how the difficulty
# effects the amount of time it can take to find a solution
class MicroProver():

    def __init__(self):

        # Settings for the LED display
        cpx.pixels.brightness = 0.1
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLANK = (0, 0, 0)

    # This function sets the difficulty level for proof-of-work
    # The user presses B to set a difficulty level from 1 - 7
    # The difficulty will be shown on the board by showing LEDs
    def program_difficulty(self):

        # First, clear the LEDs and set a base difficulty
        cpx.pixels.fill(self.BLANK)
        diff = 1
        while True:

            # Display the difficulty exponent with LEDs
            for i in range(0, diff):
                cpx.pixels[i + 1] = self.RED
            for i in range(diff, 7):
                cpx.pixels[i + 1] = self.BLANK
            cpx.pixels.show()

            # Press B to increment the difficulty exponent by 1
            if cpx.button_b:

                if diff > 6:
                    diff = 1
                else:
                    diff += 1

                # Sleep so we don't get a big jump in value
                time.sleep(0.2)

            # Press A to exit the setup and start the proof of work
            if cpx.button_a:
                break

        # Set the difficulty
        return diff

    # This function implements a basic menu for proof-of-work simulation
    # If we've found a solution, just leave it on the board and wait
    # The A button restarts a new round of proof-of-work simulation
    # The B button exits to the difficulty programming menu
    def visualize_pow(self, difficulty):

        solution = False
        while True:
            if not solution:
                solution = self.prove_work(difficulty)
            else:
                if cpx.button_a:
                    solution = False
                if cpx.button_b:
                    break;

    # This function provides a proof-of-work algorithm implementation
    # It loops infinitely until a solution is found, returning True
    def prove_work(self, difficulty):

        # Initialization for proof-of-work
        # Clear the board LEDs
        # Get a random integer to represent the "block" data
        # Set the difficulty target as an 8 bit integer
        # We're going to guess until we have a solution!
        cpx.pixels.fill(self.BLANK)
        block = self.get_random_block()
        target = self.get_diff_target(difficulty)
        nonce = 0
        while True:

            # Get the hash of the data and check if it meets the target
            hash8 = self.hash_8bit(block + nonce)

            self.display_byte_led(hash8)
            self.log_hash(target, hash8, block, nonce)

            result = self.check_hash(hash8, target)
            if result:
                return True

            # Increment the nonce
            nonce += random.randint(257, 12345678)

    # Get the difficulty target from the specified difficulty
    # The difficulty will be an 8 bit number 0 - 255
    def get_diff_target(self, difficulty):
        multiplier = 8 - difficulty
        target = (2 ** multiplier)

        return target

    # Return a really simple 8 bit hash
    # This is for educational purposes, so we don't need a
    # cryptographically secure hash, we just need one that works
    def hash_8bit(self, data):
        hash8 = data % 256

        return hash8

    # Check if the 8 bit hash is less than the
    # 8 bit target. If so, return True
    def check_hash(self, hash8, target):

        if hash8 < target:
            return True
        else:
            return False

    # Get some random data to represent a block
    def get_random_block(self):

        random.seed(time.time())
        block = random.randint(257, 12345678)

        return block

    # This function logs hash attempts to the serial connection
    # This data can be used to better understand the algorithm
    # if desired
    def log_hash(self, target, hash8, block, nonce):

        # First, format the target and hash8 in binary format (0's and 1's)
        target_bitarray = self.byte_to_bitarr(target, mode="bit")
        target_binary = "".join(target_bitarray)
        hash8_bitarray = self.byte_to_bitarr(hash8, mode="bit")
        hash8_binary = "".join(hash8_bitarray)

        # Format the log string and print to the serial console
        log_string = "Target {}, Hash8 {}, Block {}, Nonce {}"
        print(log_string.format(target_binary, hash8_binary, block, nonce))

    # This function displays an LED representation of a byte
    # It lights up 8 LEDs on the Playground Express board
    # Green represents a 1 bit
    # Red represents a 0 bit
    def display_byte_led(self, byte):

        bitarr = self.byte_to_bitarr(byte)
        for i in range(0, 8):
            if bitarr[i]:
                color = self.GREEN
            else:
                color = self.RED

            # Load the pixels from 1 - 9 so they
            # fill evenly on each side of the board
            cpx.pixels[i + 1] = color
        cpx.pixels.show()

    # Convert a byte of data (8 bit hash, etc.) into
    # an array of bits represented by True (1) and False (0)
    # (with default mode bool)
    # Specify optional mode "bit" for 0/1 representation
    def byte_to_bitarr(self, byte, mode="bool"):

        # Define some bitmasks for each spot in the byte
        # We'll create the array using bitmasking
        masks = [ 0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01 ]
        byte = int(byte)

        bitarr = []
        for i in range(0, 8):
            if mode == "bit":
                masked = byte & masks[i]
                bit = "1" if masked > 0 else "0"
            else:
                bit = bool(byte & masks[i])
            bitarr.append(bit)

        return bitarr

# This is the main entry point for the program and implements a basic main menu
while True:

    mp = MicroProver()
    diff = mp.program_difficulty()
    mp.visualize_pow(diff)