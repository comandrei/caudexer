from fabric.api import env, run, put
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
    run("sudo pip install -U pip")

def configure():
    put("caudexer.nginx.conf", "/tmp/caudexer.nginx.conf")
    put("gunicorn.conf", "/tmp/gunicorn.conf")
    run("sudo mv /tmp/gunicorn.conf /etc/init/gunicorn.conf")
    run("sudo mv /tmp/caudexer.nginx.conf /etc/nginx/sites-enabled/caudexer.conf")
    run("sudo service nginx restart")

def deploy():
    # run("rm -rf deployed")
    # run("git clone {}".format(REPO_TO_CLONE))
    run("virtualenv deployed --python=$(which python3)")
    run("cd caudexer; git pull")
    run("deployed/bin/pip install -r dexer/requirements.txt")
    run("sudo service gunicorn restart")
