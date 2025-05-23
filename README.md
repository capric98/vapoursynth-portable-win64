# vapoursynth-portable-win64

Run a portable version of [vapoursynth](https://github.com/vapoursynth/vapoursynth) out-of-the-box, so you can install any version of Python you like in `PATH` without breaking any dependencies.

## Packages

You can check the list of pre-installed packages from [Plugins.txt](https://github.com/capric98/vapoursynth-portable-win64/blob/master/config/Plugins.txt) and [Scripts.txt](https://github.com/capric98/vapoursynth-portable-win64/blob/master/config/Scripts.txt).

## Usage

Download the latest [release](https://github.com/capric98/vapoursynth-portable-win64/releases/latest).

Unzip it and open a command window in the folder, then:

```bat
call bootstrap.bat
VSPipe.exe script.vpy --y4m - | x264 - --demuxer y4m -o output.mkv
VSPipe.exe script.vpy --y4m - | x265 - --y4m -o output.mkv
```

## 
An awesome fork of VapourSynth-Editor which supports v4 API can be founded [here](https://github.com/YomikoR/VapourSynth-Editor/releases/latest).
