#!/usr/bin/python3
"""Doc
"""
from models.engine.tmp_file_storage import FileStorage


class FileStorage(FileStorage):
    """Doc
    """

    def count(self, cls=None):
        """
        returns the count of object or specific class
        """
        return -1