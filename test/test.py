import unittest
from chipi import Buffer, BufferManager


class TestBuffer(unittest.TestCase):

    def test_buffer(self):
        buf = Buffer("test")
        self.assertEqual(buf.label, "test")
        self.assertEqual(buf.len, 0)
        self.assertEqual(buf.current_value, None)
        self.assertEqual(buf.previous_value, None)
        self.assertTrue(buf.is_empty)

        buf.add(1)
        self.assertEqual(buf.len, 1)
        self.assertEqual(buf.current_value, 1)
        self.assertEqual(buf.previous_value, None)
        self.assertFalse(buf.is_empty)

        buf.add(2)
        self.assertEqual(buf.len, 2)
        self.assertEqual(buf.current_value, 2)
        self.assertEqual(buf.previous_value, 1)

        buf.clear()
        self.assertEqual(buf.len, 0)
        self.assertEqual(buf.current_value, None)
        self.assertEqual(buf.previous_value, None)
        self.assertTrue(buf.is_empty)

    def test_buffer_methods(self):
        buf = Buffer("test")

        # Test add and delta methods
        buf.add(1)
        buf.add(3)
        self.assertEqual(buf.delta(), 2)

        # Test delete method
        buf.delete(0)
        self.assertEqual(buf.len, 1)
        self.assertEqual(buf.current_value, 3)

        # Test find_duplicate method
        buf.clear()
        buf.add(4)
        buf.add(3)
        self.assertEqual(buf.find_duplicate(3), 1)
        self.assertEqual(buf.find_duplicate(4), 0)

        # Test point_diff method
        buf.clear()
        buf.add(3)
        buf.add(4)
        self.assertEqual(buf.point_diff(0, 1), 1)

        # Test has_difference method
        self.assertTrue(buf.has_difference())

        # Test has_non_numeric_difference method
        buf.clear()
        buf.add("apple")
        buf.add("banana")
        self.assertTrue(buf.has_non_numeric_difference())

        # Test reverse method
        buf.clear()
        buf.add(1)
        buf.add(2)
        buf.add(3)
        buf.reverse()
        self.assertEqual(buf.data, [3, 2, 1])

        # Test sort method
        buf.sort(reverse=True)
        self.assertEqual(buf.data, [3, 2, 1])

        # Test filter method
        filtered_data = buf.filter(lambda x: x % 2 == 0)
        self.assertEqual(filtered_data, [2])

        # Test resample method
        resampled_data = buf.resample(2)
        self.assertEqual(resampled_data, [3, 1])

        # Test slice method
        sliced_data = buf.slice(0, 2)
        self.assertEqual(sliced_data, [3, 2])

        # Test find method
        found_index = buf.find(lambda x: x == 2)
        self.assertEqual(found_index, 1)

        # Test max_value and min_value methods
        self.assertEqual(buf.max_value(), 3)
        self.assertEqual(buf.min_value(), 1)

        # Test mean method
        self.assertEqual(buf.mean(), 2.0)

        # Test unique method
        buf.clear()
        buf.add(1)
        buf.add(1)
        buf.add(2)
        buf.add(2)
        buf.add(3)
        buf.add(3)
        buf.add(3)
        self.assertEqual(buf.unique(), [1, 2, 3])

class TestBufferManager(unittest.TestCase):

    def test_buffer_manager(self):
        buf_mgr = BufferManager(["A", "B", "C"])
        self.assertEqual(len(buf_mgr.d), 3)

        buf_mgr.d["A"].add(1)
        buf_mgr.d["A"].add(2)
        buf_mgr.d["B"].add(3)

        self.assertEqual(buf_mgr.get_data("A"), [1, 2])
        self.assertEqual(buf_mgr.get_data("B"), [3])

        buf_mgr.clear("A")
        self.assertEqual(buf_mgr.get_data("A"), [])

        buf_mgr.copy_data("B", "A")
        self.assertEqual(buf_mgr.get_data("A"), [3])
        self.assertEqual(buf_mgr.get_data("B"), [3])

        buf_mgr.move_data("A", "C")
        self.assertEqual(buf_mgr.get_data("A"), [])
        self.assertEqual(buf_mgr.get_data("C"), [3])

if __name__ == '__main__':
    unittest.main()
