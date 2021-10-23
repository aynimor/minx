import time
from response import text


def test(request):
    return text("Hello World!")


def test_sleep(request):
    time.sleep(5)
    return text("Hello World!")
