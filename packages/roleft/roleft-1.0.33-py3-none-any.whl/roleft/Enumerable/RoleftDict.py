from typing import Generic, TypeVar
from roleft.Entities.RoleftKeyValue import KeyValue
from roleft.Enumerable.RoleftList import xList


TKey = TypeVar("TKey")
TValue = TypeVar("TValue")


class xDict(Generic[TKey, TValue]):
    def __init__(self) -> None:
        self.__kvs: xList[KeyValue[TKey, TValue]] = xList()

    def SureAdd(self, key: TKey, value: TValue):
        curr = self.__kvs.First(lambda x: x.key == key)
        if curr != None:
            self.__kvs.Remove(curr)

        self.__kvs.Add(KeyValue(key, value))
        return self

    def ContainsKey(self, key: TKey) -> bool:
        return self.__kvs.Exists(lambda x: x.key == key)

    def Keys(self):
        return self.__kvs.xSelect(lambda x: x.key)

    def Values(self):
        return self.__kvs.xSelect(lambda x: x.value)

    def KeyValues(self):
        return self.__kvs

    def ToList(self):
        return self.__kvs.ToList()

    def Clear(self):
        self.__kvs.Clear()
        return self

    def GetValue(self, key: TKey):
        first = self.__kvs.First(lambda x: x.key == key)
        if first != None:
            return first.value
        else:
            raise ValueError(f"不存在的key:{key}")

    def Remove(self, key: TKey):
        try:
            curr = self.GetValue(key)
            self.__kvs.Remove(curr)
        except ValueError:
            pass

        return self

    def Print(self):
        dic = {}
        for kv in self.__kvs.ToList():
            dic[kv.key] = kv.value

        print(dic)
