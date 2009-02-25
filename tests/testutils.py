import time

def wait_for(condition, timeout=1, msg=None):
    tick = 0.1
    assert timeout > 0, 'timeout should be positive, silly'
    while timeout > 0:
        try:
            assert condition()
            break
        except AssertionError:
            pass
        timeout -= tick
        time.sleep(tick)
    else:
        raise AssertionError(msg)
