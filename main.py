from lexer       import Lexer
from parser      import Parser
from interpreter import Interpreter
import colorama
import sys

def error(msg):
    print(colorama.Fore.RED+msg.strip()+colorama.Style.RESET_ALL)

def main():
    args = sys.argv
    _ = args.pop(0)
    if len(args) < 1:
        error("""
        Usage: hodl [OPTIONS] file_path
Short description of what the program does.
Options:
    -h, --help | Show this help message and exit
        """.strip())
        sys.exit(1)
    file_name = args.pop(0)
    run_program(file_name)


def run_program(file_name):
    try:
        with open(file_name, "r") as f:
            input_code = f.read()
            lexer       = Lexer(input_code)
            parser      = Parser(lexer)
            interpreter = Interpreter(parser)
            interpreter.interpret()

    except FileNotFoundError:
        error(f"File Not Found {file_name}")

    except KeyboardInterrupt:
        error(f"Closing ...")

if __name__ == "__main__":
    main()

