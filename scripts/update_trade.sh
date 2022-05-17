#!/bin/bash
cd ~/Code/StockPicker
. env/bin/activate
git pull
python3.9 RobotDaily.py

#python3.9 -m venv env
#. env/bin/activate
# python3.9 -m pip install --upgrade pip
# pip install requests
# pip install beautifulsoup4
# pip install sqlalchemy
# pip install pymysql