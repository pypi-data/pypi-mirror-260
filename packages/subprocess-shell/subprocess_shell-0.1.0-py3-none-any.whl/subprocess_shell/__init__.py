import asyncio
import asyncio.subprocess as a_subprocess
import datetime
import io
import itertools
import os
import pathlib
import queue
import re
import selectors
import subprocess
import sys
import threading
import types
import typing


__all__ = ("start", "write", "wait", "read", "run")


def _or(first_dictionary, second_dictionary):
    dictionary = dict(first_dictionary)
    dictionary.update(second_dictionary)
    return dictionary


_FORCE_ASYNC = False
_BUFFER_SIZE = int(1e6)


def _read_streams():
    selector = typing.cast(selectors.BaseSelector, _selector)
    while True:
        for key, _ in selector.select():
            while True:
                object = typing.cast(typing.IO, key.fileobj).read(_BUFFER_SIZE)
                if object in (None, b"", ""):
                    break

                key.data(object)

            if object in (b"", ""):
                selector.unregister(key.fileobj)
                key.data(None)


_selector = None
_selector_lock = threading.Lock()


def _async(coroutine):
    global _event_loop

    if _event_loop is None:
        with _event_loop_lock:
            if _event_loop is None:
                _event_loop = asyncio.new_event_loop()
                threading.Thread(target=_event_loop.run_forever, daemon=True).start()

    return asyncio.run_coroutine_threadsafe(coroutine, _event_loop)


_event_loop = None
_event_loop_lock = threading.Lock()


class _Start:
    def __init__(
        self,
        stdin: typing.Union[None, int, typing.IO] = subprocess.PIPE,
        stdout: typing.Union[
            None,
            int,
            typing.IO,
            str,
            pathlib.Path,
            typing.Callable[[typing.AnyStr], typing.Any],
        ] = subprocess.PIPE,
        pass_stdout: bool = False,
        stderr: typing.Union[
            None,
            int,
            typing.IO,
            str,
            pathlib.Path,
            typing.Callable[[typing.AnyStr], typing.Any],
        ] = subprocess.PIPE,
        pass_stderr: bool = False,
        queue_size: int = 0,
        logs: bool = False,
        return_codes: typing.Union[typing.Container[int], None] = (0,),
        force_color: bool = True,
        async_: bool = False,
        **kwargs,
    ):
        """
        `{arguments} >> start(...)` starts a sub process similar to `subprocess.Popen({arguments}, ...)` and returns a process object

        `{process} + {arguments} >> start(...)` passes stdout of the left process to stdin of the right.
        May require `{process} = {arguments} >> start(pass_stdout=True, ...)`.

        `{process} - {arguments} >> start(...)` passes stderr of the left process to stdin of the right.
        May require `{process} = {arguments} >> start(pass_stderr=True, ...)`.

        Parameters
        ----------
        stdin : None | int | IO
            See `subprocess.Popen`
        stdout : None | int | IO | str | pathlib.Path | (str | bytes) -> any
            if      None | int | IO : see `subprocess.Popen`
            if   str | pathlib.Path : write to file at path
            if (str | bytes) -> any : call function for each chunk
                called in a different thread
                **!! must not raise exceptions !!**
        pass_stdout : bool
            Don't touch stdout
        stderr : None | int | IO | str | pathlib.Path | (str | bytes) -> any
            if      None | int | IO : see `subprocess.Popen`
            if   str | pathlib.Path : write to file at path
            if (str | bytes) -> any : call function for each chunk
                called in a different thread
                **!! must not raise exceptions !!**
        pass_stderr : bool
            Don't touch stderr
        queue_size : int
            Limit size of queues
            *! may lead to deadlocks !*
        logs : bool
            Write stderr first if in a chain
        return_codes : container[int] | None
            Used to validate the return code if in a chain
        force_color : bool
            Set environment variable FORCE_COLOR to 1 if not set
        async_ : bool
            Use `asyncio` instead of `selectors`
        **kwargs
            Passed to `subprocess.Popen`
        """

        super().__init__()

        self.stdin = stdin
        self.stdout = stdout
        self.pass_stdout = pass_stdout
        self.stderr = stderr
        self.pass_stderr = pass_stderr
        self.queue_size = queue_size
        self.logs = logs
        self.return_codes = return_codes
        self.force_color = force_color
        self.async_ = async_
        self.kwargs = kwargs

        assert not (pass_stdout and stdout not in (None, subprocess.PIPE))
        assert not (pass_stderr and stderr not in (None, subprocess.PIPE))

    def __rrshift__(self, object: typing.Union[typing.Iterable, "_Pass"]) -> "_Process":
        return _Process(object, self)

    def __add__(
        self, arguments: typing.Iterable
    ) -> "_PassStdout":  # `{arguments} >> start() + {arguments}`
        return _PassStdout(self, arguments)

    def __sub__(
        self, arguments: typing.Iterable
    ) -> "_PassStderr":  # `{arguments} >> start() - {arguments}`
        return _PassStderr(self, arguments)


