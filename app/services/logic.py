from app.models.models import Photo, db
from datetime import datetime
from flask import current_app

def get_user_daily_count(user_id):
    """Calcule le nombre de photos uploadées aujourd'hui par l'utilisateur."""
    today = datetime.utcnow().date()
    return Photo.query.filter(
        Photo.user_id == user_id, 
        db.func.date(Photo.upload_date) == today
    ).count()

def can_user_upload(user):
    """Logique système : dépend de l'utilisateur et de la DB."""
    limit = get_package_limit(user.package) 
    current_count = get_user_daily_count(user.id)
    return current_count < limit

def get_package_limit(package_name):
    """Renvoie la limite numérique selon le nom du package (Utile pour O2/O5)"""
    limits = {'FREE': 2, 'PRO': 100}
    return limits.get(package_name, 0)