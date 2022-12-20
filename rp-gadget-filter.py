#rp-win-filter
import sys
import textwrap

def load_file(filename):
    gadgets = []
    raw_rop_file = open(filename, 'r')
    lines = raw_rop_file.readlines()
    for line in lines:
        if "0x" in line:
            gadgets.append(line)
    return gadgets

def remove_troublesome_operands(gadgets):
    useful_gadgets = []
    troublesome_operands = ["clts", "hlt", "lmsw", "ltr", "lgdt", "lidt" ,"lldt", "mov cr", "mov dr",
    "mov tr", "in ", "ins", "invlpg", "invd", "out", "outs", "cli", "sti"
    "popf", "pushf", "int", "iret", "iretd", "swapgs", "wbinvd", "call",
    "jmp", "leave", "ja", "jb", "jc", "je", "jr", "jg", "jl", "jn", "jo",
    "jp", "js", "jz", "lock", "enter", "wait", "???"]

    for gadget in gadgets:
        bad_gadget = False
        for operand in troublesome_operands:
            if operand in gadget:
                bad_gadget = True
        if bad_gadget != True:
            useful_gadgets.append(gadget)
    return useful_gadgets


def remove_bad_chars(less_troublesome_gadgets, badchars):
    useful_gadgets = []
    for gadget in less_troublesome_gadgets:
        bad_gadget = False
        address = gadget[0:10]
        bytes = textwrap.wrap(address, 2)
        for badchar in badchars:
            if badchar[2::] in bytes:
                bad_gadget = True
        if bad_gadget != True:
            useful_gadgets.append(gadget)
    return useful_gadgets
                

def write_useful_gadgets_to_file(useful_gadgets, filename):
    useful_file = open(f'useful_{filename}', 'w')
    useful_file.writelines(useful_gadgets)
    useful_file.close()

def main():
    arguments = []
    if len(sys.argv) <= 2:
        print(f"The proper usage is: {sys.argv[0]} output_from_rp++_rop.txt 0x00 0x20 etc")
        print("You will need to provide atleast one bad character, if you don't have any for some reason just modify this check.")
        sys.exit()
    else:
        for i, arg in enumerate(sys.argv):
            arguments.append(arg)
    badchars = []
    for x in range(2,len(arguments)):
        if len(arguments[x]) != 4:
            print(f"Bad characters need the following format 0x00 0x01 0x20. The provided bad character {arguments[x]} will work out the box.")
            sys.exit()
        badchars.append(arguments[x])
    gadgets = load_file(sys.argv[1])
    print(f"There are {len(gadgets)} total gadgets")
    less_troublesome_gadgets = remove_troublesome_operands(gadgets)
    useful_gadgets = remove_bad_chars(less_troublesome_gadgets, badchars)
    print(f"There are {len(useful_gadgets)} useful gadgets")
    write_useful_gadgets_to_file(useful_gadgets, sys.argv[1])
    
main()
