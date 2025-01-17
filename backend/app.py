from flask import Flask, jsonify, request
import sqlalchemy as db
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__);

# db_config = {
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'host': os.getenv('DB_HOST'),
#     'port': os.getenv('DB_PORT'),
#     'database': os.getenv('DB_NAME')
# }
db_config = {
    'user': 'postgres',
    'password': 'garmin',
    'host': 'db',  # This matches the service name in docker-compose
    'port': '5432',
    'database': 'garmin'
}
print(db_config)

def create_connection(inside_container=True):
    db_url_container = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    db_url_outside = f"postgresql://{db_config['user']}:{db_config['password']}@localhost:{db_config['port']}/{db_config['database']}"

    return db.create_engine(db_url_container if inside_container else db_url_outside)

engine = create_connection(inside_container=True)

@app.route('/daily_steps', methods=['GET'])
def get_daily_steps():
    try:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=14)

        time_period = request.args.get('time_period', '14days')
        end_date = datetime.now().date()
        
        if time_period == '14days':
            start_date = end_date - timedelta(days=14)
        elif time_period == '30days':
            start_date = end_date - timedelta(days=30)
        elif time_period == '7days':
            start_date = end_date - timedelta(days=7)
        elif time_period == '6months':
            start_date = end_date - timedelta(days=180)
        elif time_period == '1year':
            start_date = end_date - timedelta(days=365)

        start_date = request.args.get('start_date', start_date.strftime('%Y-%m-%d'))  # e.g., '2023-01-01'
        end_date = request.args.get('end_date', end_date.strftime('%Y-%m-%d'))      # e.g., '2023-01-10'
        aggregation = request.args.get('aggregation', 'daily') 
        
        query = f"""SELECT * FROM daily_steps WHERE date > '{start_date}' AND date < '{end_date}'"""

        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001)