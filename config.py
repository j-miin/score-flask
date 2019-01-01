import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # S3_KEY = os.environ['S3_KEY']
    # S3_SECRET = os.environ['S3_SECRET']
    # S3_BUCKET = os.environ['S3_BUCKET']
    # S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
    # SENDGRID_API_KEY=os.environ['SENDGRID_API_KEY']
    # GOOGLE_CLIENT_ID=os.environ['GOOGLE_CLIENT_ID']
    # GOOGLE_CLIENT_SECRET=os.environ['GOOGLE_CLIENT_SECRET']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
