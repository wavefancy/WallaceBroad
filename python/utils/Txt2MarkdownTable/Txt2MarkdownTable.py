#!/usr/bin/env python3

"""

    Covert input txt as markdown table format.

    @Author: wavefancy@gmail.com

    Usage:
        Txt2MarkdownTable.py [--rb int] [-n]
        Txt2MarkdownTable.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
        --rb int      Make row as bold format, 1 based. ex. 1|1,3.
        -n            Set no title line.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input:
    ------------------------
T1      T2
1       2
2       3

    #output: --rb 2
    ------------------------
| T1    | T2    |
| :---  | :---  |
| **1** | **2** |
| 2     | 3     |

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    rb = [int(x)-1 for x in args['--rb'].split(',')] if args['--rb'] else []

    """MMD Table Formatter.
    # Taken from: https://codereview.stackexchange.com/questions/145262/source-formatting-of-markdown-table
    Silly script that takes a MMD table as a
    string and returns a tidied version of the table
    """
    def get_alignment(cell):
        """"
        :---"    left aligned
        "---:"    right aligned
        ":--:"    centered (also accepts "---"), default
        """
        if cell.startswith(":") and not cell.endswith(":"):
            return str.ljust
        elif cell.endswith(":") and not cell.startswith(":"):
            return str.rjust
        elif cell.endswith(":") and cell.startswith(":"):
            return str.center
        else:
            return str.ljust


    # For "cleaned" table entries:
    rows = [[el.strip() for el in row.strip().split()] for row in sys.stdin]
    for x in rb:
        rows[x] = ['**'+x+'**' for x in rows[x]]

    #add the second align rows, set default left align. if no -n specified.
    if not args['-n']:
        rows = [rows[0]] + [[':---' for x in rows[0]]] + rows[1:]
    # print(rows)

    # Max length of each "entry" is what we'll use
    # to evenly space "columns" in the final table
    col_widths = [max(map(len, column)) for column in zip(*rows)]
    # print(col_widths)

    # Let's align entries as per intended formatting.
    # Second line of input string contains alignment commmands:
    alignments = [get_alignment(x) for x in rows[1]]
    # alignments = [str.ljust for x in rows[0]]

    # Prepare for output string:
    out = []
    for row in rows:
        for entry, width, align in zip(row, col_widths, alignments):
            # print('E:'+entry +"---"+ str(width) +"---"+ str(align))
            if not width:
                continue
            out.append("| {} ".format(align(entry, width)))
        out.append("|\n")
        # print(out)

    query = "".join(out)

    sys.stdout.write(query)
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
