import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = str(os.environ.get("localhost"))
    PORT = str(os.environ.get("3306"))
    DATABASE = str(os.environ.get("projectweb"))
    USER = str(os.environ.get("root"))

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/projectweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True