start = _Start


class _Process:
    def __init__(self, object, start):
        super().__init__()

        self.object = object
        self.start = start

        if isinstance(object, _Pass):
            assert start.stdin in (None, subprocess.PIPE)

            self._source_process = object.process

            arguments = object.arguments
            stdin, stdin_is_target = (
                (
                    (object.process._process.stderr, False)
                    if object.process._stderr_target is None
                    else (object.process._stderr_target, True)
                )
                if object.stderr
                else (
                    (object.process._process.stdout, False)
                    if object.process._stdout_target is None
                    else (object.process._stdout_target, True)
                )
            )

        else:
            self._source_process = None

            arguments = object
            stdin = start.stdin
            stdin_is_target = False

        self._async = start.async_ or os.name == "nt" or _FORCE_ASYNC
        self._arguments = list(map(str, arguments))

        _v_ = self._get_argument(start.stdout, start.pass_stdout)
        self._stdout, self._stdout_target = _v_

        _v_ = self._get_argument(start.stderr, start.pass_stderr)
        self._stderr, self._stderr_target = _v_

        kwargs: dict = dict(
            stdin=stdin, stdout=self._stdout, stderr=self._stderr, **start.kwargs
        )

        if start.force_color:
            env = kwargs.get("env")
            if env is None:
                env = os.environ

            if "FORCE_COLOR" not in env:
                kwargs["env"] = _or(env, {"FORCE_COLOR": "1"})

        if self._async:
            bufsize = kwargs.pop("bufsize", None)
            if bufsize is not None:
                kwargs["limit"] = bufsize  # TODO correct?

        self._start_datetime = datetime.datetime.now()
        self._process = (
            _async(
                a_subprocess.create_subprocess_exec(*self._arguments, **kwargs)
            ).result()
            if self._async
            else subprocess.Popen(self._arguments, **kwargs)
        )
        self._stdout_queue = (
            None
            if self._process.stdout is None or start.pass_stdout
            else self._initialize_stream(self._process.stdout, start.stdout, start)
        )
        self._stderr_queue = (
            None
            if self._process.stderr is None or start.pass_stderr
            else self._initialize_stream(self._process.stderr, start.stderr, start)
        )

        _v_ = not stdin_is_target and self._stdout_target is None
        if not (_v_ and self._stderr_target is None):

            async def _close_pipes():
                await typing.cast(a_subprocess.Process, self._process).wait()

                if stdin_is_target:
                    os.close(stdin)

                if self._stdout_target is not None:
                    os.close(typing.cast(int, self._stdout))

                if self._stderr_target is not None:
                    os.close(typing.cast(int, self._stderr))

            _async(_close_pipes())

    def _get_argument(self, object, pass_):
        # match object:
        # case str() | pathlib.Path():
        if isinstance(object, (str, pathlib.Path)):
            return (open(object, "wb"), None)

        # case c_abc.Callable():
        if isinstance(object, typing.Callable):
            return (subprocess.PIPE, None)

        if self._async and pass_:
            target, source = os.pipe()
            return (source, target)

        return (object, None)

    def _initialize_stream(self, stream, start_argument, start):
        global _selector

        if isinstance(start_argument, typing.Callable):
            queue_ = None
            function = start_argument

        else:
            queue_ = queue.Queue(maxsize=start.queue_size)
            function = queue_.put

        if self._async:

            async def _read_pipe():
                while True:
                    object = await stream.read(n=_BUFFER_SIZE)
                    if len(object) == 0:
                        function(None)
                        break

                    function(object)

            _async(_read_pipe())

        else:
            os.set_blocking(stream.fileno(), False)

            if _selector is None:
                with _selector_lock:
                    if _selector is None:
                        _selector = selectors.DefaultSelector()
                        threading.Thread(target=_read_streams, daemon=True).start()

            _selector.register(stream, selectors.EVENT_READ, data=function)

        return queue_

    def get_stdout_lines(
        self, bytes: bool = False
    ) -> typing.Generator[typing.AnyStr, None, None]:
        """
        Yields lines as strings or bytes objects similar to `iter(subprocess.Popen(...).stdout)`

        Parameters
        ----------
        bytes : bool
            Yield bytes objects instead of strings

        Returns
        -------
        generator[str] | generator[bytes]
            Lines as strings or bytes objects
        """
        _v_ = self._get_lines(self._stdout_queue, bytes)
        return typing.cast(typing.Generator[typing.AnyStr, None, None], _v_)

    def get_stderr_lines(
        self, bytes: bool = False
    ) -> typing.Generator[typing.AnyStr, None, None]:
        """
        Yields lines as strings or bytes objects similar to `iter(subprocess.Popen(...).stderr)`

        Parameters
        ----------
        bytes : bool
            Yield bytes objects instead of strings

        Returns
        -------
        generator[str] | generator[bytes]
            Lines as strings or bytes objects
        """
        _v_ = self._get_lines(self._stderr_queue, bytes)
        return typing.cast(typing.Generator[typing.AnyStr, None, None], _v_)

    def _get_lines(self, queue, bytes):
        line_generator = _LineGenerator(bytes)

        for object in self._get_bytes(queue) if bytes else self._get_strings(queue):
            yield from line_generator.append(object)

        yield from line_generator.append(None)

    def get_stdout_strings(self) -> typing.Generator[str, None, None]:
        """
        Yields chunks as strings

        Returns
        -------
        generator[str]
            Chunks as strings
        """
        return self._get_strings(self._stdout_queue)

    def get_stderr_strings(self) -> typing.Generator[str, None, None]:
        """
        Yields chunks as strings

        Returns
        -------
        generator[str]
            Chunks as strings
        """
        return self._get_strings(self._stderr_queue)

    def _get_strings(self, queue):
        objects = iter(self._get_objects(queue))

        object = next(objects, None)
        if object is None:
            return

        if isinstance(object, str):
            yield object
            yield from objects

        else:
            previous_bytes = b""
            for bytes in itertools.chain([object], objects):
                bytes = previous_bytes + bytes
                try:
                    string = bytes.decode()

                except UnicodeDecodeError as decode_error:
                    for start_index in range(4):
                        for stop_index in (None, -1, -2, -3):
                            try:
                                bytes[start_index:stop_index].decode()

                            except UnicodeDecodeError:
                                pass

                            else:
                                break
                        else:
                            raise decode_error

                    previous_bytes = bytes

                else:
                    previous_bytes = b""
                    yield string

            if previous_bytes != b"":
                yield previous_bytes.decode()

    def get_stdout_bytes(self) -> typing.Generator[bytes, None, None]:
        """
        Yields chunks as bytes objects

        Returns
        -------
        generator[bytes]
            Chunks as bytes objects
        """
        return self._get_bytes(self._stdout_queue)

    def get_stderr_bytes(self) -> typing.Generator[bytes, None, None]:
        """
        Yields chunks as bytes objects

        Returns
        -------
        generator[bytes]
            Chunks as bytes objects
        """
        return self._get_bytes(self._stderr_queue)

    def _get_bytes(self, queue):
        objects = iter(self._get_objects(queue))

        object = next(objects, None)
        if object is None:
            return

        if isinstance(object, str):
            yield object.encode()
            yield from (string.encode() for string in objects)

        else:
            yield object
            yield from objects

    def get_stdout_objects(self) -> typing.Generator[typing.AnyStr, None, None]:
        """
        Yields chunks as strings or bytes objects

        Returns
        -------
        generator[str] | generator[bytes]
            Chunks as strings or bytes objects
        """
        return self._get_objects(self._stdout_queue)

    def get_stderr_objects(self) -> typing.Generator[typing.AnyStr, None, None]:
        """
        Yields chunks as strings or bytes objects

        Returns
        -------
        generator[str] | generator[bytes]
            Chunks as strings or bytes objects
        """
        return self._get_objects(self._stderr_queue)

    def _get_objects(self, queue):
        assert queue is not None

        while True:
            object = queue.get()
            if object is None:
                queue.put(None)
                break

            yield object

    def __add__(self, arguments: typing.Iterable) -> "_Pass":
        assert self.start.pass_stdout
        return _Pass(self, False, arguments)

    def __sub__(self, arguments: typing.Iterable) -> "_Pass":
        assert self.start.pass_stderr
        return _Pass(self, True, arguments)

    def get_subprocess(self) -> typing.Union[subprocess.Popen, a_subprocess.Process]:
        """
        Returns the `subprocess.Popen` or `asyncio.subprocess.Process` object

        You shouldn't need to use this unless for complex use cases.
        If you found a common use case that should be covered by *subprocess_shell*, please let me know!

        Returns
        -------
        subprocess.Popen | asyncio.subprocess.Process
            The `subprocess.Popen` or `asyncio.subprocess.Process` object
        """
        return self._process

    def get_source_process(self) -> typing.Union["_Process", None]:
        """
        Returns the source process if in a chain

        Returns
        -------
        _Process | None
            The source process
        """
        return self._source_process

    def get_chain_string(self) -> str:
        """
        Returns a readable string representing the process and the source process

        Returns
        -------
        str
            A readable string
        """
        if self._source_process is None:
            pass_string = ""

        else:
            operator_string = "-" if self.object.stderr else "+"

            _v_ = f"{self._source_process.get_chain_string()} {operator_string} "
            pass_string = _v_

        return f"{pass_string}{str(self)}"

    def _close_stdin(self):
        if self._process.stdin is None:
            return

        typing.cast(typing.IO, self._process.stdin).close()
        if self._async:
            _async(typing.cast(asyncio.StreamWriter, self._process.stdin).wait_closed())

    def _wait(self):
        return (
            _async(self._process.wait()).result()
            if self._async
            else self._process.wait()
        )

    def __str__(self):
        if not self._async:
            self._process.poll()

        _v_ = self._process.returncode is None
        code_string = "running" if _v_ else f"returned {self._process.returncode}"

        _v_ = subprocess.list2cmdline(typing.cast(typing.Iterable, self._arguments))
        return f"{self._start_datetime} `{_v_}` {code_string}"


