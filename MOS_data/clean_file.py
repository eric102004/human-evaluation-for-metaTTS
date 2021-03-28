import os
import shutil
def clean_file(dirlist):
    for dirname in dirlist:
        if dirname.endswith('.py'):
            continue
        print(f'removing dir:{dirname}')
        for subdir in os.listdir(dirname):
            shutil.rmtree(os.path.join(dirname, subdir))


if __name__ == '__main__':
    dirlist  = os.listdir('.')
    dirlist.remove('__pycache__')
    dirlist.remove('real')
    dirlist.remove('reference')
    for dirname in dirlist:
        if dirname.endswith('.py'):
            dirlist.remove(dirname)
    print(dirlist)
    clean_file(dirlist)
