#!/usr/bin/env python3

#HALP Test the DataUploadServlet.

import requests, io, zipfile, hashlib, base64

def createzip(filedata):
    zipdata = io.BytesIO()
    with zipfile.ZipFile(zipdata, 'w') as zf:
        zf.writestr(zipfile.ZipInfo('woo.txt'), filedata) # Use ZipInfo constructor for deterministic update time.
    zipdata.seek(0)
    return zipdata

def main():
    port = int(input('Port? '))
    prefix = input('Prefix? ')
    files = {"IGNORED%s" % k: createzip("%s%s" % (prefix, k)) for k in range(2)}
    for name, z in files.items():
        h = hashlib.sha256()
        h.update(z.getvalue())
        print(name, base64.b16encode(h.digest()))
    for dt in 'attachment', 'nope':
        r = requests.post("http://localhost:%s/upload/%s" % (port, dt), files = files)
        print(r.url)
        print(r.text, end = '')

if '__main__' == __name__:
    main()