class _Pass:
    def __init__(self, process, stderr, arguments):
        super().__init__()

        self.process = process
        self.stderr = stderr
        self.arguments = arguments


class _Write:
    def __init__(self, object: typing.AnyStr, close: bool = False):
        """
        `{process} >> write(...)` writes to, flushes and optionally closes stdin and returns the process object

        similar to
        ```python
        stdin = subprocess.Popen(...).stdin
        stdin.write(object)
        stdin.flush()
        if close:
            stdin.close()
        ```

        Parameters
        ----------
        object : str | bytes
            String or bytes object to write
        close : bool
            Close stdin after write
        """

        super().__init__()

        self.object = object
        self.close = close

    def __rrshift__(self, process: _Process) -> _Process:
        stdin = typing.cast(typing.IO, process._process.stdin)
        assert stdin is not None

        if isinstance(stdin, io.TextIOBase):
            _v_ = self.object if isinstance(self.object, str) else self.object.decode()
            stdin.write(_v_)

        else:
            _v_ = self.object.encode() if isinstance(self.object, str) else self.object
            stdin.write(_v_)

        (
            _async(typing.cast(asyncio.StreamWriter, stdin).drain()).result()
            if process._async
            else stdin.flush()
        )

        if self.close:
            process._close_stdin()

        return process

    def __add__(
        self, arguments: typing.Iterable
    ) -> "_PassStdout":  # `{process} >> write({string or bytes}) + {arguments}`
        return _PassStdout(self, arguments)

    def __sub__(
        self, arguments: typing.Iterable
    ) -> "_PassStderr":  # `{process} >> write({string or bytes}) - {arguments}`
        return _PassStderr(self, arguments)


