"""
PDV - Ponto de Venda
Script para publicar Release no GitHub e fazer upload do PDV.exe
"""

import os
import sys
import json
import urllib.request
import urllib.error

REPO = "PaoCariocaPdv/pdv-app"


def get_token():
    token = os.environ.get("GH_TOKEN")
    if not token and os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("GH_TOKEN="):
                    token = line.strip().split("=", 1)[1].strip()
                    break
    if not token:
        raise RuntimeError("GH_TOKEN não encontrado nas variáveis de ambiente ou no .env")
    return token


def make_request(url, method="GET", data=None, headers=None):
    req = urllib.request.Request(url, data=data, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read(), resp.status


def main():
    if len(sys.argv) < 2:
        print("Uso: python publish_release.py <versao> [caminho_exe]")
        sys.exit(1)

    version = sys.argv[1].lstrip("v")
    tag = f"v{version}"
    exe_path = sys.argv[2] if len(sys.argv) > 2 else "dist/PDV.exe"

    if not os.path.exists(exe_path):
        print(f"Erro: Arquivo {exe_path} não encontrado!")
        sys.exit(1)

    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "PDV-Publisher",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # 1. Verifica se já existe uma release com essa tag
    print(f"Verificando releases anteriores para {tag}...")
    release_id = None
    try:
        data, _ = make_request(
            f"https://api.github.com/repos/{REPO}/releases/tags/{tag}",
            headers=headers
        )
        existing = json.loads(data.decode("utf-8"))
        release_id = existing.get("id")
        print(f"Release {tag} já existe (ID: {release_id}). Excluindo para recriar...")
        make_request(
            f"https://api.github.com/repos/{REPO}/releases/{release_id}",
            method="DELETE",
            headers=headers
        )
        print("Release antiga excluída.")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"Aviso ao consultar release: {e}")

    # 2. Cria a nova release
    print(f"Criando release {tag} no GitHub...")
    payload = json.dumps({
        "tag_name": tag,
        "name": f"PDV v{version}",
        "body": f"Release v{version} do PDV - Ponto de Venda com páginas limpas para construção do zero.",
        "draft": False,
        "prerelease": False,
    }).encode("utf-8")

    req_headers = dict(headers)
    req_headers["Content-Type"] = "application/json"

    data, _ = make_request(
        f"https://api.github.com/repos/{REPO}/releases",
        method="POST",
        data=payload,
        headers=req_headers
    )
    release = json.loads(data.decode("utf-8"))
    upload_url_template = release["upload_url"]
    upload_url_base = upload_url_template.split("{")[0]

    # 3. Faz upload do PDV.exe
    file_size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"Fazendo upload do {exe_path} ({file_size_mb:.1f} MB)...")

    with open(exe_path, "rb") as f:
        file_bytes = f.read()

    upload_headers = dict(headers)
    upload_headers["Content-Type"] = "application/octet-stream"

    asset_upload_url = f"{upload_url_base}?name=PDV.exe"
    data, status = make_request(
        asset_upload_url,
        method="POST",
        data=file_bytes,
        headers=upload_headers
    )
    print(f"Upload concluído com sucesso! (Status {status})")
    print(f"Release v{version} publicada com sucesso em: https://github.com/{REPO}/releases/tag/{tag}")


if __name__ == "__main__":
    main()
