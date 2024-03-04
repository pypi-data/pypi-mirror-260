import os
import ctypes
from sys import platform

try:
    if platform == "linux" or platform=="linux2":
        path = os.path.join(os.path.dirname(__file__))
        path += "/corex64/linux/Subdora.so"
        subdora_core = ctypes.CDLL(path)
    elif platform == "win32":
        path = os.path.join(os.path.dirname(__file__))
        path += "/corex64/win/Subdora.dll"
        subdora_core = ctypes.CDLL(path)


    mystique_encode_file_with_itr = subdora_core.subdoraEncodeFileWithItr
    mystique_encode_file_with_itr.argtypes = [ctypes.c_char_p,ctypes.c_size_t,ctypes.c_char_p]
    mystique_encode_file_with_itr.restype = None 

    def subdora_encode_file(input_file_path:str,iterations:int=-100):
        try:
            assert isinstance(input_file_path,str) or isinstance(iterations,int) ,f"ERROR: Type Mismatch input_file_path should be str and iteration should be int"
            output_file_path = input_file_path[:-3]+".myst"
            mystique_encode_file_with_itr(input_file_path.encode(),iterations,output_file_path.encode())
        except AssertionError as e:
            print(e)

    mystique_parse_file = subdora_core.subdoraParse
    mystique_parse_file.argtypes=[ctypes.c_char_p]
    mystique_parse_file.restype=ctypes.c_char_p

    def subdora_parse(mystique_file_path:str):
        try:
            assert isinstance(mystique_file_path,str) , f"ERROR: Type Mismatch expected string"
            program_to_be_executed = mystique_parse_file(mystique_file_path.encode())
            exec(program_to_be_executed.decode('utf-8'))
        except AssertionError as e:
            print(e)
    
except:
    print("error loading subdora core")


