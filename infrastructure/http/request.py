import requests
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum, auto
import logging

class HTTPMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()

@dataclass
class ServiceConfig:
    base_url: str
    endpoint: str
    method: HTTPMethod
    headers: Optional[Dict[str, str]] = None
    auth_type: Optional[str] = None
    auth_config: Optional[Dict[str, Any]] = None

class ExternalServiceClient:
    def __init__(self, config: ServiceConfig, logger: Optional[logging.Logger] = None):
        """
        Initialize the external service client with configuration.
        
        :param config: ServiceConfig object with request details
        :param logger: Optional logger for tracking requests and errors
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
    
    def _prepare_authentication(self, session: requests.Session):
        """
        Prepare authentication based on config type.
        
        :param session: Requests session to modify
        :raises ValueError: If unsupported auth type is provided
        """
        if not self.config.auth_type:
            return
        
        auth_config = self.config.auth_config or {}
        
        if self.config.auth_type == 'basic':
            session.auth = (auth_config.get('username'), auth_config.get('password'))
        elif self.config.auth_type == 'bearer':
            session.headers.update({
                'Authorization': f"Bearer {auth_config.get('token')}"
            })
        elif self.config.auth_type == 'api_key':
            key_location = auth_config.get('location', 'headers')
            key_name = auth_config.get('key_name', 'X-API-Key')
            
            if key_location == 'headers':
                session.headers.update({key_name: auth_config.get('key')})
            elif key_location == 'params':
                session.params = session.params or {}
                session.params[key_name] = auth_config.get('key')
        else:
            raise ValueError(f"Unsupported authentication type: {self.config.auth_type}")
    
    def request(self, payload: Optional[Dict[str, Any]] = None, 
                params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the configured service endpoint.
        
        :param payload: Optional request body for POST/PUT/PATCH
        :param params: Optional query parameters
        :return: Response JSON
        :raises requests.RequestException: For network/HTTP errors
        """
        full_url = f"{self.config.base_url.rstrip('/')}/{self.config.endpoint.lstrip('/')}"
        
        session = requests.Session()
        session.headers.update(self.config.headers or {})
        
        self._prepare_authentication(session)
        
        try:
            method_map = {
                HTTPMethod.GET: session.get,
                HTTPMethod.POST: session.post,
                HTTPMethod.PUT: session.put,
                HTTPMethod.DELETE: session.delete,
                HTTPMethod.PATCH: session.patch
            }
            
            request_method = method_map.get(self.config.method)
            
            if not request_method:
                raise ValueError(f"Unsupported HTTP method: {self.config.method}")
            
            response = request_method(
                full_url, 
                json=payload, 
                params=params
            )
            
            response.raise_for_status()
            
            return response.json()
        
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    @classmethod
    def from_config_file(cls, config_path: str, logger: Optional[logging.Logger] = None):
        """
        Create a client from a JSON configuration file.
        
        :param config_path: Path to JSON configuration file
        :param logger: Optional logger
        :return: ExternalServiceClient instance
        """
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        
        config_dict['method'] = HTTPMethod[config_dict.get('method', 'GET')]
        
        config = ServiceConfig(**config_dict)
        return cls(config, logger)

# Example usage
def main():
    # Example configuration for GitHub API
    github_config = ServiceConfig(
        base_url='https://api.github.com',
        endpoint='/users/octocat',
        method=HTTPMethod.GET,
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    
    client = ExternalServiceClient(github_config)
    
    try:
        response = client.request()
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()