write = _Write


class _PassStdout:
    def __init__(self, right_object, target_arguments):
        super().__init__()

        self.right_object = right_object
        self.target_arguments = target_arguments

        if isinstance(right_object, _Start):
            assert right_object.stdout in (None, subprocess.PIPE)
            right_object.pass_stdout = True

        elif isinstance(right_object, _Process):
            assert right_object.start.pass_stdout

        else:
            raise Exception

    def __rrshift__(
        self, left_object: typing.Union[typing.Iterable, _Process]
    ) -> _Pass:
        # `{arguments} >> start() + {arguments}`
        # `{process} >> write() + {arguments}`
        return (left_object >> self.right_object) + self.target_arguments


class _PassStderr:
    def __init__(self, right_object, target_arguments):
        super().__init__()

        self.right_object = right_object
        self.target_arguments = target_arguments

        if isinstance(right_object, _Start):
            assert right_object.stderr in (None, subprocess.PIPE)
            right_object.pass_stderr = True

        elif isinstance(right_object, _Process):
            assert right_object.start.pass_stderr

        else:
            raise Exception

    def __rrshift__(
        self, left_object: typing.Union[typing.Iterable, _Process]
    ) -> _Pass:
        # `{arguments} >> start() - {arguments}`
        # `{process} >> write() + {arguments}`
        return (left_object >> self.right_object) - self.target_arguments


