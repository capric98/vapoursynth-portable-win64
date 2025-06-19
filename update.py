#!/usr/bin/env python3
# coding: utf-8
import re
import requests
import time

def get_latest_py(tags: list[str], version: str) -> str:
    max_minor = -1

    for tag in tags:
        if re.match(f"v{version}.[0-9]+$", tag):
            minor = int(re.search(r"(?<=.)[0-9]+$", tag).group(0))
            py_version = f"{version}.{minor}"

            try:
                resp = requests.head(f"https://www.python.org/ftp/python/{py_version}/python-{py_version}-embed-amd64.zip")
                resp.raise_for_status()
            except Exception as _:
                print(f"Python {py_version} may not have an precompiled embedded release...")
            else:
                max_minor = max(minor, max_minor)
            finally:
                time.sleep(1)

    return f"{version}.{max_minor}" if max_minor!=-1 else ""


if __name__=="__main__":
    resp = requests.get("https://api.github.com/repos/vapoursynth/vapoursynth/releases/latest")
    resp.raise_for_status()
    releases = resp.json()
    vs_release_tag = releases["name"]

    print(f"VapourSynth release tag: \"{vs_release_tag}\"")

    vs_portable_download_link = None
    for asset in releases["assets"]:
        asset_name = asset["name"]
        if "portable" in asset_name.lower() and asset_name.lower().endswith(".zip"):
            vs_portable_download_link = asset["browser_download_url"]

    if not vs_portable_download_link:
        raise Exception("No portable download link found!")


    resp = requests.get("https://api.github.com/repos/vapoursynth/vapoursynth/tags")
    resp.raise_for_status()
    tags = resp.json()
    for tag in tags:
        if tag["name"] == vs_release_tag:
            commit = tag["commit"]["sha"]
            break

    resp = requests.get(
        "https://raw.githubusercontent.com/vapoursynth/vapoursynth/"+
        commit+
        "/VAPOURSYNTH_VERSION"
    )
    resp.raise_for_status()

    vs_current_release = resp.text.strip().split(" ")[-1].strip().split(" ")[0] # VS_CURRENT_RELEASE


    resp = requests.get(
        "https://raw.githubusercontent.com/vapoursynth/vapoursynth/"+
        commit+
        "/installer/vsinstaller.iss"
    )
    resp.raise_for_status()

    try:
        # py_minor_version_low  = int(re.search(r"(?<=PythonVersionMinorLow )[0-9]+", resp.text).group(0))
        # py_minor_version_high = int(re.search(r"(?<=PythonVersionMinorHigh )[0-9]+", resp.text).group(0))
        py_minor_version  = int(re.search(r"(?<=-cp3)[0-9]+(?=-abi)", resp.text).group(0))
        vs_wheel_filename = re.search(r"(?<=WheelFilename\(Version\) ).*?\.whl'", resp.text).group(0)
        version_var_name  = re.search(r"(?<=\+).*?(?=\+)", vs_wheel_filename).group(0).strip()
        vs_wheel_filename = eval(vs_wheel_filename, {version_var_name: vs_current_release})
    except AttributeError as e:
        print(e)
        print(resp.text)

    resp = requests.get("https://api.github.com/repos/python/cpython/tags?per_page=50")
    resp.raise_for_status()
    tags = resp.json()

    # for py_minor_version in range(py_minor_version_high, py_minor_version_low, -1):
    py_version = get_latest_py(
        tags = [tag["name"] for tag in tags],
        version = f"3.{py_minor_version}",
    )
    if py_version:
        print(f"Python {py_version} selected.")
    else:
        raise Exception(f"cannot find a suitable release for PyMinorVer={py_minor_version}")

    with open("config/VapourSynth.txt", mode="w", encoding="utf-8") as f:
        print(vs_release_tag, end=None, file=f)
    with open("config/VapourSynthPortable.txt", mode="w", encoding="utf-8") as f:
        print(vs_portable_download_link, end=None, file=f)
    with open("config/VapourSynthWheel.txt", mode="w", encoding="utf-8") as f:
        print(vs_wheel_filename, end=None, file=f)
    with open("config/Python.txt", mode="w", encoding="utf-8") as f:
        print(py_version, end=None, file=f)

    print("bump version to v0.{}.{}".format(
        py_version.replace(".", ""),
        vs_release_tag.replace("R", "").replace("C", "").replace("-", "."),
    ), end=None)
