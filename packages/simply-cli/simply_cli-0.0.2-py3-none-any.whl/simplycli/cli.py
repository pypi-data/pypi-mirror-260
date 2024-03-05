import inspect
import re
import abc
from typing import Union, Callable, TypeAlias
from .arg import ArgMatcher


class AbstractFunctionCommandWrapper(abc.ABC):
    """
    A niche class that must be used on function wrapper classes, or more specifically, classes that can be invoked
    via teh __call__ method.
    """
    @abc.abstractmethod
    def signature(self) -> Callable:
        """
        Returns the base callable associated with this class.
        :return: The base callable
        """
        raise NotImplementedError

    @abc.abstractmethod
    def invoke(self, *args, **kwargs):
        """
        Invokes this wrapper with the given arguments.
        :param args: Invocation arguments.
        :param kwargs: Invocation keyword arguments.
        :return: The result of the function invocation.
        """
        raise NotImplementedError

    def __getattribute__(self, item):
        if item == "__name__":
            return self.signature().__name__
        return super().__getattribute__(item)

    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)


class AbstractCommandClass(abc.ABC):
    """
    Provides a template class for use with :func:`@CLI.command <CLI.command>`, however, classes do not need to inherit this class
    to be an eligible command-class. They simply just need to implement the __execute__ method.
    """
    @abc.abstractmethod
    def __execute__(self, *args):
        raise NotImplementedError


CommandLike: TypeAlias = Union[Callable, AbstractCommandClass]


class Command:
    def __init__(self, name: str, command_like: CommandLike,
                 /, aliases: list[str] = None, force_lower: bool = True, case_sensitive: bool = False):
        self.command_like = command_like
        if isinstance(command_like, AbstractFunctionCommandWrapper):
            self.is_class = False
            self.__wrapped_command__ = True
        else:
            self.is_class = inspect.isclass(command_like)
            self.__wrapped_command__ = False

        self.name = name
        self.aliases = aliases
        self._aliases = list(aliases)
        self._aliases.insert(0, self.name)

        self.force_lower = force_lower
        self.case_sensitive = case_sensitive

        self.__subcommands__: set[Command] = set()
        self._parent = None

        self._command_like_instance = None

        self._arg_matcher = ArgMatcher(self)

    def execute(self, raw_input: str):
        space = re.match("\\s+", raw_input)
        if space:
            subcommand_name = raw_input[:space.start()]
            sub_raw_input = raw_input[space.end():]

            for subcommand in self.__subcommands__:
                if subcommand.matches(subcommand_name):
                    return subcommand.execute(sub_raw_input)

        args = self._arg_matcher.match_arguments(raw_input)
        if self.is_class:
            self.command_like.__execute__(*args)
        else:
            self.command_like(*args)

    def add_subcommand(self, subcommand: "Command"):
        self.__subcommands__.add(subcommand)
        subcommand.__parent__ = self

    def find_subcommand(self, parent: Union[str, CommandLike]) -> "Command":
        for subcommand in self.__subcommands__:
            if parent is str and subcommand.matches(parent):
                return subcommand
            elif subcommand.command_like is parent:
                return subcommand
            return subcommand.find_subcommand(parent)
        return None

    def get_instance(self):
        if self._command_like_instance is None:
            self._command_like_instance = self.command_like()
        return self._command_like_instance

    def get_parent(self) -> "Command":
        return self._parent

    def matches(self, cmd_name: str) -> bool:
        for alias in self._aliases:
            if self.force_lower:
                alias = alias.lower()
            if self.case_sensitive and cmd_name == alias:
                return True
            if cmd_name.lower() == alias:
                return True
        return False

def complex_decorator(**decorator_flags):
    def inner(outer, *_):
        def real_decorator(cli, *args, **kwargs):
            executed = None
            args = list(args)

            if len(args) != 0:
                executed = args[0]
                args = args[1:]

            args.insert(0, cli)

            def wrapper(f):
                run_args = list(args)

                run_args.insert(1, f)
                if decorator_flags.get("no_wrap") and executed:
                    run_args.insert(2, executed)

                res = outer(*run_args, **kwargs)
                return res

            if executed and decorator_flags.get("no_wrap") is False:
                return wrapper(executed)
            return wrapper
        return real_decorator
    return inner

