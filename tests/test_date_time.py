import unittest
from util.date_time import get_next_quarter


class TestDateTime(unittest.TestCase):
    def test_next_quarter(self):
        for hour in range(24):
            for minute in range(60):
                r_hour, r_minute = get_next_quarter(hour, minute)

                if minute < 15:
                    self.assertEqual(r_hour, hour)
                    self.assertEqual(r_minute, 15)
                    continue

                if minute < 30:
                    self.assertEqual(r_hour, hour)
                    self.assertEqual(r_minute, 30)
                    continue

                if minute < 45:
                    self.assertEqual(r_hour, hour)
                    self.assertEqual(r_minute, 45)
                    continue

                self.assertEqual(r_hour, (hour + 1) % 24)
                self.assertEqual(r_minute, 0)

    def test_hour_overflow(self):
        for minute in range(60):
            with self.assertRaises(AssertionError):
                get_next_quarter(24, minute)

    def test_minute_overflow(self):
        for hour in range(24):
            with self.assertRaises(AssertionError):
                get_next_quarter(hour, 60)

if __name__ == '__main__':
    unittest.main()
