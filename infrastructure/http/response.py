import json
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
import inspect
import logging

class ResponseStatus(Enum):
    SUCCESS = auto()
    ERROR = auto()
    VALIDATION_ERROR = auto()

@dataclass
class RouteConfig:
    service_name: str
    route_path: str
    http_method: str = 'POST'
    description: Optional[str] = None

@dataclass
class ServiceRegistry:
    routes: Dict[str, RouteConfig] = field(default_factory=dict)
    services: Dict[str, Callable] = field(default_factory=dict)

    def register_service(self, service: Callable):
        """
        Automatically register a service based on its name and create a route config
        
        Conversion rules:
        - CreateUserService -> /create-user
        - UpdateProductService -> /update-product
        """
        service_name = service.__name__
        
        # Convert service name to route path
        route_path = '/' + ''.join([
            f'-{char.lower()}' if char.isupper() and i > 0 else char.lower() 
            for i, char in enumerate(service_name.replace('Service', ''))
        ]).lstrip('-')
        
        route_config = RouteConfig(
            service_name=service_name,
            route_path=route_path
        )
        
        self.routes[route_path] = route_config
        self.services[service_name] = service
    
    def load_route_config(self, config_path: str):
        """
        Load additional route configurations from a JSON file
        """
        with open(config_path, 'r') as f:
            custom_routes = json.load(f)
        
        for route_config in custom_routes:
            route = RouteConfig(**route_config)
            self.routes[route.route_path] = route

class ResponseHandler:
    @staticmethod
    def create_response(
        status: ResponseStatus, 
        data: Optional[Any] = None, 
        message: Optional[str] = None,
        errors: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized response object
        
        :param status: Response status enum
        :param data: Successful response data
        :param message: Optional human-readable message
        :param errors: Optional error details
        :return: Standardized response dictionary
        """
        response = {
            'status': status.name.lower(),
            'timestamp': datetime.now().isoformat()
        }
        
        if data is not None:
            response['data'] = data
        
        if message:
            response['message'] = message
        
        if errors:
            response['errors'] = errors
        
        return response

class RouteManager:
    def __init__(self, service_registry: ServiceRegistry, logger: Optional[logging.Logger] = None):
        """
        Initialize route manager with service registry
        
        :param service_registry: Configured ServiceRegistry
        :param logger: Optional logging instance
        """
        self.registry = service_registry
        self.logger = logger or logging.getLogger(__name__)
    
    def execute_service(self, route_path: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the service associated with a route
        
        :param route_path: Incoming request route
        :param request_data: Request payload
        :return: Standardized response
        """
        try:
            # Find route configuration
            route_config = self.registry.routes.get(route_path)
            if not route_config:
                return ResponseHandler.create_response(
                    status=ResponseStatus.ERROR,
                    message=f"No service found for route: {route_path}",
                    errors={'route': 'Not found'}
                )
            
            # Get corresponding service
            service = self.registry.services.get(route_config.service_name)
            if not service:
                return ResponseHandler.create_response(
                    status=ResponseStatus.ERROR,
                    message=f"Service implementation not found: {route_config.service_name}",
                    errors={'service': 'Not implemented'}
                )
            
            # Validate input parameters
            service_signature = inspect.signature(service)
            try:
                bound_arguments = service_signature.bind(**request_data)
                bound_arguments.apply_defaults()
            except TypeError as validation_error:
                return ResponseHandler.create_response(
                    status=ResponseStatus.VALIDATION_ERROR,
                    message="Input validation failed",
                    errors={'validation': str(validation_error)}
                )
            
            # Execute service
            result = service(**request_data)
            
            return ResponseHandler.create_response(
                status=ResponseStatus.SUCCESS,
                data=result,
                message=f"Successfully executed {route_config.service_name}"
            )
        
        except Exception as e:
            self.logger.exception(f"Service execution error for {route_path}")
            return ResponseHandler.create_response(
                status=ResponseStatus.ERROR,
                message="Internal service error",
                errors={'exception': str(e)}
            )

# Example usage demonstration
def CreateUserService(username: str, email: str, password: str):
    """Example service for creating a user"""
    # Simulated user creation logic
    return {
        'user_id': 'generated_unique_id',
        'username': username,
        'email': email
    }

def UpdateProductService(product_id: str, name: str, price: float):
    """Example service for updating a product"""
    # Simulated product update logic
    return {
        'product_id': product_id,
        'updated_name': name,
        'updated_price': price
    }

def main():
    # Initialize service registry
    registry = ServiceRegistry()
    
    # Register services (automatic route generation)
    registry.register_service(CreateUserService)
    registry.register_service(UpdateProductService)
    
    # Optional: Load custom route configurations
    # registry.load_route_config('routes.json')
    
    # Create route manager
    route_manager = RouteManager(registry)
    
    # Simulate route execution
    create_user_response = route_manager.execute_service(
        '/create-user', 
        {'username': 'johndoe', 'email': 'john@example.com', 'password': 'secure_pass'}
    )
    print(json.dumps(create_user_response, indent=2))
    
    update_product_response = route_manager.execute_service(
        '/update-product', 
        {'product_id': 'prod_123', 'name': 'Updated Product', 'price': 29.99}
    )
    print(json.dumps(update_product_response, indent=2))

if __name__ == '__main__':
    main()