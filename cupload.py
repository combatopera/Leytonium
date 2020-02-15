import requests, io, zipfile, hashlib, base64, time

def createzip(filedata):
    zipdata = io.BytesIO()
    with zipfile.ZipFile(zipdata, 'w') as zf:
        zf.writestr(zipfile.ZipInfo('woo.txt'), filedata) # Use ZipInfo constructor for deterministic update time.
    zipdata.seek(0)
    return zipdata

def main_cupload():
    'Test the DataUploadServlet.'
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
        time.sleep(.1) # The reponse is committed before processing (including webserver stdout) has finished.
