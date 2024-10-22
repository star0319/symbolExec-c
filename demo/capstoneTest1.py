from capstone import *

def Disassembly(path,BaseAddr,FileOffset,ReadByte):
    with open(path,"rb") as fp:
        fp.seek(int(FileOffset))
        # opcode = fp.read(int(ReadByte))
        opcode = fp.read()

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    for item in md.disasm(opcode, 0):
          print("0x%x:\t%s\t%s" % (item.address, item.mnemonic, item.op_str))
        # addr = int(BaseAddr) + item.address
        # dic = {"Addr": str(addr) , "OpCode": item.mnemonic + " " + item.op_str}
        # print(dic)

if __name__ == "__main__":
    # 文件名 内存地址 开始位置 长度
    # Disassembly("d://Win32Project.exe",401000,0,1024)
    path="/Users/star/code/binary_analysis/c++/perf_test/symex-x86"
    # path="/Users/star/code/binary_analysis/c++/perf_test/symex"
    Disassembly(path, 0, 0, 0)
