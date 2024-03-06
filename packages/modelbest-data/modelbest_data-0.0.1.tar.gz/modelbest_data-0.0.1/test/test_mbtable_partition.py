import os
import unittest
from modelbest_data.file_format.mbtable_builder import MbTableBuilder
from modelbest_data.file_format.mbtable_partition import MbTablePartition, MbTablePartitionIterator


class TestMbTablePartition(unittest.TestCase):
    def setUp(self):
        for i in range(10):
            builder = MbTableBuilder(f"test/data/part_{i}.mbt")
            for j in range(100):
                key_formatted = f"{j:0{4}}"
                builder.set_kv(key_formatted, str({"col": f"value_{j}"}))
            builder.set_metadata("meta_key", "meta_value")
            builder.build()
        self.mbtable_partition = MbTablePartition("test/data")
    
    def tearDown(self):
        for i in range(10):
            file_path = f"test/data/part_{i}.mbt"
            if os.path.exists(file_path):
                os.remove(file_path)
                
    def test_get_total_count(self):
        self.mbtable_partition.get_total_count()
        assert self.mbtable_partition.total_count == 1000
                
    def test_get_file_and_position(self):
        file, postion = self.mbtable_partition.get_file_and_position(0)
        assert file == "test/data/part_0.mbt"
        assert postion == 0
        
        file, postion = self.mbtable_partition.get_file_and_position(999)
        assert file == "test/data/part_9.mbt"
        assert postion == 99
        
        file, postion = self.mbtable_partition.get_file_and_position(1001)
        assert file == None
        assert postion == None
    
    def test_get_next_file(self):
        next_file = self.mbtable_partition.get_next_file("test/data/part_0.mbt")
        assert next_file == "test/data/part_1.mbt"
        
        next_file = self.mbtable_partition.get_next_file("test/data/part_9.mbt")
        assert next_file == None
        
class TestMbTablePartitionIterator(TestMbTablePartition):
    def test_iterator(self):
        cnt = 0
        with MbTablePartitionIterator(self.mbtable_partition, start_key=0, max_iterations=1000) as iterator:
            for i, (key, value) in enumerate(iterator):
                assert key == f"{i%100:0{4}}".encode()
                assert value == str({"col": f"value_{i%100}"}).encode()          
                cnt += 1
                assert iterator.current_file == f"test/data/part_{i//100}.mbt"
        assert cnt == 1000


if __name__ == '__main__':
    unittest.main()