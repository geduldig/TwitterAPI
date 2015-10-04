""" Stdout, stdin, stderr and argv support for unicode. """
##############################################
# Support for unicode in windows cmd.exe
# Posted on Stack Overflow [1], available under CC-BY-SA [2]
#
# Question: "Windows cmd encoding change causes Python crash" [3] by Alex [4],
# Answered [5] by David-Sarah Hopwood [6].
#
# [1] https://stackoverflow.com
# [2] https://creativecommons.org/licenses/by-sa/3.0/
# [3] https://stackoverflow.com/questions/878972
# [4] https://stackoverflow.com/users/85185
# [4] https://stackoverflow.com/a/3259271/118671
# [5] https://stackoverflow.com/users/393146
#
##############################################

from __future__ import print_function
import sys
stdin = sys.stdin
stdout = sys.stdout
stderr = sys.stderr
argv = sys.argv

if sys.version_info[0] > 2:
    unicode = str

if sys.platform == "win32":
    import codecs
    from ctypes import WINFUNCTYPE, windll, POINTER
    from ctypes import byref, c_int, create_unicode_buffer
    from ctypes.wintypes import BOOL, HANDLE, DWORD, LPWSTR, LPCWSTR
    try:
        from ctypes.wintypes import LPVOID
    except ImportError:
        from ctypes import c_void_p as LPVOID

    original_stderr = sys.stderr

    # If any exception occurs in this code, we'll probably try to print it on stderr,
    # which makes for frustrating debugging if stderr is directed to our wrapper.
    # So be paranoid about catching errors and reporting them to original_stderr,
    # so that we can at least see them.
    def _complain(message):
        print(isinstance(message, str) and message or repr(message), file=original_stderr)

    # Work around <http://bugs.python.org/issue6058>.
    codecs.register(lambda name: name == 'cp65001' and codecs.lookup('utf-8') or None)

    # Make Unicode console output work independently of the current code page.
    # This also fixes <http://bugs.python.org/issue1602>.
    # Credit to Michael Kaplan <http://blogs.msdn.com/b/michkap/archive/2010/04/07/9989346.aspx>
    # and TZOmegaTZIOY
    # <https://stackoverflow.com/questions/878972/windows-cmd-encoding-change-causes-python-crash/1432462#1432462>.
    try:
        # <https://msdn.microsoft.com/en-us/library/ms683231(VS.85).aspx>
        # HANDLE WINAPI GetStdHandle(DWORD nStdHandle);
        # returns INVALID_HANDLE_VALUE, NULL, or a valid handle
        #
        # <https://msdn.microsoft.com/en-us/library/aa364960(VS.85).aspx>
        # DWORD WINAPI GetFileType(DWORD hFile);
        #
        # <https://msdn.microsoft.com/en-us/library/ms683167(VS.85).aspx>
        # BOOL WINAPI GetConsoleMode(HANDLE hConsole, LPDWORD lpMode);

        GetStdHandle = WINFUNCTYPE(HANDLE, DWORD)(("GetStdHandle", windll.kernel32))
        STD_INPUT_HANDLE = DWORD(-10)
        STD_OUTPUT_HANDLE = DWORD(-11)
        STD_ERROR_HANDLE = DWORD(-12)
        GetFileType = WINFUNCTYPE(DWORD, DWORD)(("GetFileType", windll.kernel32))
        FILE_TYPE_CHAR = 0x0002
        FILE_TYPE_REMOTE = 0x8000
        GetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, POINTER(DWORD))(("GetConsoleMode", windll.kernel32))
        INVALID_HANDLE_VALUE = DWORD(-1).value

        def not_a_console(handle):
            if handle == INVALID_HANDLE_VALUE or handle is None:
                return True
            return ((GetFileType(handle) & ~FILE_TYPE_REMOTE) != FILE_TYPE_CHAR
                    or GetConsoleMode(handle, byref(DWORD())) == 0)

        old_stdin_fileno = None
        old_stdout_fileno = None
        old_stderr_fileno = None

        if hasattr(sys.stdin, 'fileno'):
            old_stdin_fileno = sys.stdin.fileno()
        if hasattr(sys.stdout, 'fileno'):
            old_stdout_fileno = sys.stdout.fileno()
        if hasattr(sys.stderr, 'fileno'):
            old_stderr_fileno = sys.stderr.fileno()

        STDIN_FILENO = 0
        STDOUT_FILENO = 1
        STDERR_FILENO = 2
        real_stdin = (old_stdin_fileno == STDIN_FILENO)
        real_stdout = (old_stdout_fileno == STDOUT_FILENO)
        real_stderr = (old_stderr_fileno == STDERR_FILENO)

        if real_stdin:
            hStdin = GetStdHandle(STD_INPUT_HANDLE)
            if not_a_console(hStdin):
                real_stdin = False

        if real_stdout:
            hStdout = GetStdHandle(STD_OUTPUT_HANDLE)
            if not_a_console(hStdout):
                real_stdout = False

        if real_stderr:
            hStderr = GetStdHandle(STD_ERROR_HANDLE)
            if not_a_console(hStderr):
                real_stderr = False

        if real_stdin:
            ReadConsoleW = WINFUNCTYPE(BOOL, HANDLE, LPVOID, DWORD, POINTER(DWORD),
                                       LPVOID)(("ReadConsoleW", windll.kernel32))

            class UnicodeInput:

                """Unicode terminal input class."""

                def __init__(self, hConsole, name, bufsize=1024):
                    self._hConsole = hConsole
                    self.bufsize = bufsize
                    self.buffer = create_unicode_buffer(bufsize)
                    self.name = name
                    self.encoding = 'utf-8'

                def readline(self):
                    maxnum = DWORD(self.bufsize - 1)
                    numrecv = DWORD(0)
                    result = ReadConsoleW(self._hConsole, self.buffer, maxnum, byref(numrecv), None)
                    if not result:
                        raise Exception("stdin failure")
                    return self.buffer.value[:numrecv.value].encode(self.encoding)

        if real_stdout or real_stderr:
            # BOOL WINAPI WriteConsoleW(HANDLE hOutput, LPWSTR lpBuffer, DWORD nChars,
            #                           LPDWORD lpCharsWritten, LPVOID lpReserved);

            WriteConsoleW = WINFUNCTYPE(BOOL, HANDLE, LPWSTR, DWORD, POINTER(DWORD),
                                        LPVOID)(("WriteConsoleW", windll.kernel32))

            class UnicodeOutput:

                """Unicode terminal output class."""

                def __init__(self, hConsole, stream, fileno, name):
                    self._hConsole = hConsole
                    self._stream = stream
                    self._fileno = fileno
                    self.closed = False
                    self.softspace = False
                    self.mode = 'w'
                    self.encoding = 'utf-8'
                    self.name = name
                    self.flush()

                def isatty(self):
                    return False

                def close(self):
                    # don't really close the handle, that would only cause problems
                    self.closed = True

                def fileno(self):
                    return self._fileno

                def flush(self):
                    if self._hConsole is None:
                        try:
                            self._stream.flush()
                        except Exception as e:
                            _complain("%s.flush: %r from %r"
                                      % (self.name, e, self._stream))
                            raise

                def write(self, text):
                    try:
                        if self._hConsole is None:
                            if isinstance(text, unicode):
                                text = text.encode('utf-8')
                            self._stream.write(text)
                        else:
                            if not isinstance(text, unicode):
                                text = bytes(text).decode('utf-8')
                            remaining = len(text)
                            while remaining > 0:
                                n = DWORD(0)
                                # There is a shorter-than-documented limitation on the
                                # length of the string passed to WriteConsoleW (see
                                # <https://tahoe-lafs.org/trac/tahoe-lafs/ticket/1232>.
                                retval = WriteConsoleW(self._hConsole, text,
                                                       min(remaining, 10000),
                                                       byref(n), None)
                                if retval == 0 or n.value == 0:
                                    raise IOError("WriteConsoleW returned %r, n.value = %r"
                                                  % (retval, n.value))
                                remaining -= n.value
                                if remaining == 0:
                                    break
                                text = text[n.value:]
                    except Exception as e:
                        _complain("%s.write: %r" % (self.name, e))
                        raise

                def writelines(self, lines):
                    try:
                        for line in lines:
                            self.write(line)
                    except Exception as e:
                        _complain("%s.writelines: %r" % (self.name, e))
                        raise

            if real_stdin:
                stdin = UnicodeInput(hStdin, name='<Unicode console stdin>')

            if real_stdout:
                stdout = UnicodeOutput(hStdout, None, STDOUT_FILENO,
                                       '<Unicode console stdout>')
            else:
                stdout = UnicodeOutput(None, sys.stdout, old_stdout_fileno,
                                       '<Unicode redirected stdout>')

            if real_stderr:
                stderr = UnicodeOutput(hStderr, None, STDERR_FILENO,
                                       '<Unicode console stderr>')
            else:
                stderr = UnicodeOutput(None, sys.stderr, old_stderr_fileno,
                                       '<Unicode redirected stderr>')
    except Exception as e:
        _complain("exception %r while fixing up sys.stdout and sys.stderr" % (e,))

    # While we're at it, let's unmangle the command-line arguments:

    # This works around <http://bugs.python.org/issue2128>.
    GetCommandLineW = WINFUNCTYPE(LPWSTR)(("GetCommandLineW", windll.kernel32))
    CommandLineToArgvW = WINFUNCTYPE(POINTER(LPWSTR), LPCWSTR, POINTER(c_int))(("CommandLineToArgvW", windll.shell32))

    argc = c_int(0)
    argv_unicode = CommandLineToArgvW(GetCommandLineW(), byref(argc))

    argv = [argv_unicode[i].encode('utf-8') for i in range(0, argc.value)]

    if not hasattr(sys, 'frozen'):
        # If this is an executable produced by py2exe or bbfreeze, then it will
        # have been invoked directly. Otherwise, unicode_argv[0] is the Python
        # interpreter, so skip that.
        argv = argv[1:]

        # Also skip option arguments to the Python interpreter.
        while len(argv) > 0:
            arg = argv[0]
            if not arg.startswith(b"-") or arg == u"-":
                break
            argv = argv[1:]
            if arg == u'-m':
                # sys.argv[0] should really be the absolute path of the module source,
                # but never mind
                break
            if arg == u'-c':
                argv[0] = u'-c'
                break

    if argv == []:
        argv = [u'']
