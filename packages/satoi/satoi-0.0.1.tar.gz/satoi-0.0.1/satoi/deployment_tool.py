# deployment_tool.py
from fabric import Connection

class DeploymentTool:
    def __init__(self, target_host, target_user, git_repo):
        self.target_host = target_host
        self.target_user = target_user
        self.git_repo = git_repo

    def deploy(self):
        with Connection(host=self.target_host, user=self.target_user) as conn:
            self._git_clone(conn)
            self._install_dependencies(conn)
            self._build_application(conn)
            self._restart_web_server(conn)
    
    def _git_clone(self, conn):
        conn.run(f'git clone {self.git_repo} /tmp/app')
    
    def _install_dependencies(self, conn):
        conn.run('pip install -r /tmp/app/requirements.txt')
    
    def _build_application(self, conn):
        conn.run('cd /tmp/app && python manage.py migrate')
        conn.run('cd /tmp/app && python manage.py collectstatic --noinput')
    
    def _restart_web_server(self, conn):
        conn.sudo('systemctl restart nginx')
