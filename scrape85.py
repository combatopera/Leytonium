import sys, re, base64, os

pattern = re.compile('<~(.+?)~>', re.DOTALL)

def main_scrape85():
    if os.listdir():
        raise Exception
    path, = sys.argv[1:]
    with open(path) as f:
        text = f.read()
    for i, image in enumerate(pattern.findall(text)):
        print(i)
        with open("%s.png" % i, 'wb') as g:
            g.write(base64.a85decode(image))
