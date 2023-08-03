from typing import Dict, List, Tuple
from pathlib import Path

import exurl
import json
import threading
from core.cli import base_dir, console
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Column
import requests
import random
import re
import time
import queue

requests.packages.urllib3.disable_warnings()  # Disable SSL warnings


class Scanner:
    def __init__(
        self,
        timeout: int = 5,
        headers: Dict[str, str] = {},
        proxies: Dict[str, str] = {},
    ):
        self.found = queue.Queue()
        self.timeout = timeout
        self.proxies = proxies
        self.headers = headers
        self.user_agents = (
            Path(f"{base_dir}/txt/user_agents.txt").read_text().splitlines()
        )
        self.sql_errors = (
            Path(f"{base_dir}/txt/sql_errors.txt").read_text().splitlines()
        )
        self.payloads = Path(f"{base_dir}/txt/payloads.txt").read_text().splitlines()

    def start(self, targets: List[str], workers: int = 10):
        new_targets = []
        started_workers = []
        targets = [target.strip() for target in targets]
        for payload in self.payloads:
            current_urls = exurl.split_urls(targets, payload)
            new_targets.extend(current_urls)

        with Progress(
            TextColumn(
                "[progress.percentage] Scanning {task.completed}/{task.total} | {task.percentage:>3.0f}% ",
                table_column=Column(ratio=1),
            ),
            BarColumn(bar_width=50, table_column=Column(ratio=2)),
            SpinnerColumn(),
            console=console,
        ) as progress:
            pb_counter = len(new_targets)
            task1 = progress.add_task("[green] Scanning ...", total=pb_counter)
            with ThreadPoolExecutor(max_workers=workers) as executor:
                for url in new_targets:
                    started_workers.append(executor.submit(self.send, url))
                for _ in as_completed(started_workers):
                    progress.update(task1, advance=1)

        # Wait for all tasks to complete before writing the report
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.write_report, "report.json")

    def send(self, url: str):
        user_agent = random.choice(self.user_agents)
        headers = {"User-Agent": user_agent}
        headers.update(self.headers)
        try:
            # Use a session for connection pooling
            with requests.Session() as session:
                response = session.get(
                    url,
                    headers=headers,
                    verify=False,
                    proxies=self.proxies,
                    timeout=self.timeout,
                ).text
            for pattern in self.sql_errors:
                pattern = pattern.strip()
                if re.findall(pattern, response):
                    self.found.put((url, pattern))
                    console.print(
                        f"[yellow bold]>>> [/yellow bold] {url}  [red bold]{pattern}[/red bold]"
                    )
        except KeyboardInterrupt:
            exit()
        except:
            pass  # IGNORING THE ERRORS

        # Add a delay to throttle requests (adjust the value as needed)
        time.sleep(0.1)

    def write_report(self, output: str):
        results = []
        while not self.found.empty():
            results.append(self.found.get())
        with open(output, "w") as f:
            f.write(json.dumps(results))
