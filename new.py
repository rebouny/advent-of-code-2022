#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com> (credits for the template)
         Martin Schuh <development@rebouny.net> (adeptions to advent-of-code)
Purpose: Python program to write a Python program
"""

import argparse
import os
import platform
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from typing import NamedTuple


class Args(NamedTuple):
    day: int
    name: str
    email: str
    overwrite: bool


# --------------------------------------------------
def get_args() -> Args:
    """Get arguments"""

    parser = argparse.ArgumentParser(
        description='Create Python argparse program',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    defaults = get_defaults()
    username = os.getenv('USER') or 'Anonymous'
    hostname = os.getenv('HOSTNAME') or 'localhost'

    parser.add_argument('day', help='Day of program', type=int, choices=range(1, 25))

    parser.add_argument('-n',
                        '--name',
                        type=str,
                        default=defaults.get('name', username),
                        help='Name for docstring')

    parser.add_argument('-e',
                        '--email',
                        type=str,
                        default=defaults.get('email', f'{username}@{hostname}'),
                        help='Email for docstring')

    parser.add_argument('-f',
                        '--force',
                        help='Overwrite existing',
                        action='store_true')

    args = parser.parse_args()

    return Args(args.day, args.name, args.email, args.force)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    program_dir = Path(f'{args.day:02d}')
    program_dir.mkdir(exist_ok=True)
    program = program_dir / f'aoc_2022_{args.day:02d}.py'

    if os.path.isfile(program) and not args.overwrite:
        answer = input(f'"{program}" exists.  Overwrite? [yN] ')
        if not answer.lower().startswith('y'):
            sys.exit('Will not overwrite. Bye!')

    print(body(args), file=open(program, 'wt'), end='')

    if platform.system() != 'Windows':
        subprocess.run(['chmod', '+x', program], check=True)

    print(f'Done, see new script "{program}."')


# --------------------------------------------------
def body(args: Args) -> str:
    """ The program template """

    today = str(date.today())

    return f"""#!/usr/bin/env python3
    # -*- coding: utf-8 -*-

\"\"\"
Author : {args.name}{' <' + args.email + '>' if args.email else ''}
Date   : {today}
Purpose: Solves day {args.day:02d} from advent of code 2022.
\"\"\"

from typing import Final


TEST_DATA: Final = [
    ""
]


# --------------------------------------------------
def load_data(filename: str):
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.readlines()


def part_01(data) -> str:
    \"\"\"Solves part 01\"\"\"
    return ''
    

def part_02(data) -> str:
    \"\"\"solves part 02\"\"\"
    return ''


# --------------------------------------------------
def test_part_01():
    \"\"\"Tests part 01\"\"\"
    data = TEST_DATA
    assert '' == part_01(data)


def test_part_02():
    \"\"\"Tests part 02\"\"\"
    data = TEST_DATA
    assert '' == part_02(data)


# --------------------------------------------------
def main() -> None:
    \"\"\"Main wrapper.\"\"\"
    data = load_data('./input')
    print(part_01(data))
    print(part_02(data))
 

if __name__ == '__main__':
    main()
"""


# --------------------------------------------------
def get_defaults():
    """Get defaults from ~/.new.py"""

    rc = os.path.join(str(Path.home()), '.new.py')
    defaults = {}
    if os.path.isfile(rc):
        for line in open(rc):
            match = re.match('([^=]+)=([^=]+)', line)
            if match:
                key, val = map(str.strip, match.groups())
                if key and val:
                    defaults[key] = val

    return defaults


# --------------------------------------------------
if __name__ == '__main__':
    main()
