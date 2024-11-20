DROP DATABASE IF EXISTS DB_ATIVIDADE;
CREATE DATABASE DB_ATIVIDADE;
USE DB_ATIVIDADE;

CREATE TABLE PRODUTOS (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    marca_produto VARCHAR(20),
    nome_produto VARCHAR(20),
    cod_produto INT,
    qtd_estoque INT
);

CREATE TABLE ADMINISTRADOR (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome_usuario VARCHAR(50),
    senha_usuario VARCHAR(10),
    data_cadastro_usuario DATETIME
);

CREATE TABLE FUNCIONARIO (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome_usuario VARCHAR(50),
    senha_usuario VARCHAR(10),
    data_cadastro_usuario DATETIME
);

INSERT INTO ADMINISTRADOR (nome_usuario, senha_usuario, data_cadastro_usuario)
VALUES ('Adriano', 'senha123', NOW());

INSERT INTO PRODUTOS (marca_produto, nome_produto, cod_produto, qtd_estoque) VALUES
('Nike', 'Tenis Run', 1001, 50),
('Adidas', 'Camiseta Sport', 1002, 30),
('Puma', 'Shorts Pro', 1003, 25);