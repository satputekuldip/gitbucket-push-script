import os
import sys, os, time, re, json, datetime, ctypes, subprocess
if os.name == "nt":
    # Windows
    import msvcrt
else:
    # Not Windows \o/
    import select


def grab(prompt, **kwargs):
    # Takes a prompt, a default, and a timeout and shows it with that timeout
    # returning the result
    timeout = kwargs.get("timeout", 0)
    default = kwargs.get("default", None)
    # If we don't have a timeout - then skip the timed sections
    if timeout <= 0:
        if sys.version_info >= (3, 0):
            return input(prompt)
        else:
            return str(raw_input(prompt))
    # Write our prompt
    sys.stdout.write(prompt)
    sys.stdout.flush()
    if os.name == "nt":
        start_time = time.time()
        i = ''
        while True:
            if msvcrt.kbhit():
                c = msvcrt.getche()
                if ord(c) == 13:  # enter_key
                    break
                elif ord(c) >= 32:  # space_char
                    i += c
            if len(i) == 0 and (time.time() - start_time) > timeout:
                break
    else:
        i, o, e = select.select([sys.stdin], [], [], timeout)
        if i:
            i = sys.stdin.readline().strip()
    print('')  # needed to move to next line
    if len(i) > 0:
        return i
    else:
        return default


def check_path(path):
    # Let's loop until we either get a working path, or no changes
    test_path = path
    last_path = None
    while True:
        # Bail if we've looped at least once and the path didn't change
        if last_path != None and last_path == test_path: return None
        last_path = test_path
        # Check if we stripped everything out
        if not len(test_path): return None
        # Check if we have a valid path
        if os.path.exists(test_path):
            return os.path.abspath(test_path)
        # Check for quotes
        if test_path[0] == test_path[-1] and test_path[0] in ('"', "'"):
            test_path = test_path[1:-1]
            continue
        # Check for a tilde and expand if needed
        if test_path[0] == "~":
            tilde_expanded = os.path.expanduser(test_path)
            if tilde_expanded != test_path:
                # Got a change
                test_path = tilde_expanded
                continue
        # Let's check for spaces - strip from the left first, then the right
        if test_path[0] in (" ", "\t"):
            test_path = test_path[1:]
            continue
        if test_path[-1] in (" ", "\t"):
            test_path = test_path[:-1]
            continue
        # Maybe we have escapes to handle?
        test_path = "\\".join([x.replace("\\", "") for x in test_path.split("\\\\")])


git_initiated = False
def gitInit(path):
    os.system(f"cd {path}")
    os.system(f"cd {path} && git init --bare")
    git_initiated = True


def git_push(command):
    status = os.system(f"{command} status")
    print(status)


while True:
    my_file = grab('Enter the absolute path or drag a file into the terminal:')
    print("")
    if my_file.lower() == "q":
        exit()
    path = check_path(my_file)
    if not path:
        print("That path does not exist!\n")
        grab("Press [enter] to return...")
        continue
    repo_path = check_path(my_file + "/.git/")
    git_path = f"cd {path} && git "
    if not repo_path:
        print("This is not git repo\n")
        gitInit(path)
        git_push(git_path)
    else:
        print("continue giting")
        git_push(git_path)
    # if git_initiated:
    #     os.system(f"rm -rf {repo_path}")
    #     print("git folder deleted")


