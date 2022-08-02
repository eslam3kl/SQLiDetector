#!/usr/bin/python3
from core.cli import cli_opts, print_logo
from core.app import Scanner


def main():
    print_logo()
    opts = cli_opts()
    targets = opts.file
    timeout = opts.timeout
    workers = opts.workers

    if opts.proxy:
        proxy = {"http": opts.proxy, "https": opts.proxy}
    else:
        proxy = {}
    app = Scanner(timeout, proxy)
    app.start(targets, workers)
    if opts.output:
        app.write_report(opts.output)


if __name__ == "__main__":
    main()
