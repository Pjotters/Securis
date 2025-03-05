import logging
from datetime import datetime
import os

class SecurityLogger:
    def __init__(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"security_{datetime.now():%y%m%d}.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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