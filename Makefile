# This file contains a make script for the MicroProver application
#
# Author: Josh McIntyre
#

# This block defines makefile variables
SRC_FILES=src/core/*.py src/boot/* src/dataviz/*

BUILD_DIR=bin/microprover

# This rule builds the application
build: $(SRC_FILES)
	mkdir -p $(BUILD_DIR)
	cp $(SRC_FILES) $(BUILD_DIR)
	mv $(BUILD_DIR)/MicroProver.py $(BUILD_DIR)/code.py

# This rule cleans the build directory
clean: $(BUILD_DIR)
	rm $(BUILD_DIR)/*
	rmdir $(BUILD_DIR)
