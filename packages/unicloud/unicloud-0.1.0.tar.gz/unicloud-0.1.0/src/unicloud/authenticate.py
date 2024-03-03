"""Authenticate."""
import base64
import json
import os

from google.cloud import storage
from google.oauth2 import service_account as service_account_gcp


def create_client(
    project_id: str,
    your_service_key: str = None,
) -> storage.client.Client:
    """create_client.

        the returned client deals with everything related to the specific project.

    Parameters
    ----------
    project_id: [str]
        project id
    your_service_key: [string]
        path to your saved api-key json file

    Returns
    -------
    google cloud storage client object
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        credentials = service_account_gcp.Credentials.from_service_account_file(
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        )
        client = storage.Client(project=project_id, credentials=credentials)
    elif "EE_PRIVATE_KEY" in os.environ and "EE_SERVICE_ACCOUNT" in os.environ:
        # key need to be decoded into a dict/json object
        service_key_content = base64.b64decode(
            eval(f"b'{os.environ['EE_PRIVATE_KEY']}'")
        ).decode()

        service_key_content = json.loads(service_key_content)
        # connection to the service account
        client = storage.Client.from_service_account_info(service_key_content)
    elif your_service_key:
        credentials = service_account_gcp.Credentials.from_service_account_file(
            your_service_key
        )
        client = storage.Client(project=project_id, credentials=credentials)
    else:
        raise ValueError(
            "Since the GOOGLE_APPLICATION_CREDENTIALS and the EE_PRIVATE_KEY and EE_SERVICE_ACCOUNT are not in your env variables you have to provide a path to your service account"
        )

    return client
