import requests
from cms import aes_utils
from loguru import logger


# Makes API call, gets encrypted creds, decrypts creds
# using aes_utils and returns decrypted creds
def get_cred(uuid, cred_url, auth_token, iv, key):
    headers = {
        'Content-Type': 'application/json',
        f'Authorization': auth_token
    }

    data = {'uuid': uuid}

    try:
        response = requests.post(cred_url, headers=headers, json=data, verify=False)

        if response.status_code == 200:
            logger.info("Request successful!")
            json_dict = response.json()
            encrypted_cred = json_dict.get("responseData", {}).get("value")

            logger.debug(f"Raw response from API {response.text}")
            logger.debug(f"Got encrypted_cred from api {encrypted_cred}")

            try:
                decrypted_cred = aes_utils.decrypt(encrypted_cred, 'AES', iv, key)
                logger.debug(f"decrypted_cred : {decrypted_cred}")
                return decrypted_cred
            except Exception as e:
                decrypted_cred = aes_utils.decrypt(encrypted_cred, 'BASE64', iv, key)
                logger.debug(f"decrypted_cred : {decrypted_cred}")
                return decrypted_cred

        else:
            logger.error(f"Request failed with status code {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None
