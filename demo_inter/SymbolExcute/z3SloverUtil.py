# coding:utf8
from z3 import *

class Z3SolverUtil():



    def __init__(self):
        # # 首先创建一个求解器
        self.s =  Solver()


    def solve(self,pc):
        # print(pc)
        pcs=pc.split("^")
        # print(pcs)

        esi = Int('esi')
        edi = Int('edi')
        for pc in pcs:
            if pc=="true":
                continue
            else:
                self.s.add(eval(pc))


        print(self. s.check())
        if self.s.check()==sat:
            m = self.s.model()
            print(m)

