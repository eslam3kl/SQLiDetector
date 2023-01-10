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

requests.packages.urllib3.disable_warnings()  # Disable SSL warnings


class Scanner:
    def __init__(
        self,
        timeout: int = 10,
        headers: Dict[str, str] = {},
        proxies: Dict[str, str] = {},
    ):
        self.found: List[Tuple[str, str]] = []
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
        self._lock = threading.Lock()

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

    def send(self, url: str):
        user_agent = random.choice(self.user_agents)
        headers = {"User-Agent": user_agent}
        headers.update(self.headers)
        try:
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                proxies=self.proxies,
                timeout=self.timeout,
            ).text
            for pattern in self.sql_errors:
                pattern = pattern.strip()
                self._lock.acquire()
                if re.findall(pattern, response):
                    self.found.append((url, pattern))
                    console.print(
                        f"[yellow bold]>>> [/yellow bold] {url}  [red bold]{pattern}[/red bold]"
                    )
                self._lock.release()

        except KeyboardInterrupt:
            exit()
        except:
            pass  # IGNOERING THE ERRORS

    def write_report(self, output: str):
        with open(output, "w") as f:
            f.write(json.dumps(self.found))
