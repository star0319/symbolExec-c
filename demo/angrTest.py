import angr
from angrutils import *


# path="/home/wsx/symexc/symex-x86"
path="/home/wsx/coreutils/src/ls"

p = angr.Project(path, load_options={'auto_load_libs': False})

# Generate a static CFG
# cfg = p.analyses.CFGFast()

# generate a dynamic CFG
# cfg = p.analyses.CFGEmulated(keep_state=True)



# proj = angr.Project("<...>/ais3_crackme", load_options={'auto_load_libs':False})
main = p.loader.main_object.get_symbol("main")
start_state = p.factory.blank_state(addr=main.rebased_addr)
cfg = p.analyses.CFGEmulated(fail_fast=True, starts=[main.rebased_addr], initial_state=start_state)
plot_cfg(cfg, "ais3_cfg1", asminst=True, remove_imports=True, remove_path_terminator=True)



print("This is the graph:", cfg.graph)
print("It has %d nodes and %d edges" % (len(cfg.graph.nodes()), len(cfg.graph.edges())))


entry_node = cfg.get_any_node(p.entry)

# on the other hand, this grabs all of the nodes
print("There were %d contexts for the entry block" % len(cfg.get_all_nodes(p.entry)))

# we can also look up predecessors and successors
print("Predecessors of the entry point:", entry_node.predecessors)
print("Successors of the entry point:", entry_node.successors)
print("Successors (and type of jump) of the entry point:", [ jumpkind + " to " + str(node.addr) for node,jumpkind in cfg.get_successors_and_jumpkind(entry_node) ])


