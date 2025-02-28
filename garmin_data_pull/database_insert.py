import sqlalchemy as db
import json

class DatabaseHandler:
    def __init__(self, db_config, data, inside_container=True):
        self.db_config = db_config
        self.data = data
        self.engine = self.create_connection(inside_container=inside_container)

    def create_connection(self, inside_container):
        db_url_container = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        db_url_outside = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@localhost:{self.db_config['port']}/{self.db_config['database']}"
        
        connection_url = db_url_container if inside_container else db_url_outside
        print(f"Attempting to connect with URL: {connection_url}")
        
        try:
            engine = db.create_engine(connection_url)
            # Test the connection
            with engine.connect() as conn:
                print("Successfully connected to database!")
            return engine
        except Exception as e:
            print(f"Failed to connect to database: {str(e)}")
            raise
    
    def test(self):

        query = """
        INSERT INTO daily_steps (date, total_steps, distance, step_goal) VALUES ('01-01-2001', 3000,4000,10000);
        """

        with self.engine.connect() as conn:
            conn.execute(db.text(query))
            result = conn.execute(db.text("SELECT * FROM daily_steps;"))
            print(result.all())
            conn.commit()

    def insert_data(self):
        # Option 1: Convert dictionaries to JSON strings
        activity_df = self.data['activity_list'].copy()
        for column in activity_df.columns:
            if activity_df[column].apply(lambda x: isinstance(x, (dict, list))).any():
                activity_df[column] = activity_df[column].apply(lambda x: json.dumps(x) if x is not None else None)

        # Insert the processed dataframe
        activity_df.to_sql('activity_list', self.engine, if_exists='replace', index=False)

        # Original steps data should work fine as is
        self.data['daily_steps'].to_sql('daily_steps', self.engine, if_exists='replace', index=False)

    
