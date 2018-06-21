#!/usr/bin/env python

"""

    Convert input file/folder list as Google cloud sync command.
    1. Folder sync by gsutil sync
    2. File sync by gsutil cp command, because gs sync do not support sync files.

    @Author: wavefancy@gmail.com

    Usage:
        GCPSyncCMD.py -b bucket [--gz]
        GCPSyncCMD.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin (file name line by line), and output results to stdout.

    Options:
        -b bucket     Google cloud bucket name, eg: gs://2018backup_kathlab.
        --gz          Test whether a missing file has .gz format file.
                          IF yes, output the backup command for zipped file.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
import os.path as path

def ShowFormat():
    '''Input File format example:'''
    print('''
# cat test.txt | python3 GCPSyncCMD.py -b gs:test_gc --gz
#-----------------------------
gsutil -o GSUtil:parallel_composite_upload_threshold=150M -m cp -n GCPSyncCMD.py gs:test_gc/GCPSyncCMD.py
gsutil -m rsync -r data gs:test_gc/data
WARN(skipped) not a file or directory: fake
gsutil -o GSUtil:parallel_composite_upload_threshold=150M -m cp -n test2 gs:test_gc/test2.gz
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    GZ_END   = '.gz'
    CHECK_GZ = True if args['--gz'] else False # checking gzipped files.
    G_BUCKET = args['-b']
    if not G_BUCKET.endswith('/'):
        G_BUCKET += '/'

    def trimStart(d):
        '''Delete the starts / if any'''
        if d.startswith('/'):
            d = d[1:]
        return d

    for line in sys.stdin:
        line = line.strip()
        if line:
            if line.endswith('/'):
                line = line[:-1]


            if path.isfile(line):
                # -n: existing files or objects at the destination will not be overwritten
                # https://cloud.google.com/storage/docs/gsutil/commands/cp
                sys.stdout.write('gsutil -o GSUtil:parallel_composite_upload_threshold=150M -m cp -n %s %s%s\n'%(line, G_BUCKET, trimStart(line)))
            elif path.isdir(line):
                # -r recursively, copy all files within a directory.
                # https://cloud.google.com/storage/docs/gsutil/commands/rsync
                sys.stdout.write('gsutil -m rsync -r %s %s%s\n'%(line, G_BUCKET, trimStart(line)))
            else:
                if CHECK_GZ:
                    line_gz = line + GZ_END
                    if path.isfile(line_gz):
                        sys.stdout.write('gsutil -o GSUtil:parallel_composite_upload_threshold=150M -m cp -n %s %s%s\n'%(line_gz, G_BUCKET, trimStart(line_gz)))
                        continue

                sys.stderr.write('WARN(skipped) not a file or directory: %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
