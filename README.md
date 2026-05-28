# tradingsystem
# built and driven by AI chatGPT/copilot/claude
# Husain Natha

# set APP_ENV dev/test/prod
$env:APP_ENV="prod"
echo $env:APP_ENV

# init all databases dev/test/prod with sample data
python -m scripts.init_all_databases

# run build pipeline in APP_ENV
python -m app.pipeline.run_pipeline

# import data manually in to APP_ENV. sample data for dev/test. transactions are for prod.
python -m scripts.import_sample_data
python -m scripts.import_transactions

# data presentation 
tradingsystem\dashboard\trading_system.xlsx
tradingsystem\data\exports\prod-portfolio_intelligence.xlsx

# testing ...
python -m pytest tests/test_recommendation_mapper.py -v

