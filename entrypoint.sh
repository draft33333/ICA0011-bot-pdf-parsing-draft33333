#!/bin/bash

echo "🔤 Translation compilation"
pybabel compile -d translations

echo "🚀 Run bot!"
python main.py
