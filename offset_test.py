# zlib_final

import os
import sys
import zlib

from numpy import datetime_as_string

def getFile(path):

    f = open(path, "rb")
    datastream = f.read()

    # for i in range(1,145):
    #     filename = "prg_" + i + "sy_" + i + "zlib_" + i
    #     fw = open(os.path.join(os.path.dirname(path), filename), "wb")
    #     fw.write(datastream)
    f.close()
    return datastream
    

def processFile(datastream):

    prg_signature = b"\x50\x72\x47\x73\x49\x7A\x45\x3D"
    sy_signature = b"\x53\x59\x45\x4E\x43\x5A\x5A"
    zlib_signature = b"\x78\x9C"

    prg_offset_list = list()
    sy_offset_list = list()
    zlib_offset_list = list()

    # find prg_signature
    tmp_offset = datastream.find(prg_signature)
    prg_offset_list.append(tmp_offset)
    while tmp_offset != -1:
        tmp_offset = datastream.find(prg_signature, tmp_offset+1)
        prg_offset_list.append(tmp_offset)
    del prg_offset_list[-1]


    # find sy_signature
    for i in range(len(prg_offset_list)):
        tmp_offset = 0
        t_offset =0
        if i != len(prg_offset_list)-1:
            tmp_sy_offset_list = list()
            while tmp_offset != -1:
                tmp_offset = datastream.find(sy_signature, prg_offset_list[i]+t_offset, prg_offset_list[i+1])
                tmp_sy_offset_list.append(tmp_offset)
                t_offset = tmp_offset-prg_offset_list[i]+1
            del tmp_sy_offset_list[-1]
            sy_offset_list.append(tmp_sy_offset_list)
        else:
            tmp_sy_offset_list = list()
            while tmp_offset != -1:
                tmp_offset = datastream.find(sy_signature, prg_offset_list[i]+t_offset)
                tmp_sy_offset_list.append(tmp_offset)
                t_offset = tmp_offset-prg_offset_list[i]+1
            del tmp_sy_offset_list[-1]
            sy_offset_list.append(tmp_sy_offset_list)


    # find zlib_signature
    for j in range(len(sy_offset_list)):
        tmp_tmp_zlib_offset_list = list()
        sy_ofl = sy_offset_list[j]
        for i in range(len(sy_ofl)):
            tmp_offset = 0
            t_offset=0
            if i != len(sy_ofl)-1:
                tmp_zlib_offset_list = list()
                while tmp_offset != -1:
                    tmp_offset = datastream.find(zlib_signature, sy_ofl[i]+t_offset, sy_ofl[i+1])
                    tmp_zlib_offset_list.append(tmp_offset)
                    t_offset = tmp_offset-sy_ofl[i]+1
                del tmp_zlib_offset_list[-1]
                tmp_tmp_zlib_offset_list.append(tmp_zlib_offset_list)
            else:
                tmp_zlib_offset_list = list()
                while tmp_offset != -1:
                    if j != len(sy_offset_list)-1:
                        tmp_offset = datastream.find(zlib_signature, sy_ofl[i]+t_offset, sy_offset_list[j+1][0])
                    else:
                        tmp_offset = datastream.find(zlib_signature, sy_ofl[i]+t_offset)
                    tmp_zlib_offset_list.append(tmp_offset)
                    t_offset = tmp_offset-sy_ofl[i]+1
                del tmp_zlib_offset_list[-1]
                tmp_tmp_zlib_offset_list.append(tmp_zlib_offset_list)
        zlib_offset_list.append(tmp_tmp_zlib_offset_list)
    return zlib_offset_list


def findSignature(datastream, signature, offset) :
    tmp_offset = datastream.find(signature, offset)
    return tmp_offset


def writeFile(dirpath, datastream, zz):
    path = dirpath + os.path.sep + "result"
    #os.mkdir
    for i in range(len(zz)):
        for j in range(len(zz[i])):
            name = "prg" + str(i+1)+"_sy" + str(j+1) +".zlib"
            filename = os.path.join(path,name)
            f = open(filename, 'wb')
            if j != len(zz[i])-1:
                data = datastream[zz[i][j][0]:zz[i][j+1][0]-8]
            else:
                if i != len(zz)-1:
                    data = datastream[zz[i][j][0]:zz[i+1][0][0]-16]
                else:
                    data = datastream[zz[i][j][0]:]
            f.write(data)
            f.close
            '''
            for k in range(len(zz[i][j])):
                
                name = "prg" + str(i+1)+"_sy" + str(j+1) + "_zlib" + str(k+1) +".zlib"
                filename = os.path.join(path,name)
                f = open(filename, 'wb')
                if k != len(zz[i][j])-1:
                    data = datastream[zz[i][j][k]:zz[i][j][k+1]]
                else:
                    if j != len(zz[i])-1:
                        data = datastream[zz[i][j][k]:zz[i][j+1][0]-8]
                    else:
                        if i != len(zz)-1:
                            data = datastream[zz[i][j][k]:zz[i+1][0][0]-16]
                        else:
                            data = datastream[zz[i][j][k]:]
                f.write(data)
                f.close
            '''
    return path

def decompressFile(input, dirpath, mode):
    print(mode)
    in_path = dirpath + os.path.sep + "result"
    out_path = dirpath + os.path.sep + "d_result"
    #os.mkdir()
    file_list = os.listdir(in_path)
    for filename in file_list:
        in_filename = os.path.join(in_path,filename)
        input_file = open(in_filename, 'rb')
        try:
            obj_1 = input_file.read()
            obj_m = zlib.decompressobj()
            obj_2 = obj_m.decompress(obj_1)

            o_filename = "de_"+ filename.split(".")[0]
            out_filename = os.path.join(out_path,o_filename)
            output_file = open(out_filename, 'wb')
            output_file.write(obj_2)
            output_file.close()
        except:
            print("Error : ",filename)
            continue


if __name__ == '__main__':
    target = r"D:\Users\user\Desktop\해경\updateSS_VPASS\MainTask_VPASS.bin"
    dirpath = os.path.dirname(target)
    datastream = getFile(target)
    zlib_offset = processFile(datastream)
    input_path = writeFile(dirpath, datastream, zlib_offset)
    mode = 1
    decompressFile(input_path, dirpath, mode)

