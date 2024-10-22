from elftools.elf.elffile import ELFFile

def extract_func_info(file_path):
    with open(file_path, 'rb') as file:
        elffile = ELFFile(file)
        symbol_tables = [s for s in elffile.iter_sections() if s['sh_type']=='SHT_SYMTAB']
        i=0
        for section in symbol_tables:
            for symbol in section.iter_symbols():
                addr= symbol['st_value']
                if symbol['st_info']['type']=='STT_FUNC' and addr!=0 and addr>=0x1060 and addr<=0x1254:
                # if symbol['st_info']['type']=='STT_FUNC' and addr!=0 and (addr<0x1060 or addr>0x1254):
                    i+=1
                    print(i)
                    # for s in symbol.entry:
                    #     print(s)
                    # print(symbol.entry
                    print(f"函数名: {symbol.name}, 地址: {hex(symbol['st_value'])}, 大小: {symbol['st_size']}")


def extract_func_info_in_order(file_path):
    with open(file_path, 'rb') as file:
        elffile = ELFFile(file)
        symbol_tables = [s for s in elffile.iter_sections() if s['sh_type']=='SHT_SYMTAB']
        i=0
        for section in symbol_tables:
            for symbol in section.iter_symbols():
                addr= symbol['st_value']
                if symbol['st_info']['type']=='STT_FUNC' and addr!=0 and addr>=0x1060 and addr<=0x1254:
                # if symbol['st_info']['type']=='STT_FUNC' and addr!=0 and (addr<0x1060 or addr>0x1254):
                    i+=1
                    print(i)
                    # for s in symbol.entry:
                    #     print(s)
                    # print(symbol.entry
                    print(f"函数名: {symbol.name}, 地址: {hex(symbol['st_value'])}, 大小: {symbol['st_size']}")

# 使用你的elf文件路径替换'your_file.elf'
path="/Users/star/code/binary_analysis/c++/perf_test/symex-x86"
extract_func_info(path)
