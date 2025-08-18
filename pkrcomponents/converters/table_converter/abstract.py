import json
from abc import ABC, abstractmethod
from pkrcomponents.components.tables.table import Table


class AbstractTableConverter(ABC):
    """
    Abstract class to convert pkrcomponents Table to JSON
    """
    data: dict
    table: Table

    def __init__(self, table: Table):
        self.data = {}
        self.table = table