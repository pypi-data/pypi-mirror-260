import sys
import subprocess

from subprocess import CompletedProcess
from colorama import Fore, Style


def runs(*args, **kwargs) -> list[CompletedProcess]:
    """
    example:
    runs('cmd1 -args1', 'cmd2 -args1', 'cmd3 -args1')
    runs(['cmd1 -args1', 'cmd2 -args1', 'cmd3 -args1'])
    runs([['cmd1', '-args1'], ['cmd2', '-args1'], ['cmd3', '-args1']])
    """
    rets = []
    for arg in args:
        if isinstance(arg, str):
            ret = run(arg, **kwargs)
            rets.append(ret)
            if ret.returncode != 0:
                return rets
        elif isinstance(arg, (tuple, list)):
            for item in arg:
                ret = run(item, **kwargs)
                rets.append(ret)
                if ret.returncode != 0:
                    return rets
        else:
            raise Exception(f'invalid runs parameter type, must be str, tuple, list: {arg}')
    return rets


def run(*args, is_print=True, is_exit=True, **kwargs) -> CompletedProcess:
    """
    shell=True 时：
        1. args 如果是 str，shell 解释执行整个 args 字符串，
        2. args 如果是 tuple 或 list，args[0] 是传递给 shell 的需要执行的命令，args[1:] 是传递给 shell 自身的参数，而不是传递给需要执行的命令 args[0] 的参数
    shell=False 时，不能使用~等shell中的环境变量：
        1. args 如果是 str，整个 args 字符串被当做需要执行的文件名
        2. args 如果是 tuple 或 list，args[0] 是需要执行的文件名，args[1:] 是传递给 args[0] 命令的参数
    capture_output=True 时 stdout 和 stderr 将会被分别捕获，自动用 stdout=PIPE 和 stderr=PIPE 创建
    捕获并将两个流合并在一起，使用 stdout=PIPE 和 stderr=STDOUT 来代替 capture_output
    """
    if 'shell' not in kwargs:
        kwargs['shell'] = True
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    if not kwargs.get('capture_output') and not kwargs.get('stdout') and not kwargs.get('stderr'):
        kwargs['capture_output'] = True

    ret = subprocess.run(*args, **kwargs)

    if is_print:
        print(Fore.BLUE + f'> {ret.args}')
        if ret.stdout:
            print(Fore.GREEN + ret.stdout)
        if ret.stderr:
            print(Fore.RED + ret.stderr)
        print(Style.RESET_ALL, end='')

    if is_exit and ret.returncode != 0:
        sys.exit(ret.returncode)
    return ret
