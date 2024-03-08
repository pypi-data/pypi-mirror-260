import ctypes
import os

lib_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'lib', 'libsstable_internal.so'))
lib = ctypes.CDLL(lib_path)

lib.CreateSSTableBuilder.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.CreateSSTableBuilder.restype = ctypes.c_void_p

lib.SetKV.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
lib.SetKV.restype = None

lib.SetMetaData.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
lib.SetMetaData.restype = None

lib.BuildSSTable.argtypes = [ctypes.c_void_p]
lib.BuildSSTable.restype = None

class MbTableBuilder:
    def __init__(self, path: str, codec: str = 'kZlib'):
        """
        Initializes an instance of the class, setting up the underlying MbTable builder with the specified path and compression codec.

        The `codec` parameter specifies the compression method to be used for the MbTable. It must be a string that matches one of the predefined compression codec names. The available codecs are as follows:
        - 'kLzo': LZO compression.
        - 'kZlib': zlib compression.
        - 'kUnCompress': No compression.
        - 'kGzip': Gzip compression.
        - 'kSnappy': Snappy compression.
        - 'kUnknown': Represents an unknown or unsupported compression codec. It's recommended to use one of the supported codecs for compatibility.

        Args:
            path (str): The file system path where the MbTable will be created.
            codec (str, optional): The name of the compression codec to use. Defaults to 'kZlib'.

        Note:
            The path and codec arguments are encoded in UTF-8 before being passed to the underlying `CreateSSTableBuilder` function of the `lib` library.
        """
        self.builder = lib.CreateSSTableBuilder(path.encode('utf-8'), codec.encode('utf-8'))

    def set_kv(self, key, value):
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(value, str):
            value = value.encode('utf-8')
        lib.SetKV(self.builder, key, value)
            
    def set_metadata(self, key: str, value: str):
        lib.SetMetaData(self.builder, key.encode('utf-8'), value.encode('utf-8'))    
       
    def build(self):
        lib.BuildSSTable(self.builder)
        
if __name__ == '__main__':
    builder = MbTableBuilder('test/data/test.mbt')
    builder.set_kv('key1', '{"name": "Alice", "age": 25}')
    builder.set_kv('key2', 'value2')
    builder.set_metadata('meta1', 'value1')
    builder.set_metadata('meta2', 'value2')
    builder.build()

