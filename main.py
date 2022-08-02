#!/usr/bin/pythno3
from core.cli import cli_opts
from core.app import Scanner

def main():
    opts = cli_opts()
    targets = opts.file
    timeout = opts.timeout
    workers = opts.workers

    if opts.proxy:
        proxy = {"http":opts.proxy, "https":opts.proxy}
    else:
        proxy = {}
    app = Scanner(timeout,proxy)
    app.start(targets, workers)
    if opts.output:
        app.write_report(opts.output)


if __name__ == "__main__":
    main() 
