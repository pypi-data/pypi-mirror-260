import numpy as np
import itertools
import inspect
from symengine import symbols as symengine_symbols

"""
SympyのSymbol関数にそのまま投げる関数
importをTYTANだけにするための申し訳ない方策
"""
def symbols(passed_txt):
    return symengine_symbols(passed_txt)

class TytanException(Exception):
    pass

"""
リストでまとめて定義する関数
"""
def symbols_list(shape, format_txt):
    #単一intの場合
    if type(shape) == int:
        shape = [shape]
    #print(shape)

    #次元チェック
    dim = len(shape)
    if dim != format_txt.count('{}'):
        raise TytanException("specify format option like format_txt=\'q{}_{}\' as dimension")
    
    #{}のセパレートチェック
    if '}{' in format_txt:
        raise TytanException("separate {} in format_txt like format_txt=\'q{}_{}\'")

    #次元が1～5でなければエラー
    if dim not in [1, 2, 3, 4, 5]:
        raise TytanException("Currently only dim<=5 is available. Ask tytan community.")

    #次元で分岐、面倒なのでとりあえずこれで5次元まで対応したこととする
    if dim == 1:
        q = []
        for i in range(shape[0]):
            q.append(symbols(format_txt.format(i)))
    elif dim == 2:
        q = []
        for i in range(shape[0]):
            tmp1 = []
            for j in range(shape[1]):
                tmp1.append(symbols(format_txt.format(i, j)))
            q.append(tmp1)
    elif dim == 3:
        q = []
        for i in range(shape[0]):
            tmp1 = []
            for j in range(shape[1]):
                tmp2 = []
                for k in range(shape[2]):
                    tmp2.append(symbols(format_txt.format(i, j, k)))
                tmp1.append(tmp2)
            q.append(tmp1)
    elif dim == 4:
        q = []
        for i in range(shape[0]):
            tmp1 = []
            for j in range(shape[1]):
                tmp2 = []
                for k in range(shape[2]):
                    tmp3 = []
                    for l in range(shape[3]):
                        tmp3.append(symbols(format_txt.format(i, j, k, l)))
                    tmp2.append(tmp3)
                tmp1.append(tmp2)
            q.append(tmp1)
    elif dim == 5:
        q = []
        for i in range(shape[0]):
            tmp1 = []
            for j in range(shape[1]):
                tmp2 = []
                for k in range(shape[2]):
                    tmp3 = []
                    for l in range(shape[3]):
                        tmp4 = []
                        for m in range(shape[4]):
                            tmp4.append(symbols(format_txt.format(i, j, k, l, m)))
                        tmp3.append(tmp4)
                    tmp2.append(tmp3)
                tmp1.append(tmp2)
            q.append(tmp1)

    return np.array(q)



"""
個別定義用のコマンドを返す関数
exec(command)して定義
"""
def symbols_define(shape, format_txt):
    #単一intの場合
    if type(shape) == int:
        shape = [shape]
    #print(shape)

    #次元チェック
    dim = len(shape)
    if dim != format_txt.count('{}'):
        raise TytanException("specify format option like format_txt=\'q{}_{}\' as dimension")
    
    #{}のセパレートチェック
    if '}{' in format_txt:
        raise TytanException("separate {} in format_txt like format_txt=\'q{}_{}\'")

    #次元が1～5でなければエラー
    if dim not in [1, 2, 3, 4, 5]:
        raise TytanException("Currently only dim<=5 is available. Ask tytan community.")

    #次元で分岐、面倒なのでとりあえずこれで5次元まで対応したこととする
    ret = ''
    command1 = f'{format_txt} = symbols(\'{format_txt}\')'
    if dim == 1:
        for i in range(shape[0]):
            command2 = eval('command1').format(i, i)
            ret += command2 + '\r\n'
    elif dim == 2:
        for i, j in itertools.product(range(shape[0]), range(shape[1])):
            command2 = eval('command1').format(i, j, i, j)
            ret += command2 + '\r\n'
    elif dim == 3:
        for i, j, k in itertools.product(range(shape[0]), range(shape[1]), range(shape[2])):
            command2 = eval('command1').format(i, j, k, i, j, k)
            ret += command2 + '\r\n'
    elif dim == 4:
        for i, j, k, l in itertools.product(range(shape[0]), range(shape[1]), range(shape[2]), range(shape[3])):
            command2 = eval('command1').format(i, j, k, l, i, j, k, l)
            ret += command2 + '\r\n'
    elif dim == 5:
        for i, j, k, l, m in itertools.product(range(shape[0]), range(shape[1]), range(shape[2]), range(shape[3]), range(shape[4])):
            command2 = eval('command1').format(i, j, k, l, m, i, j, k, l, m)
            ret += command2 + '\r\n'

    return ret[:-2]

    # #表示用
    # if dim == 1:
    #     first_command =eval('command1').format(0, 0)
    #     final_command = eval('command1').format(shape[0]-1, shape[0]-1)
    # elif dim == 2:
    #     first_command =eval('command1').format(0, 0, 0, 0)
    #     final_command = eval('command1').format(shape[0]-1, shape[1]-1, shape[0]-1, shape[1]-1)
    # elif dim == 3:
    #     first_command =eval('command1').format(0, 0, 0, 0, 0, 0)
    #     final_command = eval('command1').format(shape[0]-1, shape[1]-1, shape[2]-1, shape[0]-1, shape[1]-1, shape[2]-1)
    # elif dim == 4:
    #     first_command =eval('command1').format(0, 0, 0, 0, 0, 0, 0, 0)
    #     final_command = eval('command1').format(shape[0]-1, shape[1]-1, shape[2]-1, shape[3]-1, shape[0]-1, shape[1]-1, shape[2]-1, shape[3]-1)
    # elif dim == 5:
    #     first_command =eval('command1').format(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    #     final_command = eval('command1').format(shape[0]-1, shape[1]-1, shape[2]-1, shape[3]-1, shape[4]-1, shape[0]-1, shape[1]-1, shape[2]-1, shape[3]-1, shape[4]-1)
    # print(f'defined global : {first_command} to {final_command}')


def symbols_nbit(start, stop, format_txt, num=8):
    #次元チェック
    if 1 != format_txt.count('{}'):
        raise TytanException("specify format option like format_txt=\'q{}\' and should be one dimension.")
    
    #生成
    q = symbols_list(num, format_txt=format_txt)

    #式
    ret = 0
    for n in range(num):
        #係数を規格化してから量子ビットをかけたい
        ret += (start + (stop - start)) * 2**(num - n - 1) / 2**num * q[n]

    return ret
