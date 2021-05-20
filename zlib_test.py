# zlib_final

import os
import sys

def getFile(path):

    f = open(path, "rb")
    size = 100 #size
    offset = 256
    f.seek(offset)
    datastream = f.read(size)
    
    # for i in range(1,145):

    #     filename = "prg_" + i + "sy_" + i + "zlib_" + i
    #     fw = open(os.path.join(os.path.dirname(path), filename), "wb")
    #     fw.write(datastream)

    #     f.close()

    return datastream

# def makeFile():
    
# def findSignature():

def offset(data):

    prg_signature = b"\x50\x72\x47\x73\x49\x7A\x45\x3D"
    sy_signature = b"\x53\x59\x45\x4E\x43\x5A\x5A"
    zlib_signature = b"\x78\x9C"

    line_offset = 0
    offset_list = list()

    print(data)

    for d in data :

        if zlib_signature in data:

            tmp = d.find(zlib_signature)
            append_offset = line_offset + tmp
            offset_list.append(str(append_offset))

        # line_offset += len(d)

    print(offset_list)

    for i in range(len(offset_list)):

        if i == len(offset_list)-1:
            break

        start = int(offset_list[i])
        end = int(offset_list[i+1])
        a = data[start:end]
        print(a)




    # for d:
    #     start = 0
    #     end = 2
    #     offset_list[start:end]
    #     data[start:end]

    # for o in offset_list:
    #     hex_offset = hex(int(o))
    #     print(hex_offset)

    # for n in offset_list:
    #     print(hex(int(n)))


# with open('PrG'+1, 'wb') as f:
#     f.write(output)


def main():

    # file = getFile(r"C:\Users\user\Downloads\MainTask_VPASS.bin")
    offset(r"C:\Users\user\Downloads\MainTask_VPASS.bin")


if __name__ == '__main__':
    main()