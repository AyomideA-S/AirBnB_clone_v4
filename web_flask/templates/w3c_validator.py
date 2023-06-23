#!/usr/bin/python3
"""
W3C validator for Holberton School

For HTML and CSS files.

Based on 2 APIs:

- https://validator.w3.org/nu/
- http://jigsaw.w3.org/css-validator/validator


Usage:

Simple file:

```
./w3c_validator.py index.html
```

Multiple files:

```
./w3c_validator.py index.html header.html styles/common.css
```

All errors are printed in `STDERR`

Return:
Exit status is the # of errors, 0 on Success

References

https://developer.mozilla.org/en-US/

"""
import sys
import requests


def __print_stdout(msg):
    """Print message in STDOUT
    """
    sys.stdout.write(msg)


def __print_stderr(msg):
    """Print message in STDERR
    """
    sys.stderr.write(msg)


def __analyse_html(file_path):
    """Start analyse of HTML file
    """
    h = {'Content-Type': "text/html; charset=utf-8"}
    d = open(file_path, "rb").read()
    u = "https://validator.w3.org/nu/?out=json"
    r = requests.post(u, headers=h, data=d)
    messages = r.json().get('messages', [])
    return [f"[{file_path}:{m['lastLine']}] {m['message']}" for m in messages]


def __analyse_css(file_path):
    """Start analyse of CSS file
    """
    d = {'output': "json"}
    f = {'file': (file_path, open(file_path, 'rb'), 'text/css')}
    u = "http://jigsaw.w3.org/css-validator/validator"
    r = requests.post(u, data=d, files=f)
    errors = r.json().get('cssvalidation', {}).get('errors', [])
    return [f"[{file_path}:{e['line']}] {e['message']}" for e in errors]


def __analyse(file_path):
    """Start analyse of a file and print the result
    """
    nb_errors = 0
    try:
        result = None
        if file_path.endswith('.css'):
            result = __analyse_css(file_path)
        else:
            result = __analyse_html(file_path)

        if len(result) > 0:
            for msg in result:
                __print_stderr(f"{msg}\n")
                nb_errors += 1
        else:
            __print_stdout(f"{file_path}: OK\n")

    except Exception as e:
        __print_stderr(f"[{e.__class__.__name__}] {e}\n")
    return nb_errors


def __files_loop():
    """Loop that analyses for each file from input arguments
    """
    return sum(__analyse(file_path) for file_path in sys.argv[1:])


if __name__ == "__main__":
    """Main
    """
    if len(sys.argv) < 2:
        __print_stderr("usage: w3c_validator.py file1 file2 ...\n")
        exit(1)

    """execute tests, then exit. Exit status = # of errors (0 on success)
    """
    sys.exit(__files_loop())
