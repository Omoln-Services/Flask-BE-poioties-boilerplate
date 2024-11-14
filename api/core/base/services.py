from abc import ABC, abstractmethod


class Service(ABC):
    """
    Abstract base service class defining structure for CRUD operations.
    """

    @abstractmethod
    def post(self, *args, **kwargs):
        """Create a new item"""
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        """Fetch single item"""
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        """Update an existing item"""
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """delete an existing item"""
        pass
