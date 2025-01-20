import logging
import re
from unidecode import unidecode

# Créer et configurer le logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Ajouter un FileHandler pour écrire les logs dans un fichier .log
file_handler = logging.FileHandler('src/logs/log.log')  # Le fichier de logs (application.log)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Ajouter le FileHandler au logger
logger.addHandler(file_handler)

# Fonction de logs
def logs(message, level=logging.INFO):
    message = unidecode(message)  # Supprimer les accents
    message = message.encode('utf-8', 'ignore').decode('utf-8')  # Supprimer les caractères spéciaux
    #message = message.replace(" ", "\ ")  # Remplacer les espaces par \ (optionnel)
    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.INFO:
        logger.info(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)