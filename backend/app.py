from flask import Flask, jsonify
import sqlalchemy as db
import pandas as pd
import os
from dotenv import load_dotenv

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
        query = "SELECT * FROM daily_steps"
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001)