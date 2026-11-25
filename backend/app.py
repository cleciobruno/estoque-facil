import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException

from database import Database
from models import ErroDominio, ValidacaoError
from repositories import MovimentacaoRepository, ProdutoRepository
from services import EstoqueService

PASTA_BACKEND = Path(__file__).parent
PASTA_FRONTEND = PASTA_BACKEND.parent / "frontend"


def criar_app(caminho_banco=os.environ.get("DB_PATH", PASTA_BACKEND / "estoque.db")):
    app = Flask(__name__, static_folder=None)

    db = Database(caminho_banco)
    service = EstoqueService(ProdutoRepository(db), MovimentacaoRepository(db))

    def corpo_json():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            raise ValidacaoError("Envie um corpo JSON válido.")
        return dados

    # ---------- tratamento de erros ----------
    @app.errorhandler(ErroDominio)
    def erro_dominio(erro):
        return jsonify({"erro": str(erro)}), erro.status_http

    @app.errorhandler(Exception)
    def erro_inesperado(erro):
        if isinstance(erro, HTTPException):
            return jsonify({"erro": erro.description}), erro.code
        app.logger.exception(erro)
        return jsonify({"erro": "Erro interno no servidor."}), 500

    # ---------- produtos ----------
    @app.get("/api/produtos")
    def listar():
        return jsonify([p.to_dict() for p in service.listar()])

    @app.post("/api/produtos")
    def cadastrar():
        produto = service.cadastrar(corpo_json())
        return jsonify(produto.to_dict()), 201

    @app.get("/api/produtos/<int:id>")
    def obter(id):
        return jsonify(service.obter(id).to_dict())

    @app.put("/api/produtos/<int:id>")
    def atualizar(id):
        return jsonify(service.atualizar(id, corpo_json()).to_dict())

    @app.delete("/api/produtos/<int:id>")
    def remover(id):
        service.remover(id)
        return "", 204

    # ---------- movimentações ----------
    @app.post("/api/produtos/<int:id>/movimentacoes")
    def movimentar(id):
        dados = corpo_json()
        produto = service.movimentar(id, dados.get("tipo"), dados.get("quantidade"))
        return jsonify(produto.to_dict()), 201

    @app.get("/api/produtos/<int:id>/movimentacoes")
    def historico(id):
        return jsonify([m.to_dict() for m in service.historico(id)])

    # ---------- front-end ----------
    @app.get("/")
    def index():
        return send_from_directory(PASTA_FRONTEND, "index.html")

    @app.get("/<path:arquivo>")
    def estaticos(arquivo):
        return send_from_directory(PASTA_FRONTEND, arquivo)

    return app


if __name__ == "__main__":
    criar_app().run(debug=True)