class _Wait:
    def __init__(
        self,
        stdout: typing.Union[bool, typing.TextIO] = True,
        stderr: typing.Union[bool, typing.TextIO] = True,
        logs: bool = False,
        return_codes: typing.Union[typing.Container[int], None] = (0,),
        rich: bool = True,
        stdout_color: str = "green",
        stderr_color: str = "red",
        log_color: str = "dark_orange3",
        ascii: bool = False,
    ):
        """
        `{process} >> wait(...)` "waits for" the source process, writes stdout and stderr as separate frames and validates and returns the return code

        Parameters
        ----------
        stdout : bool | TextIO
            if   bool : optionally write stdout to `sys.stdout`
            if TextIO : write stdout to writable object
        stderr : bool | TextIO
            if   bool : optionally write stderr to `sys.stderr`
            if TextIO : write stderr to writable object
        logs : bool
            Write stderr first
        return_codes : container[int]
            Used to validate the return code
        rich : bool
            Use *Rich* if available
        ascii : bool
            Use ASCII instead of Unicode
        """

        super().__init__()

        self.stdout = stdout
        self.stderr = stderr
        self.logs = logs
        self.return_codes = return_codes
        self.rich = rich
        self.stdout_color = stdout_color
        self.stderr_color = stderr_color
        self.log_color = log_color
        self.ascii = ascii

        self._r_console = None
        self._r_highlighter = None
        self._r_theme = None
        if rich:
            try:
                import rich.console as r_console
                import rich.highlighter as r_highlighter
                import rich.theme as r_theme

            except ModuleNotFoundError:
                pass

            else:
                self._r_console = r_console
                self._r_highlighter = r_highlighter
                self._r_theme = r_theme

    def __rrshift__(self, process: _Process) -> int:
        if process._source_process is not None:
            kwargs = dict(logs=process._source_process.start.logs)
            if self.stdout not in (False, True):
                kwargs["stdout"] = self.stdout
            if self.stderr not in (False, True):
                kwargs["stderr"] = self.stderr

            try:
                _v_ = process._source_process.start.return_codes
                _ = process._source_process >> _Wait(return_codes=_v_, **kwargs)

            except ProcessFailedError:
                raise ProcessFailedError(process)

        process._close_stdin()

        def _print_stdout():
            _v_ = process._stdout_queue is None or process.start.pass_stdout
            if not (_v_ or self.stdout is False):
                _v_ = sys.stdout if self.stdout is True else self.stdout
                self._print_stream(process.get_stdout_strings(), _v_, False, process)

        def _print_stderr():
            _v_ = process._stderr_queue is None or process.start.pass_stderr
            if not (_v_ or self.stderr is False):
                _v_ = sys.stderr if self.stderr is True else self.stderr
                self._print_stream(process.get_stderr_strings(), _v_, True, process)

        if self.logs:
            _print_stderr()
            _print_stdout()

        else:
            _print_stdout()
            _print_stderr()

        return_code = process._wait()

        if isinstance(process.start.stdout, (str, pathlib.Path)):
            typing.cast(typing.IO, process._stdout).close()

        if isinstance(process.start.stderr, (str, pathlib.Path)):
            typing.cast(typing.IO, process._stderr).close()

        if self.return_codes is not None and return_code not in self.return_codes:
            raise ProcessFailedError(process)

        return return_code

    def _print_stream(self, strings, file, is_stderr, process):
        strings = iter(strings)

        string = next(strings, None)
        if string is None:
            return

        newline_string = (
            ("\nE " if self.ascii else "\n┣ ")
            if is_stderr
            else ("\n| " if self.ascii else "\n│ ")
        )
        newline = False

        if self._r_console is None:

            def _print(*args, **kwargs):
                print(*args, file=file, flush=True, **kwargs)

        else:
            _v_ = typing.cast(types.ModuleType, self._r_highlighter).RegexHighlighter

            class _Highlighter(_v_):
                base_style = "m."

                _v_ = f"(?P<p1>{re.escape(newline_string)})"
                highlights = [r"^(?P<p1>[^`]*`).*(?P<p2>` (running|returned ))", _v_]

            color_name = (
                (self.log_color if self.logs else self.stderr_color)
                if is_stderr
                else self.stdout_color
            )

            _v_ = typing.cast(types.ModuleType, self._r_theme)
            _v_ = _v_.Theme({"m.p1": color_name, "m.p2": color_name})
            console = typing.cast(types.ModuleType, self._r_console).Console(
                file=file, soft_wrap=True, highlighter=_Highlighter(), theme=_v_
            )

            def _print(*args, **kwargs):
                console.out(*args, **kwargs)
                file.flush()

        corner_string = (
            ("EE" if self.ascii else "┏━")
            if is_stderr
            else ("+-" if self.ascii else "╭─")
        )
        _print(f"{corner_string} {process}{newline_string}", end="")

        if string.endswith("\n") and not self.ascii:
            string = string[:-1]
            newline = True

        _print(string.replace("\n", newline_string), end="")

        for string in strings:
            if newline:
                _print(newline_string, end="")
                newline = False

            if string.endswith("\n") and not self.ascii:
                string = string[:-1]
                newline = True

            _print(string.replace("\n", newline_string), end="")

        _print("␄" if not newline and not self.ascii else "")

        process._wait()

        corner_string = (
            (f"EE" if self.ascii else "┗━")
            if is_stderr
            else ("+-" if self.ascii else "╰─")
        )
        footer_string = f"{corner_string} {process}"

        _print(footer_string)


