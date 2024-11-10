from abc import ABC, abstractmethod


class Service(ABC):
    """
    Abstract base controller class defining structure for CRUD operations.
    """
    @abstractmethod
    def post(self):
        """Create a new item
        """
        pass
    
    @abstractmethod
    def get(self):
        """Fetch single item 
        """
        pass
    
    @abstractmethod
    def put(self):
        """Update an existing item
        """
        pass
    
    @abstractmethod
    def patch(self):
        """ Update existing item
        """
        pass
 
    @abstractmethod
    def delete(self, id: int):
        """delete an existing item by ID

        Args:
            id (int): item ID
        """
        pass