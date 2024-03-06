# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   api.py
    :param Author       :   Sudo
    :param Date         :   2/07/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   #
    :param Description  :   #
"""
__author__ = 'Data engineering team'
__copyright__ = 'Copyright (c) 2024 Ryght, Inc. All Rights Reserved.'

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import time
import logging
from json import JSONDecodeError

from ryght.models import Token
from ryght.models import ApiEndpoints
from ryght.configs import Credentials
from ryght.utils import RequestMethods
from ryght.managers import TokenManager
from ryght.requests import HttpxRequestExecutor

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class ApiInterface:
    credentials: Credentials
    api_endpoints: ApiEndpoints
    token_manager: TokenManager
    http_request_exec: HttpxRequestExecutor

    def __init__(self):
        self.api_endpoints = ApiEndpoints.load_api_endpoints()
        self.http_request_exec = HttpxRequestExecutor()
        self.token_manager: TokenManager = TokenManager(
            token=Token.init_as_none(),
            credentials=Credentials.init_none(),
            requestor=self.http_request_exec,
            auth_url=self.api_endpoints.auth_token_url
        )

    @TokenManager.authenticate
    def execute_request(
            self,
            method: RequestMethods,
            url,
            **kwargs
    ) -> dict:

        request_fn = None  # placeholder for passing function
        try:
            if method == RequestMethods.GET:
                request_fn = self.http_request_exec.get
            elif method == RequestMethods.PUT:
                request_fn = self.http_request_exec.put
            elif method == RequestMethods.POST:
                request_fn = self.http_request_exec.post
            elif method == RequestMethods.PATCH:
                request_fn = self.http_request_exec.patch
            elif method == RequestMethods.DELETE:
                request_fn = self.http_request_exec.delete
            else:
                raise ValueError(f'Unknown method {method}')

            response = request_fn(url=url, **kwargs)
            if response.status_code in [401, 403, 404]:
                logger.error(
                    f'Got client error: {response.status_code}, Please check your credential & api endpoint variables'
                )
                response.raise_for_status()
            elif response.status_code in [500]:
                logger.error('Got client error: 500, attempting new token request after 5 seconds')
                time.sleep(5)
                response = request_fn(url=url, **kwargs)
                response.raise_for_status()

        except ValueError as value_error:
            logger.error(f'ValueError occurred: {value_error}')
        except Exception as exception:
            logger.error('Exception occurred: {}'.format(exception))
        else:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 201:
                return f'Success! response code: {response.status_code}'

            elif response.status_code in [202, 203, 204]:
                if response.text is not None and response.text != '':
                    value = response.text
                else:
                    value = f'Success! response code: {response.status_code}'
                return value

            else:
                logger.error(f'Unknown response status code: {response.status_code}')

# -------------------------------------------------------------------------------------------------------------------- #
