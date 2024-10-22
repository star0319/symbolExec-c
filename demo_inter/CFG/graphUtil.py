import pygraphviz as pgv

from CFG.cfg import NOP, Edge

class GraphUtil():



    def __init__(self):
        # 创建有向图对象
        self.G = pgv.AGraph(directed=True)
        # self.cfg = cfg

    def getStringFromNode(self, node, baseAddr):
        if isinstance(node, NOP):
            return node.__str__()
        # return '<CsInsn 0x%x : %s %s>' % (node.address+0x2790 , node.mnemonic, node.op_str)
        # return '<CsInsn 0x%x : %s %s>' % (node.address+0x1149 , node.mnemonic, node.op_str)
        return '<CsInsn 0x%x : %s %s>' % (node.address + baseAddr, node.mnemonic, node.op_str)

    def generateGraph(self,cfg, outPath="output.dot"):
        # 添加节点
        baseAddr = cfg.baseAddr
        cfgNodes = cfg.nodes
        for node in cfgNodes:
            # print(node)

            self.G.add_node(self.getStringFromNode(node, baseAddr))

        # 添加边
        cfgEdges = cfg.outEdges
        for edges in cfgEdges.values():
            # if edges is None:
            #     continue
            for edge in edges:
                self.G.add_edge(self.sgetStringFromNode(edge.get_src(), baseAddr), self.getStringFromNode(edge.get_dst(), baseAddr))

        # 保存为Dot文件
        self.G.write(outPath)

    def generateBBGraph(self,cfg, outPath="output.dot"):
        # 添加节点
        baseAddr = cfg.baseAddr
        cfgNodes = cfg.nodes
        # print(cfgNodes)

        # cfgEdges = cfg.outEdges
        # for edges in cfgEdges.values():
        #     # if edges is None:
        #     #     continue
        #     for edge in edges:
        #         print(edge)

        tempIn = {}
        tempOut = {}
        temp = ""
        prenode = None
        # getStringFromNode=self.getStringFromNode
        # G=self.G
        for node in cfgNodes:
            # print(node)
            if isinstance(node, NOP):
                temp += (self. getStringFromNode(node, baseAddr) + "\n")
            else:
                flag = False
                edgs = cfg.getInedgeOf(node)
                # print(edgs)
                if edgs is not None:
                    for edg in edgs:
                        # print(edg.kind)
                        if edg.kind == Edge.Kind.je:
                            flag = True
                else:
                    flag = True
                if flag:
                    # print(getStringFromNode(prenode))
                    # print(prenode)
                    tempOut[self. getStringFromNode(prenode, baseAddr)] = temp
                    tempIn[temp.split("\n")[0]] = temp
                    self. G.add_node(temp)
                    temp = (self.getStringFromNode(node, baseAddr) + "\n")
                else:
                    temp += (self.getStringFromNode(node, baseAddr) + "\n")

            prenode = node

        if temp != "":
            tempOut[self. getStringFromNode(prenode, baseAddr)] = temp
            tempIn[temp.split("\n")[0]] = temp
            self.G.add_node(temp)

        # 添加边
        cfgEdges = cfg.outEdges
        for edges in cfgEdges.values():
            # if edges is None:
            #     continue
            for edge in edges:
                # print(edge)
                # if edge.kind==Edge.Kind.je:
                # G.add_edge(getStringFromNode(edge.get_src()),getStringFromNode(edge.get_dst()))
                # print(tempOut)
                if tempOut.__contains__(self. getStringFromNode(edge.get_src(), baseAddr)):
                    # print(edge)
                    # print(self. getStringFromNode(edge.get_src(), baseAddr))
                    # print(self. getStringFromNode(edge.get_dst(), baseAddr))
                    # print(hex( baseAddr))
                    self. G.add_edge(tempOut[self. getStringFromNode(edge.get_src(), baseAddr)],
                               tempIn[self. getStringFromNode(edge.get_dst(), baseAddr)])

        # 保存为Dot文件
        self.G.write(outPath)

