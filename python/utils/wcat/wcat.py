#!/usr/bin/env python3

"""

    An enhanced `cat` like program, with support read gz, zst compressed files.
    *** 1) Support read file list from stdin or from command line arguments.
    *** 2) Support read content from stdin, and output to stdout.
    *** 3) Support count the number of lines program processed and log it to file.
    
    @Author: wavefancy@gmail.com

    Usage:
        wcat.py [-i] [-c file] [-a] [-m txt] [-n] [<files>...]
        wcat.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Concatenate multiple files together, order as the appearence in parameters.
        2. Input files either in ziped(.gz), zst(.zst), or flat txts.

    Options:
        -i            Treat the stdin as content input, other than file names.
        -c file       Count the total number of lines program processed, 
                        and log the message to file.
        -m txt        Set the log message for parameter '-c'.
        -a            Append the log message to file ['-c'], instead of a new file.
        -n            If read from file list, add file name to each output line.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
import io
import codecs
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def ShowFormat():
    '''File format example'''
    print('''
''')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    LOG_FILE = args['-c'] if args['-c'] else False
    ReadFileNames = False if args['-i'] else True
    TotalLines = 0

    if ReadFileNames:
        # read file names from stdin or from parameters.
        names = args['<files>'] if args['<files>'] else []
        if not names:
            for line in sys.stdin:
                line = line.strip()
                if line:
                    names.append(line)

        import gzip
        import zstandard as zstd
        files = []
        zstfiles = []
        for f in names:
            if  f.endswith('.gz'):
                files.append(gzip.open(f, 'rt'))
            elif f.endswith('.zst'):
                # https://pypi.org/project/zstandard/, use text_stream to support read line by line.
                zst_temp = open(f, 'rb')
                dctx = zstd.ZstdDecompressor()
                stream_reader = dctx.stream_reader(zst_temp)
                text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')
                # cached files for read and close.
                files.append(text_stream)
                zstfiles.append(zst_temp)
            else:
                #files.append(open(f,'r'))
                files.append(open(f,'r',encoding="utf-8"))

        # sys.stdout.reconfigure(encoding='utf-8')
        for file,name in zip(files, names):
            for line in file:
                TotalLines += 1
                if args['-n']:
                    sys.stdout.write('%s: %s'%(name, line))
                else:
                    sys.stdout.write(line)

        #close files.
        [f.close() for f in files]
        [f.close() for f in zstfiles]
    else:
        # read content from stdin.
        for line in sys.stdin:
            TotalLines += 1
            sys.stdout.write(line)

    if LOG_FILE:
        mode = 'a' if args['-a'] else 'w'
        with open(LOG_FILE, mode=mode) as a_writer:
            if args['-m']:
                a_writer.write('%s. Total number of line: %d\n'%(args['-m'],TotalLines))
            else:
                a_writer.write('Total number of line: %d\n'%(TotalLines))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
