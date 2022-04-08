# coding: utf-8
import os
import sys
import zipfile

def add_to_zip(input: str, zip: zipfile.ZipFile):
    if os.path.isfile(input):
        zip.write(input, input)
    else:
        for root, _, files in os.walk(input):
            for file in files:
                f_path = os.path.join(root, file)
                zip.write(f_path, f_path)

if __name__=="__main__":
    argv = sys.argv

    if len(argv)<3:
        print("Usage: python zip-r.py {output}.zip file1 ...")
        sys.exit(1)

    output = argv[1]
    if not output.endswith(".zip"):
        print(f"{output} is not ended with .zip!")
        sys.exit(1)

    argv = argv[2:]

    zip = zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED)
    for f in argv:
        add_to_zip(f, zip)
    zip.close()