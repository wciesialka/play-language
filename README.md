# play-language
Simple play language built and interpreted in Python.

## What is this?

I was bored and looking for something to do, so I wrote my own stack-based language in Python3. This language is tokenized and interpreted in Python3. 
Each token is exactly one character, and whitespace is ignored.

### Syntax?

See [SYNTAX.md](SYNTAX.md) for a table of valid tokens.

## Getting Started

### Installing

Run `setup.py install`.

### Running

Run using `playlanguage` or `python3 -m playlanguage`.

```bash
usage: playlanguage [-h] [-l {d,i,w,e,c}] input

Interpreter for the Playlanguage.

positional arguments:
  input                 Input file.

optional arguments:
  -h, --help            show this help message and exit
  -l {d,i,w,e,c}, --level {d,i,w,e,c}
                        Logging level.
                            d: DEBUG
                            i: INFO
                            w: WARNING
                            e: ERROR
                            c: CRITICAL
```

## Authors

- Willow Ciesialka

## License

See [LICENSE](LICENSE) for details.