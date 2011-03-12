import os

from fabric.api import *
from fabric.context_managers import path
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts


RSYNC_EXCLUDE = (
    '.DS_Store',
    '.hg',
    '*.pyc',
    '*.example',
    '*.db',
    'media/admin',
    'media/attachments',

    'local_settings.py',
    'fabfile.py',
    'bootstrap.py',
)
env.home = '/home/hungry/'
env.git = 'git://github.com/trentonstrong/hungrry.git'
env.repo = 'hungrry'
env.project = 'hungry'


def _setup_path():
    env.root = os.path.join(env.home, 'www', env.environment)
    env.repo_root = os.path.join(env.root, env.repo)
    env.code_root = os.path.join(env.root, env.repo, env.project)
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.settings = '%(project)s.settings_%(environment)s' % env
    env.python = os.path.join(env.virtualenv_root, 'bin/python')


def staging():
    """ use staging environment on remote host"""
    env.user = 'hungry'
    env.environment = 'staging'
    env.password = 'hyperspacen'
    env.hosts = ['50.56.83.252']
    _setup_path()

def production():
    """ use production environment on remote host"""
    utils.abort('Production deployment not yet implemented.')


def bootstrap():
    """ initialize remote host environment (virtualenv, deploy, update) """
    require('root', provided_by=('staging', 'production'))
    run('mkdir -p %(root)s' % env)
    run('mkdir -p %s' % os.path.join(env.home, 'www', 'log'))
    create_virtualenv()
    deploy()
    update_requirements()
    syncdb()


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    args = '--clear --distribute'
    run('virtualenv %s %s' % (args, env.virtualenv_root))


def _activate():
    """ activates virtualenv """
    with cd(env.virtualenv_root):
        run('source bin/activate')

def _deactivate():
    """ deactivates virtualenv """
    run('deactivate')


def deploy():
    """ check out code on remote host """
    require('root', provided_by=('staging', 'production'))
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    # defaults rsync options:
    # -pthrvz
    # -p preserve permissions
    # -t preserve times
    # -h output numbers in a human-readable format
    # -r recurse into directories
    # -v increase verbosity
    # -z compress file data during the transfer
    #extra_opts = '--omit-dir-times'
    #rsync_project(
    #    env.root,
    #    exclude=RSYNC_EXCLUDE,
    #    delete=True,
    #    extra_opts=extra_opts,
    #)
    with cd(env.root):
        if (files.exists(env.repo_root)):
            run('yes | rm -r %s' % env.repo_root)
        run('git clone %s' % env.git)
    touch()

def syncdb():
    _activate()
    with cd(env.code_root):
        run('python manage.py syncdb')


def update():
    """ update code from source control on remote host """
    require('repo_root', provided_by=('staging', 'production'))
    with cd(env.repo_root):
        run('git checkout master')
        run('git pull')
    update_requirements()
    with cd(env.code_root):
        run('%s manage.py syncdb' % env.python)


def update_requirements():
    """ update external dependencies on remote host """
    require('code_root', provided_by=('staging', 'production'))
    requirements = os.path.join(env.code_root, 'requirements')
    with cd(requirements):
        cmd = ['pip install']
        cmd += ['-E %(virtualenv_root)s' % env]
        cmd += ['--requirement %s' % os.path.join(requirements, 'apps.txt')]
        run(' '.join(cmd))


def touch():
    """ touch wsgi file to trigger reload """
    require('code_root', provided_by=('staging', 'production'))
    apache_dir = os.path.join(env.code_root, 'apache')
    with cd(apache_dir):
        run('touch %s.wsgi' % env.environment)


def update_apache_conf():
    """ upload apache configuration to remote host """
    require('root', provided_by=('staging', 'production'))
    source = os.path.join('apache', '%(environment)s.conf' % env)
    dest = os.path.join(env.home, 'apache.conf.d')
    put(source, dest, mode=0755)
    apache_reload()


def configtest():    
    """ test Apache configuration """
    require('root', provided_by=('staging', 'production'))
    run('apache2ctl configtest')


def apache_reload():    
    """ reload Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo /etc/init.d/apache2 reload')


def apache_restart():    
    """ restart Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo /etc/init.d/apache2 restart')


def symlink_django():    
    """ create symbolic link so Apache can serve django admin media """
    require('root', provided_by=('staging', 'production'))
    admin_media = os.path.join(env.virtualenv_root,
                               'src/django/django/contrib/admin/media/')
    media = os.path.join(env.code_root, 'media/admin')
    if not files.exists(media):
        run('ln -s %s %s' % (admin_media, media))


def reset_local_media():
    """ Reset local media from remote host """
    require('root', provided_by=('staging', 'production'))
    media = os.path.join(env.code_root, 'media', 'upload')
    local('yes | rsync -rvaz %s@%s:%s media/' % (env.user, env.hosts[0], media))
