import importlib.metadata

from sword_converter import __name__ as distribution_name

_metadata = importlib.metadata.metadata(distribution_name)

name = _metadata["Name"]
summary = _metadata["Summary"]
version = _metadata["Version"]
