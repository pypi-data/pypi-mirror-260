# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   user.py
    :param Author       :   Sudo
    :param Date         :   2/02/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   #
    :param Description  :   #
"""
__author__ = 'Data engineering team'
__copyright__ = 'Copyright (c) 2024 Ryght, Inc. All Rights Reserved.'

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import os
import uuid
import logging

from ryght.clients import ApiClient
from ryght.configs import Credentials
from ryght.utils import FlowTypes, ModelOperation
from ryght.models import Documents, Collection, AIModels

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class RyghtClient:
    id: uuid.UUID = uuid.uuid4()
    api_client: ApiClient

    def __init__(self, user_credentials: dict | Credentials = None, env_path: str = None):
        logger.debug(f'Ryght client ID: {self.id}\n\n')
        self.api_client = ApiClient()
        if isinstance(user_credentials, dict):
            self.api_client.token_manager.credentials = Credentials(**user_credentials)
        elif isinstance(user_credentials, Credentials):
            self.api_client.token_manager.credentials = user_credentials
        elif env_path and os.path.isfile(env_path):
            credentials = Credentials(_env_file=env_path)
            self.api_client.token_manager.credentials = credentials

        self.api_client.token_manager.get_new_token()

    def list_collections(self) -> list[Collection]:
        return self.api_client.search_collections()

    def get_collection_by_id(self, collection_id: str) -> Collection:
        return self.api_client.get_collection_details(collection_id)

    def completions(
            self,
            input_str: str,
            collection_ids: str,
            flow: FlowTypes = FlowTypes.SEARCH,
            search_limit: int = 5,
            completion_model_id: str = None,
            document_ids=None
    ):
        if document_ids is None:
            document_ids = []
        return self.api_client.perform_completions(
            input_str,
            collection_ids,
            flow,
            search_limit,
            completion_model_id,
            document_ids
        )

    def list_models(self) -> list[AIModels]:
        return self.api_client.get_ai_models()

    def get_model(self, model_id: str = None) -> AIModels:
        return self.api_client.get_ai_model_by_id(model_id)

    def get_model_by_operation(self, operation: ModelOperation = ModelOperation.EMBEDDING) -> list[AIModels]:
        return self.api_client.get_ai_models_by_operation(operation)

    # Documents
    def upload_new_document(self, documents_path: str, file_name: str, tag_ids: list = None) -> str:
        return self.api_client.upload_documents(
            documents_path,
            file_name,
            tag_ids=tag_ids
        )

    def get_default_collections(self) -> list[Documents]:
        return self.api_client.get_document_collection()

    def get_document_by_id(self, document_id: str) -> Documents:
        return self.api_client.get_document_by_id(document_id)

    def delete_document_by_id(self, document_id: str) -> Documents:
        return self.api_client.delete_document_by_id(document_id)

    def rename_document(self, document_id: str, new_name: str) -> str:
        return self.api_client.rename_document(document_id, new_name)

# -------------------------------------------------------------------------------------------------------------------- #
