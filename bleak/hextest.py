addresses=  ["140202FE75BC", 
            "140202FE75BC", 
            "140202CB134A", 
            "140202BC1D3A", 
            "140202B7AC51", 
            "140202B49C32", 
            "140202BD0D1B", 
            "140202BD0D1B", 
            "140202897BCC", 
            "140202897BCC", 
            "140200FF03FF", 
            "140202007B6D", 
            "1402020F8A82", 
            "140202897BCC"]
for x in addresses:
    # data = hex(int(x, 16))
    data = bytearray.fromhex(bytes(x, 'utf-8').decode('utf-8'))
    # print(x)
    # print(hex(x))
    # data = bytearray(data, 'utf-8')
    print(data)
