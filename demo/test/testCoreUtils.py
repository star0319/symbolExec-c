from elftools.elf.elffile import ELFFile

from CFG.cfg import CFGBuilder
from CFG.graphUtil import GraphUtil
from capstoneUntil import Disassembly, DisassemblyFromBytes
import os

from textUtil import Colors


def is_elf_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read(4) == b'\x7fELF'

if __name__ == "__main__":

    # 指定Python目录路径
    directory = '/Users/star/code/py/symbol_excution/coreutils/'
    # directory = r'/Users/star/code/binary_analysis/c++/perf_test/'

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



            bytes=sec.data()
            binaries= DisassemblyFromBytes(bytes,baseAddr)
            cfgbuilder= CFGBuilder()
            cfg= cfgbuilder.build(binaries,baseAddr)
            #
            # for edges in cfg.outEdges.values():
            #     for edge in edges:
            #         print(f"{Colors.RED}{edge}{Colors.RESET}")
            #
            outPathDir = directory + "CFG_output/"
            if not os.path.exists(outPathDir):
                os.makedirs(outPathDir)

            outPath=outPathDir+item+".dot"
            # print(item)
            graphUtil=GraphUtil()
            graphUtil.generateBBGraph(cfg,outPath)

            # 关闭文件
            file.close()
            jmpCount+=cfgbuilder.jmpCounts
            counts+=cfgbuilder.counts
            #
            # if item=="md5sum" :
            #     break

    print("处理文件个数：" + str( fileCount))
    print("处理跳转指令个数：" + str( jmpCount))
    print("处理总指令个数：" + str( counts))