import logging

import pytest

from app.models.rss import RSSFeed
from app.services.database import AsyncSession
from tests.helper import test_feeds


def pytest_configure():
    logging.getLogger("vcr").setLevel(logging.WARNING)


@pytest.fixture(scope="package", autouse=True)
async def async_test_db():
    feed1 = RSSFeed(**test_feeds[0])
    feed2 = RSSFeed(**test_feeds[1])
    async with AsyncSession() as async_session:
        async_session.add(feed1)
        async_session.add(feed2)
        await async_session.commit()
        await async_session.flush()
        await async_session.refresh(feed1)
        await async_session.refresh(feed2)
    yield


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("authorization", "DUMMY")],
        "cassette_library_dir": "tests/data/cassettes",
        "decode_compressed_response": True,
        "log": None,
    }