class CLI:
    def __init__(self, console_input: Callable[[], str] = input):
        self._commands: set[Command] = set()
        self._command_table: dict[CommandLike, Command] = dict()
        self.console_input = console_input

    @complex_decorator(no_wrap=False)
    def command(self, command_like,
                aliases: list[str] = None, lowercase: bool = True, case_sensitive: bool = True):
        """
        A decorator that registers a command-like object as a command, allowing it to be executed when matched in
        an input string.

        If no aliases are specified the name of the command will match the name of the annotated class or method.

        If this decorator is used on a class, the class must contain a method named **__execute__**, this method CAN
        be static and will be executed if a command is successfully matched. Additionally, the containing class will
        operate as a singleton whenever received as a "self" parameter to __execute__, meaning updates to the class
        will persist between calls.

        Usage::

            cli = CLI()

            @cli.command
            def ping():
                print("pong")

            @cli.command(aliases=["howdy"])
            class Hello:
                @staticmethod  # this does not need to be static
                def __execute__():
                    print("Hi!")

            cli.process_input("pong")   # ping will be called
            cli.process_input("Hello")  # Hello.__execute__() will be called
            cli.process_input("howdy")  # Hello.__execute__() will be called again

        **Advanced Usage:**
        Parameters declared in the target execution method must follow special rules to correspond with a given input.
        The most simple rule is if a parameter is named "self" it will contain the singleton instance of its parent
        class.

        Additionally, each argument of a command must have a matching parameter defined in the target execution method
        which also constructs an instance of :class:`Arg` as its default value.

        The final caveat is that any matching argument supplied to the method will automatically have its type matched
        to its parameter's annotated type. When no type annotation is specified the value will either be a string or
        will match the type of the default value provided by the Arg() constructor.

        Lastly, if any parameter has the annotated type :class:`Command` then its corresponding :class:`Command`
        instance will be passed into the function upon execution.

        Advanced Usage Examples::

            cli = CLI()

            # registers a command that receives the first argument of the 'greeting' command
            @cli.command
            def greet(name: str = Arg(0)):
                print(f"Hello {name}!")

            # registers a command that takes two optional arguments (--value and --hide)
            @cli.command
            def echo(value: str = Arg("--value", default="nothing..."), hide: bool = Arg("--hide"))
                if not hide: print("Echoed " + value)

            cli.process_input("greet Alice")                # prints "Hello Alice!"
            cli.process_input("echo")                       # prints "Echoed nothing..."
            cli.process_input("echo --value text")          # prints "Echoed text"
            cli.process_input("echo --value text --hide)    # prints nothing!

        :param command_like: The command-like object to register
        :param aliases: The aliases the command can also be invoked under
        :param lowercase: If the command name should be lowercase (defaults to True)
        :param case_sensitive: If the command name is case-sensitive (defaults to True)
        :return: The wrapped function
        """
        return self._register_command(command_like, None, aliases, lowercase, case_sensitive)

    @complex_decorator(no_wrap=True)
    def subcommand(self, command_like, parent: type = None,
                   aliases: list[str] = None, lowercase: bool = True, case_sensitive: bool = True):
        """
        A decorator that registers a command-like object as a command, allowing it to be executed when matched in
        an input string.

        This decorator is nearly identical to the :func:`command` decorator except it takes an additional argument,
        `parent` which is the class of the desired parent command.

        Usage::

            cli = CLI()

            @cli.command
            class Math:
                def __execute__():
                    print("use either math add or math subtract!")

            @cli.subcommand(Math)
            def add(o1: int = Arg(0), o2: int = Arg(1)):
                print(f"{o1} + {o2} = {o1 + o2}")

            @cli.command(Math)
            def sub(o1: int = Arg(0), o2: int = Arg(1)):
                print(f"{o1} - {o2} = {o1 - o2}")

            cli.process_input("math")           # prints "use either math add or math subtract!"
            cli.process_input("math add 5 4)    # prints "5 + 4 = 9"
            cli.process_input("math sub 8 3)    # prints "8 - 3 = 5"


        :param command_like: The command-like object to register.
        :param parent: The class of the parent command.
        :param aliases: The aliases the command can also be invoked under.
        :param lowercase: If the command name should be lowercase (defaults to True).
        :param case_sensitive: If the command name is case-sensitive (defaults to True).
        :return: The wrapped function
        """
        if parent is None:
            raise ValueError("parent cannot be None")
        return self._register_command(command_like, parent, aliases, lowercase, case_sensitive)

    def identity(self, func):
        """
        A decorator that **modifies a method** to return an instance to its correspond :class:`Command` class.
        :param func: The function to modify
        :return: A modified function that returns a :class:`Command` instance.
        """
        parent_class = func.__qualname__.split(".")[-2]

        def wrapper(*_):
            return self._find_command(parent_class)

        return wrapper

    def process(self) -> str:
        """
        A function that immediately prompts for user input then processes the input,
        invoking any matching registered commands.

        :return: The resulting user input
        """
        return self.process_input(self.console_input())

    def process_input(self, raw_input: str) -> str:
        """
        A function that processes an input string, invoking any matching registered commands.

        :param raw_input: The string to process.
        :return: The input string.
        """
        original_input = raw_input
        space = re.match("\\s+", raw_input)
        if not space:
            command_name = raw_input
        else:
            command_name = raw_input[:space.start()]
            raw_input = raw_input[space.end() + 1:]

        commands = list(self._commands)
        for cmd in commands:
            if cmd.matches(command_name):
                cmd.execute(raw_input)

        return original_input

    def unregister(self, command_like: CommandLike):
        """
        Unregisters a command or subcommand via its registered command-like object.

        :param command_like: The command-like object to unregister.
        """
        matched = [cmd for cmd in self._commands if cmd.command_like == command_like]
        for match in matched:
            self._commands.remove(match)
        table_entry = self._command_table.get(command_like)
        if table_entry:
            parent = table_entry.get_parent()
            if parent:
                parent.__subcommands__.remove(table_entry)


    def _find_command(self, name) -> Command:
        for command in self._commands:
            if name is str and command.matches(name):
                return command
            elif command.command_like is name:
                return command

            subcommand = command.find_subcommand(name)
            if subcommand:
                return subcommand

    def _register_command(self, command_like, parent: type = None, aliases: list[str] = None, exact_name: bool = False, case_sensitive: bool = True):
        cmd_name: str = command_like.__name__

        kwargs = {"exact_name": exact_name, "case_sensitive": case_sensitive}

        aliases = [] if aliases is None else list(aliases)

        cmd = Command(cmd_name, aliases, command_like, kwargs)
        if parent is not None:
            command_parent = self._find_command(parent)
            if command_parent:
                command_parent.add_subcommand(cmd)
                return command_like
            else:
                raise ValueError(f"Parent not found {parent}")

        self._commands.add(cmd)
        self._command_table[command_like] = cmd
        return command_like
