from enum import Enum

from textUtil import Colors


class BinaryCFG():
    binaries = []
    entry= None
    exit= None
    # nodes=set()
    nodes=[]
    inEdges={}
    outEdges={}

    def  __init__(self, binaries):
        self.binaries = binaries

    def __init__(self, binaries,baseAddr,endAddr):
        self.binaries = []
        self.entry = None
        self.exit = None
        self. nodes = []
        self. inEdges = {}
        self.outEdges = {}
        self.binaries = binaries
        self.baseAddr=baseAddr
        self.endAddr=endAddr


    def set_entry(self, entry):
        self.entry = entry
        # self.nodes.add(entry)
        self.nodes.append(entry)
    def set_exit(self, exit):
        self.exit = exit
        # self.nodes.add(exit)
        # self.nodes.append(exit)
    def get_entry(self):
        return self.entry

    def get_exit(self):
        return self.exit

    def isEntry(self, node):
        return self.entry == node

    def isExit(self, node):
        return self.exit == node

    def addNode(self, node):
        # self.nodes.add(node)
        self.nodes.append(node)
    def addEdge(self, edge):
        # if edge.get_src()
        # print(f"{Colors.RED}{edge}{Colors.RESET}")
        self.inEdges.setdefault(edge.get_dst(), set())
        # if self.inEdges[edge.get_dst()] is  None:
        #     self.inEdges[edge.get_dst()]=set()
        self.inEdges[edge.get_dst()].add(edge)
        # if self.outEdges[edge.get_src()] is  None:
        #     self.outEdges[edge.get_src()]=set()
        self.outEdges.setdefault(edge.get_src(), set())
        self.outEdges[edge.get_src()].add(edge)
        # ss=self.outEdges[edge.get_src()]
        # for s in ss:
        #     print(f"{Colors.RED}{s}{Colors.RESET}")

    def getInedgeOf(self, node):
        if self.inEdges.__contains__(node):
            return self.inEdges[node]
        else:
            return None

    def getOutedgeOf(self, node):
        if self.outEdges.__contains__(node):
            return self.outEdges[node]
        else:
            return None
    def findInsOfAddr(self, addr):
        # print(hex(addr))
        for binary in self.binaries:
            if binary.address == addr:
                # print(binary)
                return binary
            # elif binary.address==( addr+self.baseAddr& 0x0FFFFFFFFFFFFFFF):
            #     return binary

        print(hex(addr)+"  not found  INS")
        print(hex(addr + self.baseAddr & 0x0FFFFFFFFFFFFFFF) +" not found INS")
        return None
    # def get_cfg(self):



class Edge():
    src = None
    dst = None
    kind= None


    def __init__(self, src, dst,kind=None):
        self.src = src
        self.dst = dst
        self.kind=kind

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst

    def __str__(self):
        return "Edge: " +"[" + str( self.kind) + "]: " + str(self.src) + " -> " + str(self.dst)

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst

    def __hash__(self):
        return hash((self.src, self.dst))

    class Kind(Enum):
        Entry = 0,
        GoTo = 1,
        je=2,
        Through = 3,
        Exit=4


class NOP():

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "Node NOP: " + hex(self.index)

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)



