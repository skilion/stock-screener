import scheduler
import unittest

class TestScheduler(unittest.IsolatedAsyncioTestCase):
    async def test_get_time_series_compact(self):
        # Arrange
        count = 0
        target = 100
        async def increase():
            nonlocal count
            print(count)
            count = count + 1

        # Act
        await scheduler.run_parallel([increase() for _ in range(target)])

        # Assert
        assert count == target
