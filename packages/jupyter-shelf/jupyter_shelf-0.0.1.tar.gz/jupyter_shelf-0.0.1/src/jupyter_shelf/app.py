import argparse
import os
import subprocess
import textwrap

VENV_DIR = ".venv"
SRC_DIR = "src"
SHELF_ROOT = "~/workspace/shelves"
SAFE_TEXT_EXT = "stxt"
SHELF_FILE = f"shelf.{SAFE_TEXT_EXT}"


def make_shelf(args):
    shelf_path = get_shelf_path(args, create=True)

    commands = f"""
    python{args.python_version} -m venv {VENV_DIR} && echo 'Virtual environment created successfully.' || (echo 'Failed to create virtual environment.' && exit 1)
    source {VENV_DIR}/bin/activate && echo 'Virtual environment activated successfully.' || (echo 'Failed to activate virtual environment.' && exit 1)
    pip install jupyterlab &> install_log.{SAFE_TEXT_EXT}  && echo 'Jupyter Lab installed successfully.' || (echo 'Failed to install Jupyter Lab.' && exit 1)
    python -m ipykernel install --prefix=./{VENV_DIR} --name={args.shelf} && echo 'Kernel installed successfully.' || (echo 'Failed to install kernel.' && exit 1)
    mkdir {SRC_DIR}
    touch {SHELF_FILE}
    """
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=shelf_path)
    out, err = process.communicate(commands.encode('utf-8'))

    print_process_output(process, out, err)


def print_process_output(process, out, err):
    if process.returncode != 0:
        print("An error occurred:")
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))
        return False
    else:
        print(out.decode('utf-8'))
        return True


def list_shelf(args):
    expanded_root = os.path.expanduser(args.root)
    shelves = [os.path.basename(dirpath) for dirpath, _, filenames in os.walk(
        expanded_root) if SHELF_FILE in filenames]
    print_list(shelves)


def get_shelf_path(args, create=False):
    expanded_root = os.path.expanduser(args.root)
    shelf_path = os.path.join(expanded_root, args.shelf)

    if create:
        try:
            if os.path.exists(get_shelf_path_appended(args, "_TO_DELETE")):
                raise Exception(
                    "Shelf directory marked for deletion exists! Try another directory or delete the directory manually!")

            os.makedirs(shelf_path)
        except FileExistsError:
            raise Exception(
                "Shelf directory already exists! Try another directory or delete the directory manually!")
    else:
        if not os.path.exists(shelf_path):
            raise Exception(f"Shelf directory ({shelf_path}) does not exist!")

    return shelf_path


def get_shelf_path_appended(args, append):
    expanded_root = os.path.expanduser(args.root)
    shelf_path = os.path.join(expanded_root, args.shelf+str(append))

    return shelf_path


def get_venv_path(shelf_path):
    venv_path = os.path.join(shelf_path, VENV_DIR)

    if not os.path.exists(venv_path):
        raise Exception(
            f"Virtual environment directory ('{venv_path}') does not exist!")

    return venv_path


def get_src_path(shelf_path, check=True):
    source_path = os.path.join(shelf_path, SRC_DIR)

    if check and not os.path.exists(source_path):
        raise Exception(f"Shelf directory ({source_path}) does not exist!")

    return source_path


def start_jupyter(args):
    shelf_path = get_shelf_path(args)
    venv_path = get_venv_path(shelf_path)
    src_path = get_src_path(shelf_path)

    commands = f"""
    source {venv_path}/bin/activate && echo 'Virtual environment activated successfully.' || (echo 'Failed to activate virtual environment.' && exit 1)
    jupyter-lab --port {args.port}
    """
    try:
        process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=src_path)
        out, err = process.communicate(commands.encode('utf-8'))

        print_process_output(process, out, err)

    except KeyboardInterrupt:
        process.terminate()
        process.wait()
        print("Process terminated due to keyboard interrupt.")


def stop_jupyter(args):
    # Stop the Jupyter notebook server
    print("Stopping the Jupyter notebook server is not implemented yet.")


def rm_shelf(args):
    shelf_path = get_shelf_path(args)

    commands = f"""
    rm -rf {VENV_DIR} && echo 'Virtual environment removed successfully.' || (echo 'Failed to remove virtual environment.' && exit 1)
    rmdir {SRC_DIR} && echo 'Source directory removed successfully.' || (echo 'Failed to remove source directory. Make sure it is empty.' && exit 1)
    rm -f *.{SAFE_TEXT_EXT} && echo 'Text files removed successfully.' || (echo 'Failed to remove text files.' && exit 1)
    cd ..
    rmdir {args.shelf} && echo 'Shelf directory removed successfully.' || (echo 'Failed to remove shelf directory. Make sure it is empty.' && exit 1)
    """
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=shelf_path)
    out, err = process.communicate(commands.encode('utf-8'))

    if not print_process_output(process, out, err):
        subprocess.run(["mv", shelf_path, get_shelf_path_appended(args, "_TO_DELETE")])


def print_list(items):
    console_width = os.get_terminal_size().columns

    tab_separated_string = "\t".join(items)

    wrapped_string = textwrap.fill(tab_separated_string, width=console_width)

    print(wrapped_string)

class WithContext:
    def __init__(self, object):
        self.object = object

    def __enter__(self)->argparse.ArgumentParser:
        return self.object

    def __exit__(self, type, value, traceback):
        pass

def add_sub_parser(subparsers, name, args):
    return WithContext(subparsers.add_parser(name, **args))

def main():
    parser = argparse.ArgumentParser(prog='shelf')
    subparsers = parser.add_subparsers()

    root_args = {'required':False, 'default':SHELF_ROOT, 'help':"Shelf root directory. Default: %(default)s"}
    shelf_arg = {'help':"Name of the shelf. A directory with this name can be found under shelf root."}

    with add_sub_parser(subparsers, 'mk', {'help':"Create a new shelf."}) as p:
        p.add_argument('shelf', **shelf_arg)
        p.add_argument('--root','-R', **root_args)
        p.add_argument('--python-version', default="3", help="Python version number e.g. '3.11'.Make sure "
                    "requested python version is installed. Default: %(default)s")
        p.set_defaults(func=make_shelf)

    with add_sub_parser(subparsers, 'rm', {'help':"Remove specified shelf. Retains notebooks."}) as p:
        p.add_argument('shelf', **shelf_arg)
        p.add_argument('--root','-R', **root_args)
        p.set_defaults(func=rm_shelf)

    with add_sub_parser(subparsers, 'ls', {'help':"List shelves in the given root directory."}) as p:
        p.add_argument('--root','-R', **root_args)
        p.set_defaults(func=list_shelf)

    with add_sub_parser(subparsers, 'start', {'help':"Start jupyter lab in the specified shelf."}) as p:
        p.add_argument('shelf', **shelf_arg)
        p.add_argument('--root','-R', **root_args)
        p.add_argument('--port', type=int, default=8888)
        p.set_defaults(func=start_jupyter)

    with add_sub_parser(subparsers, 'stop', {'help':"Stop jupyter lab running in the specified shelf."}) as p:
        p.add_argument('shelf', **shelf_arg)
        p.add_argument('--root','-R', **root_args)
        p.set_defaults(func=stop_jupyter)

    # Set the default function to be the parser's print_help function
    parser.set_defaults(func=lambda _: parser.print_help())

    args = parser.parse_args()
    args.func(args)

if __name__=='__main__':
    main()