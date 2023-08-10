import pytest
from app.models.post import Post


def test_post_is_created():
    new_post = Post(id=1, description="hello", priority=2)
    assert type(new_post) == Post
    assert new_post.id == 1
    assert new_post.description == "hello"
    assert new_post.priority == 2


def test_post_is_not_created():
    with pytest.raises(TypeError):
        bad_post = Post(id=1)
