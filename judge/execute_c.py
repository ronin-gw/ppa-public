import logging as lg
import os
import subprocess
import tempfile
import threading
from config import *

def strip_easysandbox(s):
    magic = '<<entering SECCOMP mode>>\n'
    if s.startswith(magic):
        return s[len(magic):]

class Command(object):
    def __init__(self, cmd, fi):
        self.cmd = cmd
        self.fi = fi
        self.process = None
        self.stdoutdata = b''
        self.stderrdata = b''

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True, stdin=self.fi, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (self.stdoutdata, self.stderrdata) = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            return False
        return True

class ExecuteC:
    def __init__(self, src, prefix='tmp'):
        """ Construct an instance for compiling and running a code.

        Params:
            src: The source code
            prefix: The pefix for the names of the temporary files.

        """
        # Create a temporary file for the source code.
        fd, name = tempfile.mkstemp(prefix=prefix, suffix='.c')
        fo = os.fdopen(fd, "w")
        fo.write(src)
        fo.close()        

        # Filenames for the source code and binary.
        self.src = name
        self.bin = name + '.bin'

        lg.debug('src: {}'.format(self.src))
        lg.debug('bin: {}'.format(self.bin))

    def __del__(self):
        """ Destructs the instance with removing temporary files.

        """
        if os.path.exists(self.src):
            os.remove(self.src)
            self.src = None
        if os.path.exists(self.bin):
            os.remove(self.bin)
            self.bin= None
    
    def compile(self):
        """ Compile the source code.

        Returns:
            int: Return value from the compiler.
            str: Error message.

        """
        cmd = COMPILE.format(src=self.src, bin=self.bin)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutadta, stderrdata = p.communicate()
        lg.debug('Compile ({}): {}'.format(p.returncode, cmd))
        return cmd, p.returncode, stderrdata.decode('utf-8')

    def run(self, argv='', fi=None, timeout=5.0):
        """ Run the program.

        Params:
            argv: Optional argument for the program
            fi: File object for STDIN
            timeout: Timeout in seconds.

        Returns:
            object: Object containing the execusion result.

        """
        cmd = RUN.format(bin=self.bin, argv=argv)
        lg.debug('Run {}'.format(cmd))
        #p = subprocess.Popen(cmd, shell=True, stdin=fi, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdoutdata, stderrdata = p.communicate(timeout=timeout)
        c = Command(cmd, fi)
        finished = c.run(timeout)
        lg.debug('Run ({}): {}'.format(c.process.returncode, cmd))
        if finished:
            return (
                '',
                c.process.returncode,
                strip_easysandbox(c.stdoutdata.decode(ENCODING, 'ignore')),
                strip_easysandbox(c.stderrdata.decode(ENCODING, 'ignore')),
                )
        else:
            lg.debug('Terminated with timeout: {}'.format(cmd))
            return ('timeout', -1, '', '')
            
if __name__ == '__main__':
    logger = lg.getLogger()
    logger.setLevel(lg.DEBUG)

    J = JudgeC('#include <stdio.h>\nint main() {\n printf("OK");\nreturn 0;\n}\n')
    J.compile()
    r = J.run()
    print(r.stdout)
    print(r.stderr)
