"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/21
"""
import datetime
import time


def dec_str(func):
    def wrapper(self, str_list):
        modify_str_list = []
        for single_str in str_list:
            modify_str = single_str.strip("\/!#$.=-").replace("None", "")
            modify_str_list.append(modify_str)
        return func(self, modify_str_list)

    return wrapper
class A:
    @dec_str
    def func_a(self, lsit):
        print(lsit)

if __name__ == "__main__":
    a = A()
    a.func_a(["a/", "b\\1", "c$$", "d.=2", "#.e!"])