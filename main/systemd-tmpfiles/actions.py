#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import mesontools

def setup():
    options = " ".join([
        "-Dmode=release",
        "-Dlibc=glibc",
        "-Dtmpfiles=true",
        "-Dstandalone-binaries=tmpfiles",
        "-Dacl=enabled",
        "-Dman=disabled",
        "-Dtests=false",
        "-Dsysusers=false",
        "-Dhwdb=false",
        "-Dkernel-install=false",
        "-Dbootloader=disabled",
        "-Dukify=disabled",
        "-Dselinux=disabled",
        "-Dblkid=disabled",
        "-Dlibmount=disabled",
        "-Danalyze=false",
        "-Dbacklight=false",
        "-Dbinfmt=false",
        "-Dcoredump=false",
        "-Dfirstboot=false",
        "-Dhibernate=false",
        "-Dhostnamed=false",
        "-Dinitrd=false",
        "-Dlocaled=false",
        "-Dlogind=false",
        "-Dmachined=false",
        "-Dnetworkd=false",
        "-Doomd=false",
        "-Dportabled=false",
        "-Dpstore=false",
        "-Dquotacheck=false",
        "-Drandomseed=false",
        "-Dresolve=false",
        "-Drfkill=false",
        "-Dtimedated=false",
        "-Dtimesyncd=false",
        "-Duserdb=false",
        "-Dutmp=false",
        "-Dvconsole=false",
        "-Dxdg-autostart=false",
    ])
    mesontools.configure(options)

def build():
    mesontools.build("systemd-tmpfiles.standalone")

def install():
    pisitools.insinto("/usr/bin", "build/systemd-tmpfiles.standalone", "systemd-tmpfiles")
    pisitools.dodoc("README.md", "LICENSE.LGPL2.1", "LICENSE.GPL2")
