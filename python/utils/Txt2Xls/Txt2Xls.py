#!/usr/bin/env python3

"""

    Convert text file to excel file.

    @Author: wavefancy@gmail.com

    Usage:
        Txt2Xls.py -o oname [--rc cindex] [-d string]
        Txt2Xls.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Line index start from 1.

    Options:
        -o string     Output file name.
        -d string     Set the column delimiter, default whitespace+. tab for '\\t'.
        --rc cindex   Format row color by the value at column 'cindex'.
        -e index      Set end line index, (inclusive).
        -a number     Set the end line as '-n index' + 'number', (inclusive).
        -r number     From start line, repeatly copy one line then skip 'number' lines, until reach file end.
        -f file       Read line index from 'file', one line one index, load all in memory.
        -h --help     Show this screen.
        -v --version  Show version.

    Dependency:
        xlsxwriter

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

class P(object):
    start = -1 # start line index
    end = -1 # end line index
    nskip = -1
    lineSet = set()
    maxLine = -1 #maximum line index need to be output.

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)
#
#     if(args['--format']):
#         ShowFormat()
#         sys.exit(-1)
# #
    outname = args['-o'] + '.xlsx'
    rc = -1 #row colow column index.
    if args['--rc']:
        rc = int(args['--rc']) -1

    # if args['-n']:
    #     P.start = int(args['-n'])
    # if args['-e']:
    #     P.end = int(args['-e'])
    # if args['-a']:
    #     P.end = P.start + int(args['-a'])
    # if args['-r']:
    #     P.nskip = int(args['-r'])
    # if args['-f']:
    #     ll = [int(x) for x in open(args['-f'], 'r')]
    #     P.maxLine = max(ll)
    #     P.lineSet = set(ll)

    import xlsxwriter
    from xlsxwriter.utility import xl_rowcol_to_cell
    cell = xl_rowcol_to_cell(1, 2)  # C2

    # Create a workbook and add a worksheet. automatic converting string to number.
    # http://stackoverflow.com/questions/20748346/python-xlsxwriter-only-writes-as-a-text-when-using-csv-data
    workbook = xlsxwriter.Workbook(outname,{'strings_to_numbers': True})
    worksheet = workbook.add_worksheet()


    # Add a format. Light red fill with dark red text.
    # A2 : col row
    format1 = workbook.add_format()
    format2 = workbook.add_format({'bg_color': '#EEEEEE',
                               #'font_color': '#9C0006'
                               })
    formats = [format1, format2]
    rc_temp = -1
    def getFormat():
        '''change color format at each call'''
        global rc_temp
        rc_temp = rc_temp + 1
        return formats[rc_temp % len(formats)]
    delimiter = args['-d'] if args['-d'] else None
    if delimiter.upper() == 'TAB':
        delimiter = '\t'

    row = 0
    col = 0
    maxCol = 0
    rc_temp_value = ''
    current_format = ''
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split(delimiter)
            col = 0
            for x in ss:
                if rc >= 0:  #change row color if value change.
                    if rc_temp_value != ss[rc]:
                        rc_temp_value = ss[rc]
                        current_format = getFormat()

                    worksheet.write(row, col, x, current_format) #row col,
                else:
                    worksheet.write(row, col, x) #row col,

                col += 1
                if col > maxCol:
                    maxCol = col
            row += 1

    # for x in range(row-1):
    #     lcell = xl_rowcol_to_cell(x, 0)
    #     rcell = xl_rowcol_to_cell(x, maxCol)
    #     mcell = xl_rowcol_to_cell(x, 1)
    #     worksheet.conditional_format(lcell + ':' + rcell, {'type': 'cell',
    #                                         'criteria': '>=',
    #                                         'value':    mcell,
    #                                         'format':   format1})

    workbook.close()

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
