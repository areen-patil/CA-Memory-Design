import math
import matplotlib.pyplot as plt

class Cache:
    def __init__(self, size,number_ways):  # size is in Kilobytes
        self.setAssociativeType = number_ways
        # following values are in bytes
        self.cacheSize = size * 1024
        self.blockSize = 4
        self.addressLength = 4
        self.cacheLines = int(self.cacheSize/(self.blockSize * self.setAssociativeType))
        # following values are in bits
        self.indexBits = int(math.log2(self.cacheLines))
        self.bitOffset = int(math.log2(self.blockSize))
        self.tagBits = self.addressLength*8 - self.indexBits - self.bitOffset


class Ways:
    def __init__(self):
        self.way_number=0
        self.validBit = 0
        self.tag = ""


class Set:
    def __init__(self, index,number_of_ways):
        self.index = index
        self.lru_register=[]
        for i in range(number_of_ways+1):
            var1=Ways()
            self.lru_register.append(var1)
            # print(type(self.lru_register[i].tag))
            self.lru_register[i].way_number=i+1
        # self.way1 = Ways()
        # self.way2 = Ways()
        # self.way3 = Ways()
        # self.way4 = Ways()
        # self.lru_register=[]
        # for i in range(number_of_ways):
            # self.lru_register.append(self.l[i])
        # self.lru_register = [self.way1, self.way2, self.way3, self.way4]

    # returns the least recently used way
    def lru(self):
        return self.lru_register[0]

    # returns 0 if tag matches otherwise -1
    def tag_match(self, tag_str):
        # print("printing the value of len of lru_register")
        # print(len(self.lru_register))
        # print("\n")
        for i in range(len(self.lru_register)):
            # print("pritning the value of i: ")
            # print("\n")
            # print(i)
            # print("\n")
            # print("printing of i done")
            # print(self.lru_register[i].tag)
            # print(type(self.lru_register[i].tag))
            if(self.lru_register[i].tag==tag_str and self.lru_register[i].validBit==1):
                return i+1
            
        return -1

        # if self.way1.validBit == 1 and self.way1.tag == tag:
        #     return 1
        # elif self.way2.validBit == 1 and self.way2.tag == tag:
        #     return 2
        # elif self.way3.validBit == 1 and self.way3.tag == tag:
        #     return 3
        # elif self.way4.validBit == 1 and self.way4.tag == tag:
        #     return 4
        # else:
        #     return -1

    def change_lru(self, way_number):
        if(way_number==-1):
            self.lru_register = self.lru_register[1:] + self.lru_register[:1]
        for i in range(len(self.lru_register)):
            if(self.lru_register[i].way_number==way_number):
                var=self.lru_register.remove(self.lru_register[i])
                self.lru_register.append(var)
                return
        return
        if way_number == -1:          # perform a left shift
            self.lru_register = self.lru_register[1:] + self.lru_register[:1]
        # shift the used way to the mru
        # elif way_number == 1:
        #     self.lru_register.remove(self.way1)
        #     self.lru_register.append(self.way1)
        # elif way_number == 2:
        #     self.lru_register.remove(self.way2)
        #     self.lru_register.append(self.way2)
        # elif way_number == 3:
        #     self.lru_register.remove(self.way3)
        #     self.lru_register.append(self.way3)
        # elif way_number == 4:
        #     self.lru_register.remove(self.way4)
        #     self.lru_register.append(self.way4)


def hex_to_bin(num, num_bits=32):     # converts a number to its binary representation
    return bin(int(num, 16))[2:].zfill(num_bits)


def instruction_file_read():
    file = open("gzip.trace", "r")
    addresses = file.readlines()
    file.close()
    return addresses


def cache_check(address):
    global number_of_hits
    global number_of_misses
    tag = address[:cache.tagBits]
    index = address[cache.tagBits:cache.bitOffset*(-1)]
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


list_of_ways=[1,2,4,8,16,32,64]
miss=[]
hits=[]
missrate=[]
hitrate=[]
for i in list_of_ways:
    cache = Cache(1024,i)  # size is in Kilobytes
    number_of_hits = 0
    number_of_misses = 0
    instruction_file = instruction_file_read()
    file_size = len(instruction_file)

    memory = []
    for memory_line in range(pow(2, cache.indexBits)):
        memory.append(Set(memory_line,i))

    for line in range(file_size):
        cache_check(hex_to_bin(instruction_file[line][4:12], 32))  # give the 32-bit address to the cache
        print(f' Percent Complete: {(line/file_size)*100}%', end='\r')

    print("Number of hits : ", number_of_hits)
    hits.append(number_of_hits)
    print("Number of misses : ", number_of_misses)
    miss.append(number_of_misses)
    print("Hits rate : ", (number_of_misses*100)/(number_of_misses+number_of_hits))
    hitrate.append((number_of_hits*100)/(number_of_misses+number_of_hits))
    # print("Miss/Hits : ", (number_of_hits/number_of_misses))
    # missrate.append((number_of_hits/number_of_misses))
plt.plot(list_of_ways,hitrate)
plt.title("This is the graph of hitrate vs associativity")
plt.xlabel("associativity")
plt.ylabel("hitrate")
x=list_of_ways  
plt.plot(x,hitrate)