import git
import os
import time
import sys
import shutil

# Caminho do repositório local
REPO_DIR = "/home/pi/TesteAtualizar/repositorio_local"
# URL do repositório remoto no GitHub
REMOTE_URL = "https://github.com/csilva82/Sistema_001.git"
# Nome do branch principal
MAIN_BRANCH = "main"

def clonar_repositorio():
    print("Clonando repositório...")
    repo = git.Repo.clone_from(REMOTE_URL, REPO_DIR)
    try:
        # Renomeia branch inicial para MAIN_BRANCH
        repo.git.branch('-m', MAIN_BRANCH)
    except Exception:
        pass
    print("Repositório clonado com sucesso.")
    return repo

def atualizar_repositorio():
    # Se a pasta não existe, clona
    if not os.path.exists(REPO_DIR):
        return clonar_repositorio() is not None

    try:
        repo = git.Repo(REPO_DIR)
    except git.exc.InvalidGitRepositoryError:
        print(f"{REPO_DIR} não é um repositório Git válido. Apagando e clonando novamente...")
        shutil.rmtree(REPO_DIR)
        return clonar_repositorio() is not None

    print("Verificando atualizações...")
    o = repo.remotes.origin
    o.fetch()  # busca atualizações no GitHub

    # Garante que o HEAD está apontando para a branch principal
    repo.git.checkout(MAIN_BRANCH)

    # Verifica se há diferenças entre local e remoto
    if repo.head.commit != repo.refs[f'origin/{MAIN_BRANCH}'].commit:
        print("Atualização encontrada! Fazendo pull...")
        o.pull(MAIN_BRANCH)
        print("Repositório atualizado com sucesso  66.")
        return True
    else:
        print("Nenhuma atualização encontrada.")
    return False

if __name__ == "__main__":
    while True:
        atualizado = atualizar_repositorio()
        if atualizado:
            print("Reiniciando programa com a versão nova...")
            os.execv(sys.executable, ['python3'] + sys.argv)
        time.sleep(60)  # verifica a cada 1 minuto
