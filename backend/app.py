from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
import sqlalchemy as db
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})

# db_config = {
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'host': os.getenv('DB_HOST'),
#     'port': os.getenv('DB_PORT'),
#     'database': os.getenv('DB_NAME')
# }
db_config = {
    'user': Config.POSTGRES_USER,
    'password': Config.POSTGRES_PASSWORD,
    'host': Config.POSTGRES_HOST,
    'port': Config.POSTGRES_PORT,
    'database': Config.POSTGRES_DB
}
print(db_config)

def create_connection(inside_container=True):
    db_url_container = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    db_url_outside = f"postgresql://{db_config['user']}:{db_config['password']}@localhost:{db_config['port']}/{db_config['database']}"

    return db.create_engine(db_url_container if inside_container else db_url_outside)

engine = create_connection(inside_container=True)

def calc_dates(time_period):

    end_date = datetime.now().date()
    
    if time_period == '14days':
        start_date = end_date - timedelta(days=14)
    elif time_period == '30days':
        start_date = end_date - timedelta(days=30)
    elif time_period == '7days':
        start_date = end_date - timedelta(days=7)
    elif time_period == '90days':
        start_date = end_date - timedelta(days=90)
    elif time_period == '6months':
        start_date = end_date - timedelta(days=180)
    elif time_period == '1year':
        start_date = end_date - timedelta(days=365)

    start_date = start_date.strftime('%Y-%m-%d') # e.g., '2023-01-01'
    end_date = end_date.strftime('%Y-%m-%d')      # e.g., '2023-01-10'

    return start_date, end_date



@app.route('/daily_steps', methods=['GET'])
def get_daily_steps():
    try:

        # end_date = datetime.now().date()
        # start_date = end_date - timedelta(days=14)

        # time_period = request.args.get('time_period', '14days')
        # end_date = datetime.now().date()
        
        # if time_period == '14days':
        #     start_date = end_date - timedelta(days=14)
        # elif time_period == '30days':
        #     start_date = end_date - timedelta(days=30)
        # elif time_period == '7days':
        #     start_date = end_date - timedelta(days=7)
        # elif time_period == '90days':
        #     start_date = end_date - timedelta(days=90)
        # elif time_period == '6months':
        #     start_date = end_date - timedelta(days=180)
        # elif time_period == '1year':
        #     start_date = end_date - timedelta(days=365)

        # start_date = request.args.get('start_date', start_date.strftime('%Y-%m-%d'))  # e.g., '2023-01-01'
        # end_date = request.args.get('end_date', end_date.strftime('%Y-%m-%d'))      # e.g., '2023-01-10'
        # aggregation = request.args.get('aggregation', 'daily') 

        start_date, end_date = calc_dates(request.args.get('time_period', '14days'))
        
        query = f"""SELECT * FROM daily_steps WHERE date > '{start_date}' AND date < '{end_date}' ORDER BY date asc"""

        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/activity_list', methods=['GET'])
def get_activity_times():
    try:
        start_date, end_date = calc_dates(request.args.get('time_period', '14days'))
        
        query = f""" SELECT a."startTimeGMT", a."activityTypeName", a."elapsedDuration", a."activityName" FROM activity_list AS a WHERE a."startTimeGMT" > '{start_date}' AND a."startTimeGMT" < '{end_date}' ORDER BY a."startTimeGMT" asc; """
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))

   # SELECT a."activityTypeName", a."elapsedDuration", a."activityName" FROM activity_list AS a WHERE a."startTimeGMT" > '{start_date}' AND a."startTimeGMT" < '{end_date}' ORDER BY date asc; 
   # """ SELECT a."startTimeGMT", a."activityTypeName", a."elapsedDuration", a."activityName" FROM activity_list AS a WHERE a."startTimeGMT" > '2024-10-01' AND a."startTimeGMT" < '2024-11-10' ORDER BY a."startTimeGMT" asc; """

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001)



# """SELECT a."startTimeGMT", a."activityTypeName", a."elapsedDuration", a."activityName" FROM activity_list AS a WHERE a."startTimeGMT" > '2024-10-01' AND a."startTimeGMT" < '2024-11-10' ORDER BY a."startTimeGMT" asc GROUPBY a."startTimeGMT" ; """