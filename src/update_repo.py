import subprocess
import requests
import os

def get_local_head_commit():
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener el commit local: {e}")
        return None

def get_remote_head_commit(owner, repo, branch='main', token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{branch}'
    headers = {'Authorization': f'token {token}'} if token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    else:
        print(f"Error al obtener el commit remoto: {response.status_code}, {response.text}")
        return None

def git_pull():
    try:
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True, check=True)
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error al hacer git pull: {e}")

def check_and_update_repo(owner, repo, branch='main', token=None):
    os.chdir('/ruta/a/tu/repositorio')  # Cambia esta línea a la ruta de
