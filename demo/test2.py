# test1.py
from capstone import *



# CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
# path = "/Users/star/code/binary_analysis/c++/perf_test/symex-x86"
path="/home/wsx/symexc/symex-x86"
with open(path, "rb") as fp:
    fp.seek(int(0x1060))
    # opcode = fp.read(int(ReadByte))
    CODE = fp.read()

md = Cs(CS_ARCH_X86, CS_MODE_64)
for i in md.disasm(CODE, 0x1060):
    print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
