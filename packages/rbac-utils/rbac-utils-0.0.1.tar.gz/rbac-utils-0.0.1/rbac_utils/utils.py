import jwt
import requests
from datetime import datetime
from dotenv import dotenv_values
import logging

logger = logging.getLogger('normal')
env = dotenv_values('rbac_utils.env')

def get_from_env(key):
    value = env.get(key)
    if not value:
        logger.error('Error: Could not find the key %s in rbac_utils.env', key)
    return value

ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'
SECRET_KEY = get_from_env('SECRET_KEY')
ALGORITHMS = ['HS256']
RBAC_BASE_URL = get_from_env('RBAC_BASE_URL')
VALIDATE_TOKEN_PATH = "/validate/token"
TOKEN_DATA_PATH = "/update-token-data"
USER_DETAILS_PATH = "/user-details"
VALIDATE_TOKEN_URL = RBAC_BASE_URL + VALIDATE_TOKEN_PATH
TOKEN_DATA_URL = RBAC_BASE_URL + TOKEN_DATA_PATH
USER_DETAILS_URL = RBAC_BASE_URL + USER_DETAILS_PATH
TIMEOUT = 20

class Utils:
    def __init__(self, token):
        self.secret_key = SECRET_KEY
        self.algorithms = ALGORITHMS
        self.decoded_token = None
        self.token = token

    def __get_decoded_token__(self):
        # Decode + signature verification
        logger.info("decoding token")
        return jwt.decode(self.token, self.secret_key, algorithms=self.algorithms)

    def validate_token(self):
        """
            Checks if the token is:
                a. not expired AND
                b. well formed AND
                c. signed by RBAC
        """
        logger.info("validating token")
        try:
            # decode token + signature verification
            decoded_token = self.__get_decoded_token__()

            # expiration checking
            expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
            if expiration_time < datetime.utcnow():
                return False

            return True

        except Exception as exc:
            logger.error("error occured while validating token:\n%s", exc)
            return False
        
    def get_user_roles(self):
        """ Returns roles decoded from the give token """
        roles = []
        logger.info("extracting user roles from token")
        try:
            decoded_token = self.__get_decoded_token__()
            roles = decoded_token['roles']
        except Exception as exc:
            logger.error("error occured while extracting user roles from token:\n%s", exc)

        return roles
    
    def is_user_role_present(self, role):
        """ Returns if the give role is present in the given token """
        logger.info("checking if role %s is present on token", role)
        roles = self.get_user_roles()
        return role in roles

    def get_user_details(self):
        """ Returns { user_id, email and mobile_number } from the given token """
        logger.info("fetching user details")
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.get(
                url=USER_DETAILS_URL,
                params={ 'token': self.token },
                headers=headers,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            res_json = response.json()
            return res_json.get('details')
        except Exception as exc:
            logger.error("error occured while extracting user details from token:\n%s", exc)
            return {}

    def validate_with_server(self):
        """ validate token with server """
        logger.info("validating token with server")
        try:
            data = {
                'token': self.token
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(VALIDATE_TOKEN_URL, json=data, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            res_json = response.json()
            return res_json.get('is_valid', False)
        except Exception as exc:
            logger.error("error occured while validating token with server:\n%s", exc)
            return False

    def update_token_data(self, data):
        """ update data claim in token """
        logger.info("updating token data")
        try:
            data = {
                'token': self.token,
                'data': data
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(TOKEN_DATA_URL, json=data, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            res_json = response.json()
            return res_json.get('token')
        except Exception as exc:
            logger.error("error occured while updating the token data:\n%s", exc)
            return None
