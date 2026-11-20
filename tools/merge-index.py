#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# Merges kedi and pisi repos

from __future__ import print_function

import argparse
import hashlib
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

PISI_INDEX = "https://stable2.pisilinux.org/pisi-index.xml.xz"
NOT_BASE = ["rsyslog", "vixie-cron", "libee", "libestr", "libfastjson", "liblogging"]
NOT_BASE_COMPONENT = "util.admin"


def write_sha1sum(path):
    with open(path, "rb") as f:
        digest = hashlib.sha1(f.read()).hexdigest()
    with open(path + ".sha1sum", "w") as f:
        f.write(digest)


def main():
    parser = argparse.ArgumentParser(description="Merge Kedi's index with Pisi's.")
    parser.add_argument("kedi_index", help="Kedi's own pisi-index.xml, from `pisi index`")
    parser.add_argument("-o", "--output", required=True, help="folder for the merged index files")
    args = parser.parse_args()

    kedi = ET.parse(args.kedi_index).getroot()
    kedi_names = set(p.findtext("Name") for p in kedi.findall("Package"))

    tmp = tempfile.mkdtemp(prefix="merge-index-")
    xz = os.path.join(tmp, "pisi-index.xml.xz")
    subprocess.check_call(["curl", "-fsSL", "-o", xz, PISI_INDEX])
    pisi_xml = subprocess.check_output(["xz", "-dc", xz])
    pisi = ET.fromstring(pisi_xml)
    shutil.rmtree(tmp)

    merged = ET.Element("PISI")
    for element in list(pisi):
        if element.tag == "Package":
            name = element.findtext("Name")
            if name in kedi_names:
                continue
            part_of = element.find("PartOf")
            if name in NOT_BASE and part_of is not None and part_of.text == "system.base":
                part_of.text = NOT_BASE_COMPONENT
        elif element.tag == "Distribution":
            obsoletes = element.find("Obsoletes")
            if obsoletes is not None:
                for p in list(obsoletes):
                    if p.text in kedi_names:
                        obsoletes.remove(p)
        merged.append(element)
    for package in kedi.findall("Package"):
        merged.append(package)

    if not os.path.isdir(args.output):
        os.makedirs(args.output)
    index = os.path.join(args.output, "pisi-index.xml")
    ET.ElementTree(merged).write(index, encoding="utf-8")
    subprocess.check_call(["xz", "-9", "-kf", index])
    write_sha1sum(index)
    write_sha1sum(index + ".xz")
    for path in (index, index + ".xz"):
        subprocess.check_call(["gpg", "--yes", "--detach-sig", path])

    print("Wrote %s" % index)


if __name__ == "__main__":
    main()
