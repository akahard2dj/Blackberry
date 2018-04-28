import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SERCRET_KEY = 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentSQLiteConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class DevelopmentMySQLConfig(Config):
    DEBUG = True
    user = os.environ.get("MYSQL_USER")
    passwd = os.environ.get("MYSQL_PASSWORD")
    hostname = os.environ.get("MYSQL_HOSTNAME")
    database = os.environ.get("MYSQL_DATABASE")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(user, passwd, hostname, database)


class ProductionConfig(Config):
    DEBUG = False
    user = os.environ.get("MYSQL_USER")
    passwd = os.environ.get("MYSQL_PASSWORD")
    hostname = os.environ.get("MYSQL_HOSTNAME")
    database = os.environ.get("MYSQL_DATABASE")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(user, passwd, hostname, database)


config = {
    'dev_sqlite': DevelopmentSQLiteConfig,
    'dev_mysql': DevelopmentMySQLConfig,
    'production': ProductionConfig,

    'default': DevelopmentSQLiteConfig
}
