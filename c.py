import math
import matplotlib.pylot as plt

class Cache:
    def __init__(self, blocksize):  # size is in Kilobytes
        self.setAssociativeType = 4
        # following values are in bytes
        self.cacheSize = 1024 * 1024
        self.blockSize = blocksize
        self.addressLength = 4
        self.cacheLines = int(self.cacheSize/(self.blockSize * self.setAssociativeType))
        # following values are in bits
        self.indexBits = int(math.log2(self.cacheLines))
        self.bitOffset = int(math.log2(self.blockSize))
        self.tagBits = self.addressLength*8 - self.indexBits - self.bitOffset


class Ways:
    def __init__(self):
        self.validBit = 0
        self.tag = ""


class Set:
    def __init__(self, index):
        self.index = index
        self.way1 = Ways()
        self.way2 = Ways()
        self.way3 = Ways()
        self.way4 = Ways()
        self.lru_register = [self.way1, self.way2, self.way3, self.way4]

    # returns the least recently used way
    def lru(self):
        return self.lru_register[0]

    # returns 0 if tag matches otherwise -1
    def tag_match(self, tag):
        if self.way1.validBit == 1 and self.way1.tag == tag:
            return 1
        elif self.way2.validBit == 1 and self.way2.tag == tag:
            return 2
        elif self.way3.validBit == 1 and self.way3.tag == tag:
            return 3
        elif self.way4.validBit == 1 and self.way4.tag == tag:
            return 4
        else:
            return -1

    def change_lru(self, way_number):
        if way_number == -1:          # perform a left shift
            self.lru_register = self.lru_register[1:] + self.lru_register[:1]

        # shift the used way to the mru
        elif way_number == 1:
            self.lru_register.remove(self.way1)
            self.lru_register.append(self.way1)
        elif way_number == 2:
            self.lru_register.remove(self.way2)
            self.lru_register.append(self.way2)
        elif way_number == 3:
            self.lru_register.remove(self.way3)
            self.lru_register.append(self.way3)
        elif way_number == 4:
            self.lru_register.remove(self.way4)
            self.lru_register.append(self.way4)


def hex_to_bin(num, num_bits=32):     # converts a number to its binary representation
    return bin(int(num, 16))[2:].zfill(num_bits)


def instruction_file_read(file_name):
    file = open(file_name, "r")
    addresses = file.readlines()
    file.close()
    return addresses


def cache_check(address, cache):
    global number_of_hits
    global number_of_misses
    tag = address[:cache.tagBits]
    index = address[cache.tagBits:cache.bitOffset*(-1)]
    if index == "":
        index = "0"
    tag_match_with_way_number = memory[int(index, 2)].tag_match(tag)
    if tag_match_with_way_number > 0:
        number_of_hits += 1
        memory[int(index, 2)].change_lru(tag_match_with_way_number)
    else:
        lru_way = memory[int(index, 2)].lru()
        lru_way.validBit = 1
        lru_way.tag = tag
        memory[int(index, 2)].change_lru(-1)
        number_of_misses += 1

cache_size=[]
cache_list = []
block_size = 1  # size is in Kilobytes
while block_size <= 128:
    cache_list.append(Cache(block_size))
    block_size = block_size*2
k=1
while(k<=128):
    cache_size.append(k)
    k=k*2

file_names=[]
final_yaxis=[]
for j in file_names:
    instruction_file = instruction_file_read(file_names[j])
    file_size = len(instruction_file)
    temp=[]
    for test in range(6):
        number_of_hits = 0
        number_of_misses = 0
        memory = []
        for memory_line in range(pow(2, cache_list[test].indexBits)):
            memory.append(Set(memory_line))

        for line in range(file_size):
            cache_check(hex_to_bin(instruction_file[line][4:12], 32), cache_list[test])  # give the 32-bit address to the cache
            print(f'Percent Complete: {(line/file_size)*100}%', end='\r')

        print(f"For cache size {cache_list[test].cacheSize/1024}")
        print(f"For Block size {cache_list[test].blockSize}")
        print("Number of hits : ", number_of_hits)
        print("Number of misses : ", number_of_misses)
        temp.append((number_of_misses*100)/(number_of_misses+number_of_hits))
        print("Miss rate : ", (number_of_misses*100)/(number_of_misses+number_of_hits))
        print("Miss/Hits : ", (number_of_hits/number_of_misses))
        print("")
    final_yaxis.append(temp)
plt.plot(cache_size,final_yaxis[0],color="r",marker="o")
plt.plot(cache_size,final_yaxis[1],color="b",marker="o")
plt.plot(cache_size,final_yaxis[2],color="y",marker="o")
plt.plot(cache_size,final_yaxis[3],color="c",marker="o")
plt.plot(cache_size,final_yaxis[4],color="m",marker="o")
for i in range(len(final_yaxis)):
    for j in range(len(cache_size)):
        plt.annotate(f'{final_yaxis[i][j]:.2f}', 
                     (cache_size[j], final_yaxis[i][j]), 
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center')
# plt.plot(cache_size,final_yaxis[0],color="r",marker="o")
plt.xlabel("cache_size")
plt.ylabel("miss_rate")
plt.title("missrate vs cache_size")
plt.show()