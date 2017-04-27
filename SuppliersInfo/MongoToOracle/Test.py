"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/21
"""
import datetime
import time


def dec_str(func):
    def wrapper(self, str_list):
        special_characters = "!#$.=-〓*＊\"'<>《》,.\\，。\ue29c\ue29b\ue2f1\ue006★"
        modify_str_list = []
        for single_str in str_list:
            for special_character in special_characters:
                print(special_character)
                single_str = single_str.replace(special_character, "")

            modify_str = single_str.replace("None", "").strip()
            modify_str_list.append(modify_str)
        return func(self, modify_str_list)

    return wrapper
class A:
    @dec_str
    def func_a(self, lsit):
        print(lsit)

if __name__ == "__main__":
    a = A()
    a.func_a(["/!#$.=-〓*＊\"'<>《》,5.\\，None/!#$.=-〓*1＊\"'<>3《》,.\\，\ue29c。\ue29b  \ue2f1"])