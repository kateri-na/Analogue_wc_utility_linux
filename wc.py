#!/usr/bin/env python3
import sys
from typing import List
from enum import Enum
from enum import auto
import re


class CommandLineOption(Enum):
    LINES = auto(),
    BYTES = auto(),
    CHARS = auto(),
    WORDS = auto(),
    MAX_LINE_LENGTH = auto()


def map_letter(arg: str) -> CommandLineOption:
    match arg:
        case 'l':
            return CommandLineOption.LINES
        case 'c':
            return CommandLineOption.BYTES
        case 'm':
            return CommandLineOption.CHARS
        case 'w':
            return CommandLineOption.WORDS
        case 'L':
            return CommandLineOption.MAX_LINE_LENGTH


def parse_cmdargs(args: List[str]) -> List[CommandLineOption]:
    cmd_opts: List[CommandLineOption] = []

    for arg in args:
        match arg:  # pattern matching
            case '--lines' | '-l':
                cmd_opts.append(CommandLineOption.LINES)
            case '--bytes' | '-c':
                cmd_opts.append(CommandLineOption.BYTES)
            case '--chars' | '-m':
                cmd_opts.append(CommandLineOption.CHARS)
            case '--words' | '-w':
                cmd_opts.append(CommandLineOption.WORDS)
            case '--max-line-length' | '-L':
                cmd_opts.append(CommandLineOption.MAX_LINE_LENGTH)
            case arg if arg.startswith('-') and len(arg) > 2:
                for letter in arg.replace('-', ''):
                    cmd_opts.append(map_letter(letter))
            case _:
                print(f"Invalid option {arg}")

    return cmd_opts


def exec(filename: str, options: List[CommandLineOption]) -> str:
    # deduplicate elements
    opts_set = set(options)
    result_str = ""

    for option in opts_set:
        match option:
            case CommandLineOption.LINES:
                result_str += ' ' + str(count_lines(filename))
            case CommandLineOption.BYTES:
                result_str += ' ' + str(count_bytes(filename))
            case CommandLineOption.CHARS:
                result_str += ' ' + str(count_chars(filename))
            case CommandLineOption.WORDS:
                result_str += ' ' + str(count_words(filename))
            case CommandLineOption.MAX_LINE_LENGTH:
                result_str += ' ' + str(count_max_line_length(filename))

    return result_str + ' ' + filename


def print_help() -> None:
    print("""This script releases following functions with input file:
    --lines, -l            print the newline counts 
    --bytes, -c            print the bytes counts
    --chars, -m            print the character counts
    --words, -w            print the word counts
    --max-line-length, -L  print the maximum display width
    --help                 display this help
    --version              output version information
    """)


def print_version() -> None:
    print("""
    analogue of wc 8.32
    
    written by Ekaterina Panina
    """)


def main(args: List[str]) -> None:
    cmdline_args = args[1:]  # slice

    match cmdline_args:
        case []:
            print_help()
        case ['--help']:
            print_help()
        case ['--version']:
            print_version()
        case [filename]:
            print(exec(filename, [CommandLineOption.LINES, CommandLineOption.WORDS, CommandLineOption.BYTES]))
        case arguments:
            arguments.reverse()
            [filename, *rest] = arguments
            rest.reverse()
            print(exec(filename, parse_cmdargs(rest)))


def count_lines(filename: str) -> int:
    # arm - automatic resource management
    try:
        with open(filename, 'r') as file:  # create context, in context file closes
            return file.read().count('\n')
    except:
        return 0


def count_bytes(filename: str) -> int:
    try:
        with open(filename, 'rb') as file:
            return len(file.read())
    except:
        return 0


def count_chars(filename: str) -> int:
    try:
        with open(filename, 'r') as file:
            return len(file.read())
    except:
        return 0


def count_words(filename: str) -> int:
    # regular expressions
    pattern = "\S+" # not white spaces
    try:
        with open(filename, 'r') as file:
            text = file.read()
            occurrences = re.findall(pattern, text)
            return len(occurrences)
    except:
        return 0


def count_max_line_length(filename: str) -> int:
    max_line = 0
    try:
        with open(filename, 'r') as file:
            for line in file.readlines():
                curr_line_len = len(line.replace('\n', ''))
                if curr_line_len > max_line:
                    max_line = curr_line_len
        return max_line
    except:
        return max_line


if __name__ == '__main__':  # Dunder or magic methods
    main(sys.argv)
