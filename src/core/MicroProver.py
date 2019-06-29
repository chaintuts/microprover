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

        # Settings for random numbers
        self.RAND_MIN = 0
        self.RAND_MAX = 255

        # Settings for "cryptography"
        self.HASH_MOD = 256

        # Initialize logging and logging data
        self.run = 1
        self.init_logging()

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
                solution = self.prove_work(self.run, difficulty)
            else:
                if cpx.button_a:
                    solution = False
                    self.increment_run()
                if cpx.button_b:
                    break;

    # This function provides a proof-of-work algorithm implementation
    # It loops infinitely until a solution is found, returning True
    def prove_work(self, run, difficulty):

        # Initialization for proof-of-work
        # Clear the board LEDs
        # Get a random integer to represent the "block" data
        # Set the difficulty target as an 8 bit integer
        # We're going to guess until we have a solution!
        cpx.pixels.fill(self.BLANK)
        block = self.get_random_block()
        target = self.get_diff_target(difficulty)
        possible_nonces = self.create_nonces()
        nonce = 0
        attempt = 1
        while True:

            # Get the hash of the data and check if it meets the target
            hash8 = self.hash_8bit(block + nonce)

            self.display_byte_led(hash8)
            self.log_hash(run, target, hash8, block, nonce, attempt)

            result = self.check_hash(hash8, target)
            if result:
                self.alert_solution()
                return True

            # Increment the nonce and attempt counter
            nonce = possible_nonces[attempt]
            attempt += 1

    # Get the difficulty target from the specified difficulty
    # The difficulty will be an 8 bit number 0 - 255
    def get_diff_target(self, difficulty):
        multiplier = 7 - difficulty
        target = (2 ** multiplier)

        return target

    # Since our hash space is only 8 bit, we should have a
    # max of 256 possible nonces
    # Since our hash algorithm is simplistic and predictable,
    # let's shuffle the list of possible nonces to make our
    # algorithm behave more realistically
    def create_nonces(self):

        nonces = list( range(self.RAND_MIN, self.RAND_MAX) )
        for i in range(self.RAND_MAX - 1, 0, -1):
            swap = random.randint(0, i + 1)
            tmp = nonces[i]
            nonces[i] = nonces[swap]
            nonces[swap] = tmp

        return nonces

    # Return a really simple 8 bit hash
    # This is for educational purposes, so we don't need a
    # cryptographically secure hash, we just need one that works
    def hash_8bit(self, data):
        hash8 = data % self.HASH_MOD

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
        block = random.randint(self.RAND_MIN, self.RAND_MAX)

        return block

    # Increment the run counter for logging
    def increment_run(self):

        self.run = self.run + 1

    # Initialize logging functionality
    # This function will output CSV headers
    def init_logging(self):

        print("Run,Target,Hash8,Block,Nonce,Attempt")

    # This function logs hash attempts to the serial connection
    # This data can be used to better understand the algorithm
    # if desired
    def log_hash(self, run, target, hash8, block, nonce, attempt):

        # First, format the target and hash8 in binary format (0's and 1's)
        target_bitarray = self.byte_to_bitarr(target, mode="bit")
        target_binary = "".join(target_bitarray)
        hash8_bitarray = self.byte_to_bitarr(hash8, mode="bit")
        hash8_binary = "".join(hash8_bitarray)

        # Format the log string and print to the serial console
        log_string = "{},{},{},{},{},{}\n"
        log_entry = log_string.format(run, target_binary, hash8_binary, block, nonce, attempt)
        print(log_entry)

        # Now write to the log file onboard the CircuitPython device if able
        try:
            with open("pow_log.csv", "a") as f:
                f.write(log_entry)
        except Exception as e:
            print("{}".format(e))

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

    # Make an audible alert when a solution is found
    # This plays a tone through the Circuit Playground's speaker
    def alert_solution(self):

        cpx.play_tone(300, 0.5)

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
mp = MicroProver()
while True:

    diff = mp.program_difficulty()

    # Initialize the number of runs
    mp.visualize_pow(diff)
    mp.increment_run()