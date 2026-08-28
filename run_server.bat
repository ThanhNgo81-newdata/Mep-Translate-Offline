@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
streamlit run mep_translator_offline.py --server.address 0.0.0.0 --server.port 8501
pause
