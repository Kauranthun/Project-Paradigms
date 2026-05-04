import os

class Config:
    SECRET_KEY = 'votre_cle_secrete'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///photos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    
    LIMITS = {
        'FREE': 2,
        'PRO': 100
    }