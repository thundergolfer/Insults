import os
import shutil


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


if __name__ == '__main__':
    copytree(os.path.join(PATH_TO_HERE, 'hit_templates'),
             os.path.join(PATH_TO_HERE, 'simple-amt', 'hit_templates'))
    copytree(os.path.join(PATH_TO_HERE, 'hit_task_properties'),
             os.path.join(PATH_TO_HERE, 'simple-amt', 'hit_properties'))
    copytree(os.path.join(PATH_TO_HERE, 'hit_inputs'),
             os.path.join(PATH_TO_HERE, 'simple-amt', 'hit_inputs'))
