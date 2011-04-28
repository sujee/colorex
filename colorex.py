#!/usr/bin/python

#    colorex is a console tool that displays files highlighting some patterns with colors
#    Copyright (C) 2011  http://www.scopart.fr
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/gpl-3.0.txt.

__version__ = "1.2"

from optparse import OptionParser, TitledHelpFormatter
import random, sys, re, types
import sre_constants

colorcode = {'red':chr(27)+'[31m', 'green':chr(27)+'[32m', 'yellow':chr(27)+'[33m',
             'blue':chr(27)+'[34m', 'magenta':chr(27)+'[35m', 'cyan':chr(27)+'[36m',
             'bred':chr(27)+'[41m', 'bgreen':chr(27)+'[42m', 'byellow':chr(27)+'[43m',
             'bblue':chr(27)+'[44m', 'bmagenta':chr(27)+'[45m', 'bcyan':chr(27)+'[46m',
             'blink':chr(27)+'[5m', 'bold':chr(27)+'[1m',
             'reset':chr(27)+'[0m'}
ambigous_pattern = [0]


def check_pattern(options):
    for pattern_list in options.values():
        if type(pattern_list) == types.ListType:
            for pattern in pattern_list:
                for ansi_seq in colorcode.values():
                    try:
                        match_obj = re.search(pattern , ansi_seq)
                    except sre_constants.error, info:
                        sys.stderr.write("ERROR :  %s  : %s\n" % (info, pattern))
                        sys.exit(1)
                    if match_obj:
                        ambigous_pattern[0] = pattern
                        return False
    return True

def colorise(line, options):
    if options['bisounours']:
        color = random.choice(colorcode.keys())
        line = line.replace(line,  colorcode[color] + line.rstrip() + colorcode['reset'])
    else:
        for color in colorcode.keys():
            if color != 'reset':
                if options[color]:
                    for pattern in options[color]:
                        match_obj = re.search(pattern , line)
                        if match_obj:
                            line = re.sub(pattern, colorcode[color] + match_obj.group() + colorcode['reset'], line)
    return line.rstrip()

def option_parse():
    version = __version__
    description = "Display files or sdtin with pretty colors for matched patterns. if you don't specify files, stdin is used."
    epilog = """Regular expressions are interpreted, so if you want to match a '*' escape it with a backslash.
                                                                            usage examples:
                                                                            ---------------
                                                                    colorex --red '\*' foo.txt
                                                                    tail -f bar.txt | colorex --blue word --red otherword --yellow '[0-9]{3}'
                                                                    (some patterns can't be used if they match ansi escape code)"""
    usage='colorex [options] [file1] [file2] ...'
    formatter=TitledHelpFormatter(width=90, max_help_position=39)
    parser = OptionParser( prog='colorex',description=description, version=__version__, usage=usage, formatter=formatter, epilog=epilog)
    parser.add_option("-b", "--blue", action="append", dest="blue", help="display BLUE pattern in blue")
    parser.add_option("-r", "--red", action="append", dest="red", help="display RED pattern in red")
    parser.add_option("-g", "--green", action="append", dest="green", help="display GREEN pattern in green")
    parser.add_option("-y", "--yellow", action="append", dest="yellow", help="display YELLOW pattern in yellow")
    parser.add_option("-m", "--magenta", action="append", dest="magenta", help="display MAGENTA pattern in magenta")
    parser.add_option("-c", "--cyan", action="append", dest="cyan", help="display CYAN pattern in cyan")
    parser.add_option("-B", "--bblue", action="append", dest="bblue", help="display BBLUE pattern in blue background")
    parser.add_option("-R", "--bred", action="append", dest="bred", help="display BRED pattern in red background")
    parser.add_option("-G", "--bgreen", action="append", dest="bgreen", help="display BGREEN pattern in green background")
    parser.add_option("-Y", "--byellow", action="append", dest="byellow", help="display BYELLOW pattern in yellow background")
    parser.add_option("-M", "--bmagenta", action="append", dest="bmagenta", help="display BMAGENTA pattern in magenta background")
    parser.add_option("-C", "--bcyan", action="append", dest="bcyan", help="display BCYAN pattern in cyan background")
    parser.add_option("-K", "--blink", action="append", dest="blink", help="display BLINK pattern blinking (not widely supported)")
    parser.add_option("-D", "--bold", action="append", dest="bold", help="display BOLD pattern in bold")
    parser.add_option("-N", "--bisounours", action="store_true", dest="bisounours", default=False, help="display with random colors")

    return parser.parse_args()

def main():
    (options_instance, args) = option_parse()
    options = options_instance.__dict__
    
 #    if not check_pattern(options):
 #       sys.stderr.write("ERROR : ambigous pattern '%s'\n" % ambigous_pattern[0])
 #       sys.exit(1)

    try:
        if args:
            for file in args:
                try:
                    file_handle = open(file, 'r')
                    for line in file_handle:
                        print colorise(line, options)
                    file_handle.close()
                except Exception,info:
                    sys.stderr.write("ERROR : can't read file %s\n" % file)
                    sys.stderr.write(str(info) + '\n')
        else:
            while True:
                line = raw_input()
                print colorise(line, options)

    except EOFError:
        sys.stderr.write('End of Input ...\n')

    except KeyboardInterrupt:
        sys.stderr.write('KeyboardInterrupt ...')

    except Exception, info:
        sys.stderr.write("ERROR : %s\n" % info)

if __name__ == "__main__":
    main()

