import requests
import json
from dotenv import dotenv_values
import logging
import jwt

logger = logging.getLogger('normal')
env = dotenv_values('rbac_utils.env')

def get_from_env(key):
    """
    Get a value from environment variables.
    """
    value = env.get(key)
    if not value:
        logger.error('Error: Could not find the key %s in rbac_utils.env', key)
    return value

RBAC_API_KEY = get_from_env('RBAC_API_KEY')
RBAC_BASE_URL = get_from_env('RBAC_BASE_URL')

GENERATE_TOKEN_URL = RBAC_BASE_URL + "/generate-token"
USER_DETAILS_URL = RBAC_BASE_URL + "/user-details"
REFRESH_TOKEN_URL = RBAC_BASE_URL + "/refresh-token"
REVOKE_USER_TOKENS_URL = RBAC_BASE_URL + "/revoke-token"
UPDATE_TOKEN_DATA_URL = RBAC_BASE_URL + "/update-token-data"

TIMEOUT = 20

class Utils:
    @classmethod
    def generate_user_tokens(cls, user_id, data=None):
        """
        Generate user tokens (access token and refresh token) for the given user_id.

        Args:
            user_id (str): The identifier of the user for whom tokens are generated.
            data (dict): A dictionary containing custom key-value pairs. 
                         This dictionary is added as a value to the data key of the token.

        Returns:
            dict: A dictionary containing the generated access token and refresh token.
                  An empty dictionary is returned if the generation process fails.
        """
        payload_dict = {
            "user_id": user_id
        }
        if data:
            payload_dict['data'] = data
        payload = json.dumps(payload_dict)
        headers = {
            'X-API-KEY': RBAC_API_KEY,
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(
                GENERATE_TOKEN_URL,
                headers=headers,
                data=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()
            access_token = response_json['access_token']
            refresh_token = response_json['refresh_token']
            return dict(
                access_token=access_token,
                refresh_token=refresh_token
            )
        except Exception as exc:
            # logger.error('Error generating user tokens')
            return {}

    @classmethod
    def validate_access_token(cls, access_token):
        """
        Validate an access token and retrieve user details.

        Args:
            access_token (str): The access token to be validated.

        Returns:
            dict: A dictionary containing user details if the token is valid.
                  An empty dictionary is returned if validation fails.
        """
        payload = json.dumps({
            "token": access_token
        })
        headers = {
            'content-type': 'application/json',
        }
        try:
            response = requests.post(
                USER_DETAILS_URL,
                headers=headers,
                data=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()
            details = response_json['details']
            return {'is_valid': True, 'user_details': details}
        except Exception as exc:
            # logger.error('Error validating access token')
            return {'is_valid': False, 'user_details': {}}

    @classmethod
    def refresh_user_tokens(cls, refresh_token):
        """
        Refresh user tokens using a refresh token.

        Args:
            refresh_token (str): The refresh token used to obtain new tokens.

        Returns:
            dict: A dictionary containing the new access token and refresh token.
                  An empty dictionary is returned if token refresh fails.
        """
        payload = json.dumps({
            "token": refresh_token
        })
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(
                REFRESH_TOKEN_URL,
                headers=headers,
                data=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()
            new_access_token = response_json['access_token']
            new_refresh_token = response_json['refresh_token']
            return dict(
                access_token=new_access_token,
                refresh_token=new_refresh_token
            )
        except Exception as exc:
            # logger.error('Error trying to refresh token')
            return {}

    @classmethod
    def revoke_user_tokens(cls, access_token, refresh_token):
        """
        Revoke user tokens.

        Args:
            access_token (str): The access token to be revoked.
            refresh_token (str): The refresh token to be revoked.

        Returns:
            bool: True if the tokens were successfully revoked, False otherwise.
        """
        payload = json.dumps({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(
                REVOKE_USER_TOKENS_URL,
                headers=headers,
                data=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return True
        except Exception as exc:
            # logger.error('Error trying to revoke user tokens')
            return {}

    @classmethod
    def update_token_data(cls, access_token, data):
        """
        Update a user's access token with new data.
        NOTE: The existing access token will be invalidated after the update and the newly returned one takes its place.

        Args:
            access_token (str): The access token to be updated.
            data (dict): New data to be added to the access token.

        Returns:
            str: The (a new string) updated access token with the new data.
                  None is returned if the update fails.
        """
        payload = json.dumps({
            "data": data,
            "token": access_token
        })
        headers = {
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(
                UPDATE_TOKEN_DATA_URL,
                headers=headers,
                data=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()
            return response_json['token']
        except Exception as exc:
            # logger.error('Error trying to update token data')
            return None

    @classmethod
    def extract_token_claims(cls, token):
        """
        Extract token claims.

        Args:
            token (str): The JWT from which claims will be extracted.

        Returns:
            dict: A dictionary containing the claims from the JWT.
                  An empty dictionary is returned if decoding fails.
        """
        try:
            claims = jwt.decode(token, algorithms=["none"], options=dict(verify_signature=False))
            return claims
        except Exception as exc:
            # logger.error('Error extracting token claims')
            return {}

