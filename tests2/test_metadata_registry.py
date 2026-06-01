from src.data.cache.metadata_registry import (
    MetadataRegistry
)


metadata = MetadataRegistry.load_metadata(
    ticker="GC=F",
    interval="1d"
)

print(metadata)