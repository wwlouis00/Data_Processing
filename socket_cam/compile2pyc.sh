#! /bin/bash

rm -rf /home/pi/socket_cam
python3 compile2pyc.py
sed 's/\/winnoz_eggi2.0//; s/.py/.pyc/' autostart.sh > /home/pi/socket_cam/autostart.sh
echo "autostart.sh copied"
chmod +x /home/pi/socket_cam/autostart.sh
echo "Done!"
