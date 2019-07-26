# This file contains a make script for the MicroProver application
#
# Author: Josh McIntyre
#

# This block defines makefile variables
SRC_FILES=src/core/*.py src/boot/* src/dataviz/*
RES_FILES=res/sounds/*.wav

BUILD_DIR=bin/microprover
RES_DIR=sounds

# This rule builds the application
build: $(SRC_FILES) $(RES_FILES)
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/$(RES_DIR)
	cp $(SRC_FILES) $(BUILD_DIR)
	cp $(RES_FILES) $(BUILD_DIR)/$(RES_DIR)
	mv $(BUILD_DIR)/MicroProver.py $(BUILD_DIR)/code.py

# This rule cleans the build directory
clean: $(BUILD_DIR)
	rm -r $(BUILD_DIR)/*
	rmdir $(BUILD_DIR)
