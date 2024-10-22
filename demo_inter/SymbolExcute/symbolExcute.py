from CFG.cfg import NOP
from SymbolExcute.z3SloverUtil import Z3SolverUtil


def findAddress_in_Dword(target):
    stackAddress = target[target.find('[') + 1:target.find(']')]
    return stackAddress
class SymbolExcute():
    def __init__(self,cfg):
        #   初始化
        self.cfg=cfg


    def getNextStmts(self,comIn):
        edges = self.cfg.outEdges[comIn]
        nexts=[]
        for edge in edges:
            nexts.append(edge.get_dst())
        # print(nexts)
        # nexts.sort()
        return nexts
    def excute(self):
        entry=self.cfg.get_entry()
        next= self.cfg.outEdges[entry].pop().get_dst()
        # print(next)
        state={}
        pc="true"
        self.excuteNext(next,state,pc)

        return

    #单条语句执行
    def excuteNext(self,nextStmt,state,pc):

        if isinstance(nextStmt,NOP) and nextStmt==self.cfg.get_exit():
            print(pc)
            print(state)
            print("exittt")
            return

        # assert 0x45
        # if nextStmt.address==0x45:
        #     print("ssss")
        #     print(pc)
        #     print(state)
        #     ops = nextStmt.op_str.split(", ")
        #     # print(ops)
        #     # cmp op0,op1
        #     op0 = ops[0]
        #     op1 = ops[1]
        #     op0 = state.get(op0)
        #     op1 = state.get(op1)
        #     pc+="^"+op0+"=="+op1
        #     z3=Z3SolverUtil()
        #     z3.solve(pc)
        #     return
        # print(nextStmt)


        cmd= nextStmt.mnemonic
        match cmd:
            # case "endbr64":
            #     print("endbr64")
            # case "push":
            #     print("push")
            case "cmp":
                # print("cmp")
                # print(nextStmt.op_str)

                ops = nextStmt.op_str.split(", ")
                # print(ops)
                # cmp op0,op1
                op0 = ops[0]
                op1 = ops[1]
                # cmp dword ptr [rbp - 0x14], 0
                if op1.isdigit():
                   op0=  state.get(op0)

                # cmp eax, dword ptr [rbp - 4]
                else:
                    op0=state.get(op0)
                    op1=state.get(op1)



                nextStmt = self.getNextStmts(nextStmt).pop()
                cmd1= nextStmt.mnemonic
                jmpAdress=nextStmt.op_str
                # print(nextStmt.mnemonic)
                # print(nextStmt.address)
                nextStmts = self.getNextStmts(nextStmt)
                stmt1=nextStmts[0]
                stmt2=nextStmts[1]

                if cmd1 == "je":
                    # print(stmt1.address)
                    # print(int(jmpAdress, 16))
                    # print(stmt2.address)
                    #stmt1是jmp目的地址
                    if stmt1.address==int(jmpAdress, 16):
                        pc1=pc+"^"+op0+"=="+op1
                        state1=state.copy()
                        self.excuteNext(stmt1, state1, pc1)
                        pc2=pc+"^"+op0+"!="+op1
                        state2 = state.copy()
                        self.excuteNext(stmt2, state2, pc2)

                    # stmt2是jmp目的地址
                    else:
                        pc1=pc+"^"+op0+"!="+op1
                        state1=state.copy()
                        self.excuteNext(stmt1, state1, pc1)
                        pc2=pc+"^"+op0+"=="+op1
                        state2 = state.copy()
                        self.excuteNext(stmt2, state2, pc2)
                elif cmd1 == "jne":
                    # print(stmt1.address)
                    # print(int(jmpAdress, 16))
                    # print(stmt2.address)
                    #stmt2是jmp目的地址
                    if stmt2.address==int(jmpAdress, 16):
                        pc1=pc+"^"+op0+"=="+op1
                        state1=state.copy()
                        self.excuteNext(stmt1, state1, pc1)
                        pc2=pc+"^"+op0+"!="+op1
                        state2 = state.copy()
                        self.excuteNext(stmt2, state2, pc2)

                    # stmt1是jmp目的地址
                    else:
                        pc1=pc+"^"+op0+"!="+op1
                        state1=state.copy()
                        self.excuteNext(stmt1, state1, pc1)
                        pc2=pc+"^"+op0+"=="+op1
                        state2 = state.copy()
                        self.excuteNext(stmt2, state2, pc2)

                return



                # print(state)

            case "mov":
                # print("mov")
                # print(nextStmt.op_str)
                ops= nextStmt.op_str.split(", ")
                # print(ops)
                target= ops[0]
                sourse=ops[1]
                # mov dword ptr [rbp - 0x14], edi
                # if target.startswith("dword ptr"):
                    # stackAddress=findAddress_in_Dword(target)
                    # print(stackAddress)
                    # if sourse=="edi" or sourse=="esi":
                        # state.update(stackAddress,sourse)
                        # state.update(target,sourse)
                    # else:
                    #     state.update(target,state.get(sourse))

                # if sourse == "edi" or sourse == "esi"  or sourse.isdigit():

                if sourse == "edi" or sourse == "esi" or sourse == "rdi" or sourse == "edx" or sourse.isdigit():
                    # print(sourse)
                    state[target]= sourse
                else:
                    # print(f"sss{sourse}")
                    state[target]= state.get(sourse)

                # print(state)

            case "add":
                # print("add")
                ops = nextStmt.op_str.split(", ")
                # print(ops)
                # add op0,op1
                op0 = ops[0]
                op1 = ops[1]
                 #add eax 0
                if  op1.isdigit():
                    state[op0] =state[op0]+ "+"+op1
                #add eax,ebx
                else:
                    state[op0] = state[op0]+ "+"+state.get(op1)

                # print(state)


            # case _:
            #     print(cmd+nextStmt.op_str)

        nextStmts=self.getNextStmts(nextStmt)

        for stmt in nextStmts:
            self.excuteNext(stmt,state,pc)




        return
