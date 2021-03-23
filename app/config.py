import os

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-super-secret-key'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://rhhixcdomamkvc:8d0bb086ced3f64949a7df52d05b16cc6cfc3d1febbc532641f43cf6306f42f6@ec2-23-21-229-200.compute-1.amazonaws.com:5432/d33cq9sjt4qji8'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://project_1:marcg@localhost/project_1'
    SQLALCHEMY_TRACK_MODIFICATIONS = True # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
    UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER'] = 'uploads' 

class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False



