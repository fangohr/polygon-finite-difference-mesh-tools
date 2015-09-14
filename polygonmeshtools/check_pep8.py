import subprocess


def test_pep8():
    """Runs pep8 over all code"""
    path = '.'

    command = "pep8 {}".format(path)
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as ex:
        # caught error.
        print("Output with error:\n")
        for line in ex.output.splitlines():
            print(line)
        # some PEP8 problem
        assert False

if __name__ == "__main__":
    test_pep8()
