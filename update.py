#!/usr/bin/env python3
# coding: utf-8
import re
import requests

def get_latest_py(tags: list[str], major_ver: str) -> str:
    max_minor = -1

    for tag in tags:
        if re.match(f"v{major_ver}.[0-9]+$", tag):
            minor = int(re.search(r"(?<=.)[0-9]+$", tag).group(0))
            max_minor = max(minor, max_minor)

    if max_minor == -1:
        raise ValueError("no minor version")

    return f"{major_ver}.{max_minor}"

if __name__=="__main__":
    resp = requests.get("https://api.github.com/repos/vapoursynth/vapoursynth/tags")
    resp.raise_for_status()
    tags = resp.json()
    vs_version = tags[0]["name"]

    resp = requests.get(
        "https://raw.githubusercontent.com/vapoursynth/vapoursynth/"+
        tags[0]["commit"]["sha"]+
        "/installer/vsinstaller.iss"
    )
    resp.raise_for_status()
    py_major_version = re.search(r"(?<=PythonVersion ')[.0-9]+", resp.text).group(0)

    resp = requests.get("https://api.github.com/repos/python/cpython/tags")
    resp.raise_for_status()
    tags = resp.json()

    py_version = get_latest_py(
        tags = [tag["name"] for tag in tags],
        major_ver = py_major_version,
    )

    with open("config/VapourSynth.txt", mode="w", encoding="utf-8") as f:
        print(vs_version, end=None, file=f)
    with open("config/Python.txt", mode="w", encoding="utf-8") as f:
        print(py_version, end=None, file=f)

    print("Bump version to v0.{}.{}.".format(
        py_version.replace(".", ""),
        vs_version.replace("R", "").replace("C", "").replace("-", "."),
    ), end=None)