class CFGBuilder():
    # 语句总个数
    counts = 0
    # 处理的跳转语句个数
    jmpCounts = 0
    # def __init__(self, path):
    #     self.path = path

    def build(self,binaries,baseAddr,endAddr):
        binaryCFG = BinaryCFG(binaries,baseAddr,endAddr)
        entry= NOP(len(binaries))
        binaryCFG.set_entry(entry)

        exit = NOP(len(binaries) + 1)
        binaryCFG.set_exit(exit)
        self.buildEdge(binaryCFG)
        binaryCFG.nodes.append(exit)
        return binaryCFG



    def buildEdge(self,binaryCFG):
        binaries = binaryCFG.binaries
        binaryCFG.addEdge(
            Edge(binaryCFG.get_entry(), binaries[0], Edge.Kind.Entry)
        )
        # baseAddr=0x1149
        baseAddr=binaryCFG.baseAddr
        endAddr=binaryCFG.endAddr
        for i in range(0, len(binaries)):
            curr=binaries[i]
            binaryCFG.addNode(curr)
            if(curr.mnemonic=="je" or curr.mnemonic=="jne"or curr.mnemonic=="jz"or curr.mnemonic=="jnz"
            or curr.mnemonic=="js"or curr.mnemonic=="jns"or curr.mnemonic=="jc"or curr.mnemonic=="jnc"
            or curr.mnemonic=="jo"or curr.mnemonic=="jno"or curr.mnemonic=="ja"or curr.mnemonic=="jna"
            or curr.mnemonic=="jae"or curr.mnemonic=="jnae"or curr.mnemonic=="jg"or curr.mnemonic=="jng"
            or curr.mnemonic=="jge"or curr.mnemonic=="jnge"or curr.mnemonic=="jb"or curr.mnemonic=="jnb"
            or curr.mnemonic=="jbe"or curr.mnemonic=="jnbe"or curr.mnemonic=="jl"or curr.mnemonic=="jnl"
            or curr.mnemonic=="jle"or curr.mnemonic=="jnle"or curr.mnemonic=="jp"or curr.mnemonic=="jnp"
            or curr.mnemonic=="jpe"or curr.mnemonic=="jpo" ):
                if i + 1 < len(binaries):
                    binaryCFG.addEdge(
                      Edge(curr, binaries[i+1], Edge.Kind.je)
                    )

                    # if curr.op_str=="rax" :continue
                    if ((int(curr.op_str, 16) + baseAddr) & 0x0FFFFFFFFFFFFFFF)<baseAddr:continue
                     # print("the command is   0x%x:\t%s\t%s" % (int(baseAddr)+curr.address, curr.mnemonic, curr.op_str))
                    # print("the command is   0x%x:\t%s\t0x%x" % (int(baseAddr)+curr.address, curr.mnemonic,  int(curr.op_str, 16) +int(baseAddr)))
                    if int( curr.op_str,16) >= 0 and int( curr.op_str,16)<= endAddr:
                        target = binaryCFG.findInsOfAddr(int( curr.op_str,16))
                        # target = binaryCFG.findInsOfAddr(baseAddr+ int( curr.op_str,16))
                        binaryCFG.addEdge(
                           #基础地址
                          Edge(curr, target, Edge.Kind.je)
                        )
                    self.jmpCounts+=1


            elif curr.mnemonic=="jmp":
                if i + 1 < len(binaries):
                    if (curr.op_str=="rax" or curr.op_str=="qword ptr [rcx]" or curr.op_str.find("qword")!=-1
                            or curr.op_str=="rbx" or curr.op_str=="rcx"or curr.op_str=="rdx") :continue
                    # print(curr)
                    if ((int(curr.op_str, 16) + baseAddr) & 0x0FFFFFFFFFFFFFFF)<baseAddr:continue
                    # print (hex ((int(curr.op_str, 16) + baseAddr) & 0x0FFFFFFFFFFFFFFF))
                    # print(hex(int(curr.op_str, 16) + baseAddr) )

                    # print("the command is   0x%x:\t%s\t%s" % (int(baseAddr)+curr.address, curr.mnemonic, curr.op_str))
                    # print("the command is   0x%x:\t%s\t0x%x" % (int(baseAddr)+curr.address, curr.mnemonic,  int(curr.op_str, 16) +int(baseAddr)))
                    if int( curr.op_str,16) >= 0 and int( curr.op_str,16)<= endAddr:

                        target = binaryCFG.findInsOfAddr(int( curr.op_str,16))
                        # target = binaryCFG.findInsOfAddr(baseAddr+ int( curr.op_str,16))
                        binaryCFG.addEdge(
                           #基础地址
                          Edge(curr, target, Edge.Kind.je)
                        )
                    self.jmpCounts += 1

            else:
                if i+1<len(binaries):
                    # if curr.address==0x147c:
                    #     print(f"{Colors.RED}{curr}{Colors.RESET}")
                    #     print(f"{Colors.RED}{binaries[i+1]}{Colors.RESET}")
                    binaryCFG.addEdge(
                        Edge(curr, binaries[i+1], Edge.Kind.Through)
                    )

            # elif(curr.mnemonic=="j"):
            #     target = CFGBuilder.findInsOfAddr(baseAddr+ int( curr.op_str,16))
            #     binaryCFG.addEdge(
            #         Edge(curr, target, Edge.Kind.GoTo)
            #     )

        binaryCFG.addEdge(
            Edge(binaries[len(binaries)-1], binaryCFG.get_exit(), Edge.Kind.Exit)
        )
        self.counts+=len(binaries)
        # print(self.counts)









def test():
    e1=Edge(1,2,Edge.Kind.Entry)
    e2=Edge(1,3)
    e3=Edge(2,3)
    cfg=BinaryCFG([1,2,3])
    cfg.addEdge(e1)
    print(cfg.inEdges[2])


    # cfgbuilder= CFGBuilder()
    # cfgbuilder.build()


if __name__ == "__main__":
    test()
