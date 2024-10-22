from capstone import *

from CFG.cfg import CFGBuilder


def Disassembly(path,BaseAddr,FileOffset,ReadByte):
    with open(path,"rb") as fp:
        fp.seek(int(FileOffset))
        # opcode = fp.read(int(ReadByte))
        opcode = fp.read()

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    binaries=[]
    for item in md.disasm(opcode, 0):
        print("0x%x:\t%s\t%s" % (int(BaseAddr)+item.address, item.mnemonic, item.op_str))
        # addr = int(BaseAddr) + item.address
        # dic = {"Addr": str(addr) , "OpCode": item.mnemonic + " " + item.op_str}
        # print(dic)
        binaries.append(item)


    return binaries


def DisassemblyFromBytes(opcode,BaseAddr):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    binaries=[]
    for item in md.disasm(opcode, 0):
        # print("0x%x:\t%s\t%s" % (int(BaseAddr)+item.address, item.mnemonic, item.op_str))
        # addr = int(BaseAddr) + item.address
        # dic = {"Addr": str(addr) , "OpCode": item.mnemonic + " " + item.op_str}
        # print(dic)
        binaries.append(item)


    return binaries

if __name__ == "__main__":
    # 文件名 内存地址 开始位置 长度
    # Disassembly("d://Win32Project.exe",401000,0,1024)
    path="/Users/star/code/binary_analysis/c++/perf_test/symex-x86"
    # path="/Users/star/code/py/symbol_excution/coreutils/cat"
    # path="/Users/star/code/binary_analysis/c++/perf_test/symex"
    # binaries= Disassembly(path, 0x1149, 0x1149, 0)

    baseAddr=0x1060
    # binaries= Disassembly(path, 0x2790, 0x2790, 0)
    binaries= Disassembly(path, baseAddr, baseAddr, 0)

    cfgbuilder= CFGBuilder()
    cfg= cfgbuilder.build(binaries,baseAddr)

    # print(cfg.inEdges)
    # generateBBGraph(cfg)

    # cfgEdges = cfg.inEdges
    # for edgeItem in cfgEdges.values():
    #    print(edgeItem.get_src(),edgeItem.get_dst())


