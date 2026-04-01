import json
import os
import shutil
import platform

if platform.system() == "Windows":
    BASE_DIR = os.path.abspath(os.sep)
else:
    BASE_DIR = "/"

def check_path(path) :
    path = os.path.normpath(path)
    print(path)
    return True

def check_and_inc_name(path) :
    newpath = path
    count = 2
    while os.path.isdir(newpath) or os.path.isfile(newpath):
        p, e = os.path.splitext(path)
        newpath = p + " " + str(count) + e
        count += 1

    return newpath

def rename(old, new):
    src = os.path.join(BASE_DIR, old)
    dst = os.path.join(os.path.dirname(src), new)
    if src != dst :
        dst = check_and_inc_name(dst)
        os.rename(src, dst)
    return '{"ok":"ok"}'

def create(dst, name):
    dst = os.path.join(BASE_DIR, dst, name)
    dst = check_and_inc_name(dst)
    os.mkdir(dst)
    return '{"ok":"ok"}'

def move(src, dst):
    src = os.path.join(BASE_DIR, src)
    dst = os.path.join(BASE_DIR, dst, os.path.basename(src))
    dst = check_and_inc_name(dst)
    shutil.move(src, dst)
    return '{"ok":"ok"}'

def unzip(zip_path):
    zip_path = os.path.join(BASE_DIR, zip_path)
    zip_parent_folder = os.path.dirname(zip_path)
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zf:
        members = [m for m in zf.namelist() if not m.startswith('__MACOSX/')]
        zf.extractall(zip_parent_folder, members)
    return '{"ok":"ok"}'

def zip(folder):
    folder = os.path.join(BASE_DIR, folder)
    if os.path.isdir(folder):
        import zipfile
        zipname = os.path.basename(folder) + ".zip"
        zip_path = os.path.join(os.path.dirname(folder), zipname)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    arcname = os.path.join(os.path.basename(folder),
                                           os.path.relpath(filepath, folder))
                    zf.write(filepath, arcname)
    return '{"ok":"ok"}'

def copy(src, dst):
    src = os.path.join(BASE_DIR, src)
    dst = os.path.join(BASE_DIR, dst, os.path.basename(src))
    dst = check_and_inc_name(dst)
    if os.path.isfile(src) :
        shutil.copy(src, dst)
    if os.path.isdir(src) :
        shutil.copytree(src, dst)
    return '{"ok":"ok"}'

def delete(src):
    src = os.path.join(BASE_DIR, src)
    if os.path.isfile(src) :
        os.remove(src)
    if os.path.isdir(src) :
        shutil.rmtree(src)
    return '{"ok":"ok"}'

def get_node(fpath):
    if fpath == '#' :
        return get_files(BASE_DIR)
    else :
        return get_files(os.path.join(BASE_DIR, fpath))

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            if x == 'bytes' : return "%d %s" % (int(num), x)
            else : return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_to_dict(fpath):
    return {
        'name': os.path.basename(fpath),
        'children': False,
        'type': 'file',
        'size': str(convert_bytes(os.stat(fpath).st_size)),
        'path': os.path.relpath(fpath, BASE_DIR),
        }

def folder_to_dict(fpath):
    return {
        'name': os.path.basename(fpath),
        'children': True,
        'type': 'folder',
        'path': os.path.relpath(fpath, BASE_DIR),
        }

def get_files(rootpath):
    root, folders, files = next(os.walk(rootpath))
    contents = []

    root = os.path.normpath(root)

    folders = sorted(folders, key=lambda s: s.lower())
    files = sorted(files, key=lambda s: s.lower())
    # add to the list if they are cool
    for folder in folders :
        if not folder[0] == '.' and folder != "__pycache__":
            path = os.path.join(root, folder)
            contents += [folder_to_dict(path)]

    for ffile in files :
        if not ffile[0] == '.' :
            path = os.path.join(root, ffile)
            contents += [file_to_dict(path)]

    return json.dumps(contents, indent=4)
