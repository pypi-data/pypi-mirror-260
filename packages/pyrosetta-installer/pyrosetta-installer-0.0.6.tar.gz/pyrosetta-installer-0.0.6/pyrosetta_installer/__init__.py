import os, sys, platform, subprocess
import urllib.request

_PYROSETTA_EAST_MIRROR_ = 'https://graylab.jhu.edu/download/PyRosetta4/archive/release'
_PYROSETTA_WEST_MIRROR_ = 'https://west.rosettacommons.org/pyrosetta/release/release'
_PYROSETTA_RELEASES_URLS_ = [_PYROSETTA_WEST_MIRROR_, _PYROSETTA_EAST_MIRROR_]


def get_pyrosetta_os():
    if sys.platform.startswith("linux"):
        if platform.uname().machine == 'aarch64': r = 'aarch64'
        else: r = 'ubuntu' if os.path.isfile('/etc/lsb-release') and 'Ubuntu' in open('/etc/lsb-release').read() else 'linux'  # can be linux1, linux2, etc
    elif sys.platform == "darwin" : r = 'mac'
    elif sys.platform == "cygwin" : r = 'cygwin'
    elif sys.platform == "win32" :  r = 'windows'
    else:                           r = 'unknown'

    if platform.machine() == 'arm64': r = 'm1'

    return r


def install_pyrosetta(mirror=0, type='Release', extras='', serialization=False, silent=False, skip_if_installed=True):
    if skip_if_installed:
        try:
            import pyrosetta
            if not silent: print('PyRosetta install detected, doing nothing...')
            return

        except ModuleNotFoundError:
            pass

    assert not (serialization and extras), 'ERROR: both extras and serialization flags should not be specified!'
    if serialization: extras = '.cxx11thread.serialization'

    os_name = get_pyrosetta_os()

    if os_name not in ['ubuntu', 'linux', 'mac', 'm1']:
        print(f'Could not find PyRosetta wheel for {os_name!r}, aborting...')
        sys.exit(1)

    print(f'Installing PyRosetta...\nos: {os_name}\ntype: {type}\nextras: {extras}\nmirror: {_PYROSETTA_RELEASES_URLS_[mirror]}\n')

    url = f'{_PYROSETTA_RELEASES_URLS_[mirror]}/PyRosetta4.{type}.python{sys.version_info.major}{sys.version_info.minor}.{os_name}{extras}.wheel/'

    login, password = '', ''

    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, login, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    try:
        with urllib.request.urlopen(url+'latest.html') as f:
            html = f.read().decode('utf-8')
            wheel = html.partition('url=')[2].partition('"')[0]

    except urllib.error.HTTPError as e:
        print(f'Could not retrive PyRosetta wheel for {os_name!r} error-code: {e.code}, aborting...')
        sys.exit(1)



    url_parts = list( url.partition('https://') )
    url_parts.insert(-1, f'{login}:{password}@')
    url = ''.join(url_parts)

    url += wheel
    print(url)

    subprocess.check_call(f'pip install {url}', shell=True)
