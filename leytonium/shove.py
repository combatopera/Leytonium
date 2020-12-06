import sys, subprocess, re

pattern = re.compile('latest|.+[.]latest')

def main_shove():
    spec, = sys.argv[1:]
    slash = spec.index('/')
    colon = spec.rindex(':')
    tag = spec[colon + 1:]
    if pattern.fullmatch(tag) is None:
        raise Exception('REFUSAL!')
    subprocess.check_call(['bash', '-ic', 'aws ecr batch-delete-image --repository-name "$1" --image-ids "$2"', 'ecr', spec[slash + 1:colon], "imageTag=%s" % tag])
    subprocess.check_call(['docker', 'push', spec])
