import json
import os
import unittest
from modelbest_data.file_format.mbtable import MbTable, MbTableIterator
from modelbest_data.file_format.mbtable_builder import MbTableBuilder


class TestMbTable(unittest.TestCase):
    def setUp(self):
        self.path = "test/data/single_file_padding_key.mbt"
        builder = MbTableBuilder(self.path)
        for i in range(100):
            builder.set_kv(f"{i:0{2}}", json.dumps({"col": f"value_{i}"}))
        builder.set_metadata("meta_key", "meta_value")
        builder.build()
        self.mbtable = MbTable(self.path)
    
    def tearDown(self):
        os.remove(self.path)
    
    def test_get_value(self):
        self.assertEqual(self.mbtable.get_value("00"), json.dumps({"col": "value_0"}).encode())
        self.assertEqual(self.mbtable.get_value("99"), json.dumps({"col": "value_99"}).encode())
        self.assertEqual(self.mbtable.get_value("100"), b'')
        self.assertEqual(self.mbtable.get_value("abc"), b'')
        
    def test_get_metadata(self):
        self.assertEqual(self.mbtable.get_metadata("meta_key"), b"meta_value")
        self.assertEqual(self.mbtable.get_metadata("not_exist"), b'')
    
    def test_get_entry_count(self):
        self.assertEqual(self.mbtable.get_entry_count(), 100)
    
    
class TestMbTableIterator(TestMbTable):
    def pad_key(self, key):
        return f"{key:0{2}}"
        
    def test_iterator(self):
        cnt = 0
        with MbTableIterator(self.path) as iterator:    
            for key, value in iterator:
                self.assertEqual(key, f"{cnt:0{2}}".encode())
                self.assertEqual(value, json.dumps({"col": f"value_{cnt}"}).encode())
                cnt += 1
        assert cnt == 100
    
    def test_iterator_with_args(self):
        key, cnt = 50, 0
        with MbTableIterator(self.path, start_key=self.pad_key(key), max_iterations=10) as iterator:  
            for _, _ in iterator:
                cnt += 1
        assert cnt == 10
        
        key, cnt = 99, 0
        with MbTableIterator(self.path, start_key=self.pad_key(key), max_iterations=1000) as iterator:  
            for _, _ in iterator:
                cnt += 1
        assert cnt == 1
    
        key, cnt = 1000, 0
        # !!! note that key in mbtable is string and is sorted in lexicographic order
        # so key 1000 is greater than 10 but less than 11, this would start from 11
        with MbTableIterator(self.path, start_key=self.pad_key(key), max_iterations=1000) as iterator:  
            for _, _ in iterator:
                cnt += 1
        assert cnt == 89
    
    def test_iterator_raw(self):
        iterator = MbTableIterator(self.path)
        iterator.__enter__()
        k, v = iterator.__next__()
        iterator.__exit__(None, None, None)
        self.assertEqual(k, b"00")
        self.assertEqual(v, json.dumps({"col": "value_0"}).encode())
        pass
        

                
if __name__ == '__main__':
    unittest.main()
    