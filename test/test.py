list1 = 'qwertyuiopasdfghjklzxcvbnm'
n = 24



for i in range(1,int('1'*n,base=2)+1):
    list_str = []
    index_bin = str(bin(i)).lstrip('0b')
    if len(index_bin)< n:
        index_bin = (n-len(index_bin))*'0' + index_bin
    for i in range(len(index_bin)):
        if index_bin[i] == '1':
            list_str.append(list1[i])

    print(''.join(list_str))
