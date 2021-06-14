import os
import shutil
import errno
import stat
import platform
from conanfile import IgeConan

def _errorRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IWUSR | stat.S_IWRITE | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        func(path)
    else:
        raise ValueError("file {} cannot be deleted.".format(path))

def setEnv(name, value):
    if platform.system() == 'Windows':
        os.system(f'set {name}={value}')
    else:
        os.system(f'export {name}={value}')
    os.environ[str(name)] = str(value)

def safeRemove(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=False, onerror=_errorRemoveReadonly)
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def build(platform, arch):
    safeRemove('build')
    try:
        os.mkdir('build')
    except:
        pass
    os.chdir('build')
    ret_code = os.system(f'conan install --update .. --profile ../cmake/profiles/{platform}_{arch}')
    if ret_code != 0:
        exit(1)

    os.chdir('..')
    ret_code = os.system('conan build . --build-folder build')
    if ret_code != 0:
        exit(1)

    ret_code = os.system(f'conan export-pkg . {IgeConan.name}/{IgeConan.version}@ige/test --build-folder build --force')
    if ret_code != 0:
        exit(1)

def main():
    setEnv('CONAN_REVISIONS_ENABLED', '1')
    if platform.system() == 'Windows':
        build('windows', 'x86_64')
        build('android', 'x86_64')
        build('android', 'armv8')
    elif platform.system() == 'Darwin':
        build('macos', 'x86_64')
        build('ios', 'armv8')
    ret_code = os.system(f'conan upload {IgeConan.name}/{IgeConan.version}@ige/test --remote ige-center  --all --check --confirm --retry 3 --retry-wait 60 --force')
    if ret_code != 0:
        exit(1)

if __name__ == "__main__":
    main()
