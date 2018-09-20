from bitarray import bitarray
# 3rd party
import mmh3


class BloomFilter(set):
    '''
    bloom过滤器
    '''
    def __init__(self, size, hash_count):
        '''
        :param size:  bloomfilter 二进制array的长度
        :param hash_count: hash的次数
        '''
        super(BloomFilter, self).__init__()
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.size = size
        self.hash_count = hash_count

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.bit_array)

    def add(self, item):
        '''
        添加对象
        :param item: 元素，要hash的对象
        :return self 链式调用
        '''
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1
        return self

    def __contains__(self, item):
        '''
        重写contains 判断对象是否重复
        有一定的误判，但是概率很小可以接受
        :param item:
        :return: ture 表示重复
                false表示不重读
        '''
        out = True
        # 只要存在不为1 ，就判断不再其中
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                out = False
                break
        return out


def main():
    bloom = BloomFilter(100, 10)
    animals = ['dog', 'cat', 'giraffe', 'fly', 'mosquito', 'horse', 'eagle',
               'bird', 'bison', 'boar', 'butterfly', 'ant', 'anaconda', 'bear',
               'chicken', 'dolphin', 'donkey', 'crow', 'crocodile']
    # 初始化bloomfilter
    for animal in animals:
        bloom.add(animal)

    # 对判断，True过滤
    #       False 加入过滤器
    other_animals = ['badger', 'cow', 'pig', 'sheep', 'bee', 'wolf', 'fox']
    for other_animal in other_animals:
        if other_animal in bloom:
            print('{} is in the bloom'.format(other_animal))
            bloom.add(other_animal)
        else:
            print('{} is not in the bloom filter as expected'.format(other_animal))


if __name__ == '__main__':
    main()
