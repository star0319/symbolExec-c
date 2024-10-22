import cmd
import os


if __name__ == "__main__":
    directory = '/Users/star/code/py/symbol_excution/coreutils/CFG_output/cat'
    # directory="/Users/star/code/binary_analysis/c++/perf_test/CFG_output/symex-x86"
    file_names = [f for f in os.listdir(directory) if not os.path.isdir(os.path.join(directory, f))]
    # os.system(f"cd {directory}")
    # os.system(f"pwd")

    for filename in file_names:
        if filename.split('.')[1]=="dot":
            os.system(f"cd {directory};  dot {filename} -T svg -o {filename.split('.')[0]}.svg")