class ProcessFailedError(Exception):
    def __init__(self, process: _Process):
        super().__init__(process)

        self.process = process

    def __str__(self):
        return self.process.get_chain_string()


wait = _Wait


class _Read:
    def __init__(
        self,
        stdout: typing.Union[bool, typing.TextIO] = True,
        stderr: typing.Union[bool, typing.TextIO] = False,
        bytes: bool = False,
        return_codes: typing.Union[typing.Container[int], None] = (0,),
    ):
        """
        `{process} >> read(...)` "waits for" the process, concatenates the chunks from stdout and optionally stderr and returns the result

        `{process} >> read(stdout=True, stderr=True, ...)` returns the tuple (result from stdout, result from stderr).

        Parameters
        ----------
        stdout : bool | TextIO
            if  False : don't touch stdout
            if   True : concatenate and return stdout
            if TextIO : passed to `wait`
        stderr : bool | TextIO
            if  False : don't touch stderr
            if   True : concatenate and return stderr
            if TextIO : passed to `wait`
        bytes : bool
            Return bytes objects instead of strings
        return_codes : collection[int]
            Passed to `wait`
        """

        super().__init__()

        self.stdout = stdout
        self.stderr = stderr
        self.bytes = bytes
        self.return_codes = return_codes

    def __rrshift__(
        self, process: _Process
    ) -> typing.Union[
        str,
        bytes,
        typing.Tuple[typing.Union[str, bytes], typing.Union[str, bytes]],
        None,
    ]:
        stdout = self.stdout is True
        stderr = self.stderr is True

        _ = process >> _Wait(
            stdout=(not self.stdout) if isinstance(self.stdout, bool) else self.stdout,
            stderr=(not self.stderr) if isinstance(self.stderr, bool) else self.stderr,
            return_codes=self.return_codes,
        )

        stdout_object = (
            (
                b"".join(process.get_stdout_bytes())
                if self.bytes
                else "".join(process.get_stdout_strings())
            )
            if stdout
            else None
        )
        stderr_object = (
            (
                b"".join(process.get_stderr_bytes())
                if self.bytes
                else "".join(process.get_stderr_strings())
            )
            if stderr
            else None
        )

        if stdout and stderr:
            return typing.cast(
                typing.Tuple[typing.Union[str, bytes], typing.Union[str, bytes]],
                (stdout_object, stderr_object),
            )

        if stdout:
            return typing.cast(typing.Union[str, bytes], stdout_object)

        if stderr:
            return typing.cast(typing.Union[str, bytes], stderr_object)


