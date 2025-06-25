#!/bin/bash
export DISPLAY=:1
export HOME=/home/ubuntu
vncserver -kill :1 2>/dev/null || true
vncserver :1 -geometry 1024x768 -depth 24
sleep 2
DISPLAY=:1 fluxbox &
sleep 2
cd /home/ubuntu/facebook_publisher
source venv/bin/activate
DISPLAY=:1 python3 FacebookPublisherBoisMalin.py &
