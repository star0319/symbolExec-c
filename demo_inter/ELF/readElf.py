# coding=utf-8
# 解析 elf 文件需要导入的依赖库
#   安装 pyelftools 库
from elftools.elf.elffile import ELFFile
# from elfwrapper.elf_wrapper import ElfAddrObj


def extract_func_info_in_order(elffile):
    text_section=elffile.get_section_by_name(".text")
    baseAddr=text_section.header['sh_addr']
    endAddr=baseAddr+ text_section.header['sh_size']
    # print( hex(   baseAddr+ text_section.header['sh_size'] ))
    funcs=[]
    symbol_tables = [s for s in elffile.iter_sections() if s['sh_type']=='SHT_SYMTAB']
    # i=0
    for section in symbol_tables:
        for symbol in section.iter_symbols():
            addr= symbol['st_value']
            # print(baseAddr)
            if symbol['st_info']['type']=='STT_FUNC' and addr!=0 and addr>=baseAddr and addr<endAddr:
                # if symbol['st_info']['type']=='STT_FUNC' and addr!=0 and (addr<0x1060 or addr>0x1254):
                #     i+=1
                funcs.append(symbol)
                # print(i)
                # print(f"函数名: {symbol.name}, 地址: {hex(symbol['st_value'])}, 大小: {symbol['st_size']}")

    funcs.sort(key= lambda o:o['st_value'])

    for i in range(0,len(funcs)):
        symbol=funcs[i]
        addr = symbol['st_value']
        print(f"函数名: {symbol.name}, 地址: {hex(symbol['st_value'])}, 大小: {symbol['st_size']}")
        if symbol['st_size']==0:
            symbol.entry['st_size']=funcs[i + 1]['st_value'] - addr
        # print(funcs[i + 1]['st_value'] - addr)
        # print(symbol['st_size'])
        # print(addr)
        # print(baseAddr)
        # print(f"函数名: {symbol.name}, 地址: {hex(symbol['st_value'])}, 大小: {symbol['st_size']}")

    return funcs

def main():
    # 要解析的动态库路径
    elf_path = r'/Users/star/code/binary_analysis/c++/perf_test/symex-x86'
    # elf_path="/Users/star/code/py/symbol_excution/coreutils/cat"
    # 打开 elf 文件
    file = open(elf_path, 'rb')
    # 创建 ELFFile 对象 , 该对象是核心对象
    elf_file = ELFFile(file)

    extract_func_info_in_order(elf_file)

    # # 打印 elf 文件头
    # print(elf_file.header)
    # # 打印 程序头入口 个数
    # print(elf_file.num_segments())
    # # 打印 节区头入口 个数
    # print(elf_file.num_sections())
    #
    #
    # # 遍历打印 程序头入口
    # for segment in elf_file.iter_segments():
    #     print(segment.header)
    #     print(segment.header['p_align'])
    #
    # # 遍历打印 节区头入口
    # for section in elf_file.iter_sections():
    #     print('name:', section.name)
    #     print('header', section.header)
    #
    #
    # sec= elf_file.get_section_by_name(".text")
    #
    # print(sec.data().hex())
    # print(sec.header)


    # 关闭文件
    file.close()
    pass


if __name__ == '__main__':
    main()

