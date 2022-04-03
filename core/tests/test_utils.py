import uuid

from ..utils import generate_uuid_4


def test_generate_uuid_4_returns_builtin_uuid4():
    assert type(generate_uuid_4()) == type(uuid.uuid4())
