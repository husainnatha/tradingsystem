@echo off

cd /d C:\Users\Husain\OneDrive\TradingSystem

call venv\Scripts\activate

python -m app.marketdata.collect_macro_data

echo.
echo Macro market data collection complete.