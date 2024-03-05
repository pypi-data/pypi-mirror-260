import os
import re
import subprocess
import tempfile
from collections import namedtuple
from contextlib import contextmanager

from tqdm import tqdm

from rkale.exceptions import DataRootError


def read(file_path):
    if os.path.exists(file_path):
        return open(file_path, "r").readlines()
    return []


@contextmanager
def check_files(paths):
    Check = namedtuple("Check", ["src_out", "dst_out", "diff_out", "stderr"])
    checks = []
    for source, destination in paths:
        print(f"Comparing paths {source} and {destination}...")
        src_out, dst_out, diff_out, error_out = (
            tempfile.mkstemp()[1] for _ in range(4)
        )
        result = subprocess.run(
            f"rclone check {source} {destination}"
            + f" --missing-on-src {src_out}"
            + f" --missing-on-dst {dst_out}"
            + f" --error {error_out} --differ {diff_out}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        errors = read(error_out)
        files_stderr = ""
        if errors:
            files_stderr = "/n".join(
                [
                    f"Got {len(errors)} when comparing {source} and {destination}",
                    "Caused by files:",
                    *errors,
                ]
            )
        stderr = (
            result.stderr.decode("utf-8")
            if (
                not read(src_out)
                and not read(dst_out)
                and not read(diff_out)
                and result.returncode == 1
            )
            else files_stderr
        )
        os.remove(error_out)
        checks.append(Check(src_out, dst_out, diff_out, stderr))

    try:
        yield checks
    finally:
        for check in checks:
            os.remove(check.src_out)
            os.remove(check.dst_out)
            os.remove(check.diff_out)


def check_paths(paths):
    for pair in paths:
        for item in pair:
            split_path = item.split(":")

            # path is local
            if len(split_path) == 1:
                if os.path.expanduser(
                    split_path[0].rstrip(".").rstrip("/")
                ) == os.path.expanduser("~"):
                    raise DataRootError(f"Local {item} is a root path")
            else:
                if split_path[1].rstrip(".").rstrip("/") == "":
                    raise DataRootError(f"Remote {item} is a root path")


def sync(source, destination, files_from=None, progress=False, flags=None):
    return _run(
        "sync",
        source,
        destination,
        files_from=files_from,
        progress=progress,
        flags=flags,
    )


def copy(source, destination, files_from=None, progress=False, flags=None):
    return _run(
        "copy",
        source,
        destination,
        files_from=files_from,
        progress=progress,
        flags=flags,
    )


def _run(command, source, destination, files_from=None, progress=False, flags=None):
    if flags is None:
        flags = []
    if files_from is not None:
        flags.append(f"--files-from {files_from}")
    if progress:
        flags.append("--progress")

    command = " ".join(["rclone", command, source, destination, *flags])
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    if progress:
        pbar = tqdm(desc="Transferring")
        while True:
            line = process.stdout.readline()
            if line:
                line = line.decode("utf-8")
                update = re.findall(
                    r"^Transferred.* ([0,1-9][0-9]*) / ([0,1-9][0-9]*)", line
                )
                if update:
                    pbar.total = int(update[0][1])
                    pbar.n = int(update[0][0])
                    pbar.refresh()
            else:
                pbar.close()
                break
    return process.wait()
