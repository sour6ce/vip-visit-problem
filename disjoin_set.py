from typing import List, Set


class DisjoinSet:
    # If negative it means that is a parent node and the absolute value is the size, if positive the number stored is the parent
    __dj: List[int]

    def __init__(self, count: int):
        self.__dj = [-1]*count

    def get_parent(self, i: int):
        if self.__dj[i] < 0:
            return i
        else:
            p = self.get_parent(self.__dj[i])
            self.__dj[i] = p
            return p

    def get_setsize(self, i: int):
        return self.__dj[self.get_parent(i)]*-1

    def merge(self, a: int, b: int):
        # Merge the parents
        a = self.get_parent(a)
        b = self.get_parent(b)

        # They are already merged
        if a == b:
            return False

        if self.__dj[a] > self.__dj[b]:
            # Put in a the parent of the bigger dj set
            c = a
            a = b
            b = c

        # The total size of new set is the sum of both
        self.__dj[a] += self.__dj[b]
        self.__dj[b] = a  # The parent of b is now a

        return True

    def get_all_parents(self) -> List[int]:
        return [i for i, v in enumerate(self.__dj) if v < 0]
