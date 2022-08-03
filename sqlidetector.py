#!/usr/bin/python3
from sys import stdin, argv
from core.cli import cli_opts, print_logo
from core.app import Scanner
from rich.console import Console

console = Console(style="bold red")

def main():
    print_logo()
    opts = cli_opts()
    if opts.file:
        targets = opts.file
    elif opts.stdin:
        targets = [url for url in stdin.readlines() if "?" in url]
    else:
        console.print(f"\n[!] Usage: {argv[0]} -h\n")
        exit(1)
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
