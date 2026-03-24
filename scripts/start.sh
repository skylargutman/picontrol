#!/bin/bash
echo "Starting pigpiod..."
sudo systemctl start pigpiod

echo "Starting display daemon..."
python3 /home/skylar/picontrol/scripts/update_display.py &
sleep 1

echo "Starting model..."
sudo /home/skylar/picontrol/models/MATLAB_ws/R2025b/model_b.elf &

echo "Done. Run stop.sh to shut down."
