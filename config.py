import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI =  'mysql://admin:pknu1234@pknu.cmqhog94n5bp.ap-northeast-2.rds.amazonaws.com:3306/Test'
