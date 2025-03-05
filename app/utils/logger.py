import logging
from datetime import datetime
import os

class SecurityLogger:
    def __init__(self):
        # Configureer logging
        logging.basicConfig(
            filename=f'logs/security_{datetime.now().strftime("%Y%m")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def log_login_attempt(self, user_id, success, method, ip):
        logging.info(
            f"Login poging - Gebruiker: {user_id}, "
            f"Methode: {method}, IP: {ip}, "
            f"Status: {'Succesvol' if success else 'Mislukt'}"
        )
        
    def log_registration(self, user_id, ip):
        logging.info(
            f"Nieuwe registratie - Gebruiker: {user_id}, IP: {ip}"
        )
        
    def log_security_event(self, event_type, details):
        logging.warning(
            f"Beveiligingsgebeurtenis - Type: {event_type}, Details: {details}"
        ) 