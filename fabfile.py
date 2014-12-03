from __future__ import with_statement
# First we import the Fabric api
from fabric.api import *
from fabric.context_managers import cd, show

# We can then specify host(s) and run the same commands across those systems
#env.user = 'sbook'
#http://debian7-template.ny.sharedbook.com/
env.hosts = ['localhost']



#######################################################################################################################
# installs
def inst_cache_client():
   local_server='http://localhost:3142'
   jupiter_server='http://jupiter:3142'
   prompt(
      "cache server is (i.e.  default='http://localhost:3142'):",
      default=jupiter_server,
      key='cacheserver',
   )
   cacheserver = env['cacheserver'].lower()
   prox_cache='''Acquire {
      Retries 0;
         HTTP {
            Proxy "%(cacheserver)s";
         };
      };'''%locals()
   sudo('echo "%(prox_cache)s" > /etc/apt/apt.conf.d/02proxy.conf'%locals())

def py_cache_client(cache_urls=None):
   jupiter_url='http://jupiter:3141/root/pypi/'
   localhost_url='http://localhost:3141/root/pypi/'
   prompt(
         "cache server is (i.e.  default='%(localhost_url)s'):"%locals(),
         default=jupiter_url,
         key='py_cache_url',
      )
   cache_url = env['py_cache_url'].lower()
   # already installed in the docker
   run("rm ~/.pip/pip.conf")
   sudo("pip install devpi-client")
   pip_conf='''[global]
timeout = 60
index-url = %(cache_url)s
extra-index-url = https://pypi.python.org/pypi
force-yes = true
'''%locals()
   run(''' mkdir -p ~/.pip/ && echo "%(pip_conf)s" > ~/.pip/pip.conf  '''%locals())
   # configure env to use the devpi
   sudo(''' devpi use  --set-cfg  %(cache_url)s '''%locals())


def server_setup_inst_cache_server():
   sudo('apt-get install apt-cacher-ng && service apt-cacher-ng restart')
   sudo('pip install -q devpi-server && devpi-server --stop && devpi-server --host 0.0.0.0 --start ')

def inst_deb_lxc_docker():
   sudo('echo deb http://get.docker.io/ubuntu docker main | sudo tee /etc/apt/sources.list.d/docker.list')
   sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9')
   sudo('apt-get update')
   sudo('apt-get install -y lxc-docker')

def inst_fig():
   sudo('pip install -U fig')

def inst_vim():
   sudo('apt-get install vim')

def  inst_tmux():
   sudo('gem install tmuxinator')
   sudo('apt-get install install byobu')
   setup_custom_byobu()

def setup_custom_byobu():
   run('cp tmux_mk.conf ~/.config/byobu/.tmux.conf')
   #run('echo "source ~/.config/byobu/.tmux.conf" >> ~/.config/byobu/profile.tmux')



#######################################################################################################################


def clean():
   sudo(" docker ps -qa  | xargs  echo  docker rm")
   prompt(
      "continue?",
      default='yes',
      key='cont',
   )
   if env['cont'].lower() in ['yes', 'y']:
      sudo(" docker ps -qa  | xargs  docker rm")
   else:
      run('echo aborted')


def clean_images():
   sudo(" docker images  | grep none | awk '{print $3 }' | xargs  echo  docker rmi")
   prompt(
      "continue?",
      default='yes',
      key='cont',
   )
   if env['cont'].lower() in ['yes', 'y']:
      sudo(" docker images  | grep none | awk '{print $3 }' | xargs  docker rmi")
   else:
      run('echo aborted')
      #    run("uptime")

      #def install():
      #    run("uptime")




#
#def the_target_dir():
#   default_target = 'docker-container-djanginx'
#   other_targets = ['jessie-cached', 'wheezy-cached', 'fcrepo']
#   key = 'target_dir'
#   prompt(
#      "Enter target dir: %s or %s" % (default_target, ', '.join(other_targets)),
#      default=default_target,
#      key=key,
#   )
#   return env[key]
#
#
#def build():
#   target_dir = the_target_dir()
#   local(" cd ./%(target_dir)s && sudo fig  rm    "%locals())
#   local(" cd ./%(target_dir)s && sudo fig  build   "%locals())
#
#def up():
#   target_dir = the_target_dir()
#   local(" cd ./%(target_dir)s && sudo fig  up   "%locals())
#


