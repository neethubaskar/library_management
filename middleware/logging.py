import logging

logging.basicConfig(filename="logs/api.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_request(endpoint: str, method: str, user: str):
    logging.info(f"Endpoint: {endpoint} | Method: {method} | User: {user}")

def log_error(error_message: str):
    logging.error(f"Error: {error_message}")
