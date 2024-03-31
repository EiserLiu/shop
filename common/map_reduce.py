def hashmap(List):
    hash_map = {}
    for i in List:
        if hash_map.get(i):
            hash_map[i] += 1
        else:
            hash_map[i] = 1
    return hash_map


if __name__ == '__main__':
    List = [1, 2, 3, 6, 3, 4, 5, 6]
    resout = hashmap(List)
    print(resout)
