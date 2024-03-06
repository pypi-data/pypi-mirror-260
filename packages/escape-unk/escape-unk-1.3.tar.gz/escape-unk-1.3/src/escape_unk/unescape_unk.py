from argparse import ArgumentParser
import logging
import regex
import sys

try:
    from .utils import setup_logging
except ImportError:
    from utils import setup_logging


# Detect escaped characters
# allow one of the brackets missing
escaped_re = regex.compile(r"\[?\[[abcdef\d]+\]\]|\[\[[abcdef\d]+\]\]?")


def unescape(match, strict=False):
    ''' Convert hex values to unicode string '''
    hexvalue = match.captures()[0].strip('[]')
    logging.debug(f"Unescaping: '{hexvalue}'")
    try:
        b = bytes.fromhex(hexvalue).decode('utf-8')
    except ValueError:
        if strict:
            # Reraise the exception in strict mode
            raise ValueError("Invalid escaped sequence." \
                             + " Translator may have copied it wrong.")
        else:
            # Return invalid hex sequences as empty value
            return ''
    return b

def main():
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    parser.add_argument('-s','--strict', action='store_true',
            help='Strict mode. By default invalid escaped sequences will be omitted.')
    args = parser.parse_args()
    setup_logging(args)

    for line in sys.stdin:
        # Find splits and matches inside the sentence
        escaped = list(escaped_re.finditer(line.strip()))
        splits = list(escaped_re.splititer(line.strip()))
        output = ''

        # Join splits with unescaped matches
        for i, split in enumerate(splits):
            if i != len(splits)-1:
                output += split + unescape(escaped[i], args.strict)
            else:
                output += split

        print(output)


if __name__ == "__main__":
    main()
