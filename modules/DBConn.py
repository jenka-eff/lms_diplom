from sqlalchemy import create_engine



class DBConn:
    def conn(self):
        try:
            db_connect = create_engine(
                'postgresql://postgres:postgres@db-1.csjtwc9fnrfy.us-east-2.rds.amazonaws.com:5432/postgres')
            return db_connect
        except Exception as e:
            return 'Exception: {}'.format(e)
