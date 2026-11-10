#!/usr/bin/python

import os

DATADIR = "/root/.gnupg"
DATADIRMODE = 0o700

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
        if not os.path.exists(DATADIR):
            os.makedirs(DATADIR, DATADIRMODE)
        
        os.system ("gpg --homedir %s --batch --import /usr/share/kedi/keyrings/kedi.asc" % DATADIR)
        os.system("echo '9E85F9FD3DA7B18E1C3B83B142544D8F3BF9CD4A:6:' | gpg --homedir %s --batch --import-ownertrust" % DATADIR)