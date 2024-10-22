from elftools.elf.elffile import ELFFile

from CFG.cfg import CFGBuilder
from CFG.graphUtil import GraphUtil
from ELF.readElf import extract_func_info_in_order
from SymbolExcute.symbolExcute import SymbolExcute
from capstoneUntil import Disassembly, DisassemblyFromBytes
import os

from textUtil import Colors


def is_elf_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read(4) == b'\x7fELF'


if __name__ == "__main__":

    # 指定Python目录路径
    # directory = '/Users/star/code/py/symbol_excution/coreutils/'
    directory = r'/Users/star/code/binary_analysis/c++/perf_test/'

    # 列出该目录下的所有文件名（不包括子目录）
    file_names = [f for f in os.listdir(directory) if not os.path.isdir(os.path.join(directory, f))]
    # file_names = ["md5sum"]
    # print(file_names)

    fileCount=0
    jmpCount=0
    counts=0
    for item in file_names:
        if item.find(".")!=-1:
            print(item)
        #针对二进制文件
        else:
            print(f"{Colors.RED}"+ "file"+item+f"{Colors.RESET}")
            elf_path=directory+item
            # print(elf_path)
            file = open(elf_path, 'rb')
            # 创建 ELFFile 对象 , 该对象是核心对象
            #判断是不是elf文件
            if not is_elf_file(elf_path):continue
            fileCount+=1
            elf_file = ELFFile(file)

            # 打印 elf 文件头
            # print(elf_file.header)
            # 打印 程序头入口 个数
            # print(elf_file.num_segments())
            # 打印 节区头入口 个数
            # print(elf_file.num_sections())

            sec = elf_file.get_section_by_name(".text")
            # print(sec.header['sh_addr'])
            baseAddr =sec.header['sh_addr']
            bytes = sec.data()

            funcs= extract_func_info_in_order(elf_file)

            for fun_symbol in funcs:
                fun_addr = fun_symbol['st_value']
                offsef=fun_addr-baseAddr
                # print(baseAddr)
                print(f"函数名: {fun_symbol.name}, 地址: {hex(fun_symbol['st_value'])}, 大小: {fun_symbol['st_size']}")
                if fun_symbol['st_size']==0: continue
                funBytes=bytes[offsef:offsef+fun_symbol['st_size']]

                if fun_symbol.name!="_Z3fooii": continue
                # if fun_symbol.name!="_Z11rangeSumBSTP8TreeNodeii": continue

                binaries= DisassemblyFromBytes(funBytes,fun_addr)

                cfgbuilder= CFGBuilder()

                cfg= cfgbuilder.build(binaries,fun_addr,fun_symbol['st_size'])

                #
                # for edges in cfg.outEdges.values():
                #     for edge in edges:
                #         print(f"{Colors.RED}{edge}{Colors.RESET}")
                #

                # #输出cfg图
                # outPathDir = directory + "CFG_output/"+item+"/"
                # if not os.path.exists(outPathDir):
                #     os.makedirs(outPathDir)
                #
                # outPath=outPathDir+fun_symbol.name+".dot"
                # # print(item)
                # graphUtil=GraphUtil()
                # graphUtil.generateBBGraph(cfg,outPath)

                symbolExcute=SymbolExcute(cfg)
                symbolExcute.excute()

                jmpCount += cfgbuilder.jmpCounts
                counts += cfgbuilder.counts


            # 关闭文件
            file.close()


            #
            # if item=="md5sum" :
            #     break

    print("处理文件个数：" + str( fileCount))
    print("处理跳转指令个数：" + str( jmpCount))
    print("处理总指令个数：" + str( counts))