import sys
import getopt
from file_spider import pdffile_to_fdfs

default_args = {'userName': 'someone', 'maxThread': 10, 'tempDir': '/tmp/'}


def Usage():
    print('usage:')
    print('-h,--help: print help message.')
    print('--user-name: downloader name, default', default_args['userName'])
    print('--max-thread: max threads, default', default_args['maxThread'])
    print('--temp-dir: file temp dir, default', default_args['tempDir'])


def parse_args(argv):
    _args = default_args
    try:
        opts, args = getopt.getopt(argv[1:], 'h:', ['user-name=', 'max-thread=', 'temp-dir='])
    except getopt.GetoptError as err:
        Usage()
        sys.exit(2)
    for o, v in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('--user-name',):
            _args['userName'] = v
        elif o in ('--max-thread',):
            _args['maxThread'] = v
        elif o in ('--temp-dir',):
            _args['tempDir'] = v
        else:
            print('unhandled option')
            sys.exit(3)
    return _args


if __name__ == '__main__':
    args = parse_args(sys.argv)
    task = pdffile_to_fdfs.FileMain(userName=args['userName'], maxThread=args['maxThread'], tempDir=args['tempDir'])
    while task.hasNext():
        task.craw()
        succeed, failed, active, total = task.statistic()
        print("成功 %s,失败 %s,正在爬取 %s" % (succeed, failed, active))

    task.close()
