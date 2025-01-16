import sqlalchemy as db

class DatabaseHandler:
    def __init__(self, db_config, data, inside_container=True):
        self.db_config = db_config
        self.data = data
        self.engine = self.create_connection(inside_container=inside_container)

    def create_connection(self, inside_container):
        db_url_container = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        db_url_outside = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@localhost:{self.db_config['port']}/{self.db_config['database']}"

        return db.create_engine(db_url_container if inside_container else db_url_outside)
    
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

        self.data['daily_steps'].to_sql('daily_steps', self.engine, if_exists='append', index=False)

        # query = f"""
        # INSERT INTO daily_steps (date, total_steps, distance, step_goal) VALUES (data:, total_steps:,distance:,step_goal:), [{self.data['daily_steps']}];
        # """

        # with self.engine.connect() as conn:
        #     conn.execute(db.text(query))
        #     result = conn.execute(db.text("SELECT * FROM daily_steps;"))
        #     print(result.all())
        #     conn.commit()

    
