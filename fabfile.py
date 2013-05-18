from fabric.api import run, cd, prefix, put, local, env, lcd, abort

env_prefix = 'source %s/env/bin/activate' % (env.cwd)


def deploy():
    check_branch()
    prepare_package()
    upload_package()
    unpack_package()
    stop_server()
    switch_installation()
    install_environment()
    update_db()
    collect_static_files()
    start_server()


def check_branch():
    if not env.branch:
        abort("No branch set for deployment")
    branch = local("git rev-parse --abbrev-ref HEAD", capture=True)
    if branch != env.branch:
        abort("You are on the wrong branch for this deployment: " + branch)


def prepare_package():
    """
    We basically want to publish every file that isn't marked as ignored right now
    plus some extra stuff. We put everything into a nice little zip file for this.
    """
    with lcd('pygraz_website/static'):
        local('rm -rf css/*.css')
        local('compass compile -s compact')
    with lcd('pygraz_website'):
        local('django-admin.py compilemessages')
    local('rm -rf production.zip')
    local('zip -x@production-exclude.lst -r production.zip *')
    with lcd('pygraz_website/static/css'):
        local('rm -rf *.css')


def upload_package():
    put('production.zip', 'tmp/production.zip')


def unpack_package():
    with cd('tmp'):
        run('rm -rf app && mkdir app && cd app && unzip ../production.zip')


def stop_server():
    with prefix(env_prefix):
        run('circusctl --endpoint {0} stop django'.format(env.circus_endpoint))


def switch_installation():
    run('rm -rf app_previous && if [[ -d app ]]; then mv app app_previous; fi')
    run('mv tmp/app ./')


def install_environment():
    with prefix('source env/bin/activate'):
        run('pip install -r app/requirements.txt')


def update_db():
    with prefix(env_prefix), cd('app'):
        run('python manage-{0}.py syncdb --noinput --migrate'.format(env.environment))


def collect_static_files():
    with prefix(env_prefix), cd('app'):
        run('mkdir -p pygraz_website/static_collected && python manage-{0}.py collectstatic -c --noinput'.format(env.environment))


def start_server():
    with prefix(env_prefix):
        run('circusctl --endpoint {0} start django'.format(env.circus_endpoint))