read = _Read


class _Run:
    def __init__(self, *args):
        """
        `{arguments} >> run(...)` is a shortcut for `{arguments} >> start(...) {* >> write(...) *} >> {wait(...) | read(...)}`

        `{arguments} >> run()` is equivalent to `{arguments} >> start() >> wait()`.

        Parameters
        ----------
        *args
            A sequence of objects returned by `start(...)`, `write(...)`, `wait(...)` and `read(...)`
        """

        super().__init__()

        self.args = args

        self._start = None
        self._writes = []
        self._wait = None
        self._read = None

        for object in args:
            if isinstance(object, _Start):
                assert self._start is None
                self._start = object

            elif isinstance(object, _Write):
                self._writes.append(object)

            elif isinstance(object, _Wait):
                assert self._wait is None
                self._wait = object

            elif isinstance(object, _Read):
                assert self._read is None
                self._read = object

        assert not (self._wait is not None and self._read is not None)

    def __rrshift__(
        self, object: typing.Union[typing.Iterable, "_Pass"]
    ) -> typing.Union[
        int,
        str,
        bytes,
        typing.Tuple[typing.Union[str, bytes], typing.Union[str, bytes]],
        None,
    ]:
        process = object >> (_Start() if self._start is None else self._start)
        for write in self._writes:
            process = process >> write

        if self._read is not None:
            return process >> self._read

        return process >> (_Wait() if self._wait is None else self._wait)


run = _Run


class LineStream(io.IOBase):
    def __init__(
        self,
        function: typing.Callable[[typing.AnyStr], typing.Any],
        stream: typing.IO,
        bytes: bool = False,
    ):
        """
        A writable stream which passes objects on to another stream and calls a function for each line

        The motivating use case:
        ```python
        matches = False

        def function(string):
            global matches
            matches = matches or re.search(pattern, string) is not None

        process >> wait(stdout=LineStream(function, sys.stdout))
        ```

        Use `{process}.get_stdout_lines(...)` and `{process}.get_stderr_lines(...)` for more complex use cases.

        Parameters
        ----------
        function : (str) -> any | (bytes) -> any
            The function to call
        stream : IO
            A writable stream
        """

        super().__init__()

        self.function = function
        self.stream = stream
        self.bytes = bytes

        self._line_generator = _LineGenerator(bytes)

    def write(self, object):
        self.stream.write(object)

        for line_object in self._line_generator.append(object):
            self.function(line_object)

    def flush(self):
        return self.stream.flush()


class _LineGenerator:
    def __init__(self, bytes):
        super().__init__()

        self.bytes = bytes

        self._idle = True
        self._empty_object, self._newline_object = (b"", b"\n") if bytes else ("", "\n")
        self._parts = []

    def append(self, object) -> typing.Generator[typing.AnyStr, None, None]:
        assert self._idle
        self._idle = False

        if object is None:
            object = self._empty_object.join(self._parts)
            if object != self._empty_object:
                yield typing.cast(typing.AnyStr, object)
                self._parts.clear()

            self._idle = True
            return

        start_index = 0
        while True:
            end_index = object.find(self._newline_object, start_index)
            if end_index == -1:
                self._parts.append(object[start_index:])
                break

            self._parts.append(object[start_index : end_index + 1])
            yield typing.cast(typing.AnyStr, self._empty_object.join(self._parts))
            self._parts.clear()

            start_index = end_index + 1

        self._idle = True
