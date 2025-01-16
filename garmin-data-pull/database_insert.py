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

        with self.engine.connect() as conn:
            result = conn.execute(db.text("select 'hello world'"))
            print(result.all())
    
