import pytest

if __name__ == "__main__":
    pytest.main(["-vv","--disable-warnings","-s", "app/tests/test_user.py"])
    # pytest.main(["-vv","--disable-warnings","-s", "app/tests/test_blog.py"])
    # pytest.main(["-vv","--disable-warnings","-s", "app/tests/test_comments.py"])