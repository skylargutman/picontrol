#!/bin/bash
echo "Stopping model..."
sudo pkill -f model_b.elf

echo "Stopping display daemon..."
pkill -f update_display.py

echo "Stopping pigpiod..."
sudo systemctl stop pigpiod

echo "Done."
