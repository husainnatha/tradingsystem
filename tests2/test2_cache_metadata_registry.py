from src.data.cache.metadata_registry import (
    MetadataRegistry
)

def test_cache_metadata_registry ():

    metadata = MetadataRegistry.load_metadata(
        ticker="GC=F",
        interval="1d"
    )

    print(metadata)

    assert True