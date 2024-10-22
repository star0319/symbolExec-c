import cmd
import os
def is_elf_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read(4) == b'\x7fELF'

if __name__ == "__main__":

    # directory = '/Users/star/code/py/symbol_excution/coreutils/'
    directory = r'/Users/star/code/binary_analysis/c++/perf_test/'
    file_names = [f for f in os.listdir(directory) if not os.path.isdir(os.path.join(directory, f))]
    # os.system(f"cd {directory}")
    # os.system(f"pwd")

    for item in file_names:
        if item.find(".") != -1:
            # print(item)
            continue
        # 针对二进制文件
        else:
            # print(f"{Colors.RED}" + "file" + item + f"{Colors.RESET}")
            elf_path = directory + item
            # print(elf_path)
            # 创建 ELFFile 对象 , 该对象是核心对象
            # 判断是不是elf文件
            if not is_elf_file(elf_path): continue
            os.system(f"cd {directory}; objdump {item} --disassemble-all >> ./Dump/{item}Dump.txt")