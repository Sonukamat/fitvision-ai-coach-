@echo off
title AI Real-time GYM Coach
echo ===================================================
echo 🏋️ Starting AI Real-time GYM Coach...
echo ===================================================
cd /d "%~dp0Main App"
..\.venv\Scripts\streamlit.exe run main.py
pause
