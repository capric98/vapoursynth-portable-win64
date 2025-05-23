#!/usr/bin/env python3
# coding: utf-8
import re
import requests

def get_latest_py(tags: list[str], version: str) -> str:
    max_minor = -1

    for tag in tags:
        if re.match(f"v{version}.[0-9]+$", tag):
            minor = int(re.search(r"(?<=.)[0-9]+$", tag).group(0))
            max_minor = max(minor, max_minor)

    return f"{version}.{max_minor}" if max_minor!=-1 else ""

if __name__=="__main__":
    resp = requests.get("https://api.github.com/repos/vapoursynth/vapoursynth/releases")
    resp.raise_for_status()
    releases = resp.json()
    vs_version = releases[0]["name"]

    print(f"VapourSynth version: \"{vs_version}\"")

    resp = requests.get("https://api.github.com/repos/vapoursynth/vapoursynth/tags")
    resp.raise_for_status()
    tags = resp.json()
    for tag in tags:
        if tag["name"] == vs_version:
            commit = tag["commit"]["sha"]
            break

    resp = requests.get(
        "https://raw.githubusercontent.com/vapoursynth/vapoursynth/"+
        commit+
        "/installer/vsinstaller.iss"
    )
    resp.raise_for_status()

    try:
        py_minor_version_low  = int(re.search(r"(?<=PythonVersionMinorLow )[0-9]+", resp.text).group(0))
        py_minor_version_high = int(re.search(r"(?<=PythonVersionMinorHigh )[0-9]+", resp.text).group(0))
    except AttributeError as e:
        print(e)
        print(resp.text)

    resp = requests.get("https://api.github.com/repos/python/cpython/tags")
    resp.raise_for_status()
    tags = resp.json()

    for py_minor_version in range(py_minor_version_high, py_minor_version_low, -1):
        py_version = get_latest_py(
            tags = [tag["name"] for tag in tags],
            version = f"3.{py_minor_version}",
        )
        if py_version:
            print(f"Python {py_version} selected.")
            break

    with open("config/VapourSynth.txt", mode="w", encoding="utf-8") as f:
        print(vs_version, end=None, file=f)
    with open("config/Python.txt", mode="w", encoding="utf-8") as f:
        print(py_version, end=None, file=f)

    print("bump version to v0.{}.{}".format(
        py_version.replace(".", ""),
        vs_version.replace("R", "").replace("C", "").replace("-", "."),
    ), end=None)
