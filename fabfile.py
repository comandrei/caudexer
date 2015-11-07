from fabric.api import env, run
# the user to use for the remote commands
env.user = 'caudexer'
# the servers where the commands are executed
env.hosts = ['caudexer.com']
REPO_TO_CLONE = "https://github.com/comandrei/caudexer/"
def provision():
    deps = []
    with open("caudexer/requirements.apt") as req_file:
        for line in req_file:
            if line.startswith("#") or line.startswith(" "):
                continue
            deps.append(line.strip())
    run("sudo apt-get update")
    run("sudo apt-get install {} --assume-yes".format(" ".join(deps)))


def deploy():
    run("rm -rf deployed")
    run("virtualenv deployed --python=$(which python3)")
    run("git clone {}".format(REPO_TO_CLONE))
    run("deployed/bin/pip install -r caudexer/caudexer/requirements")
