import sqlite3


class Database:
    def __init__(self, caminho):
        self.__caminho = caminho
        self.criar_tabelas()

    def conectar(self):
        conexao = sqlite3.connect(self.__caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    def criar_tabelas(self):
        with self.conectar() as conexao:
            conexao.executescript(
                """
                CREATE TABLE IF NOT EXISTS produtos (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo           TEXT    NOT NULL CHECK (tipo IN ('perecivel', 'duravel')),
                    nome           TEXT    NOT NULL,
                    preco          REAL    NOT NULL CHECK (preco > 0),
                    quantidade     INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
                    validade       TEXT,
                    garantia_meses INTEGER
                );

                CREATE TABLE IF NOT EXISTS movimentacoes (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL REFERENCES produtos(id) ON DELETE CASCADE,
                    tipo       TEXT    NOT NULL CHECK (tipo IN ('entrada', 'saida')),
                    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                    data       TEXT    NOT NULL
                );
                """
            )
