CREATE TABLE clientes (
id_cliente SERIAL PRIMARY KEY,
nome VARCHAR(150) NOT NULL,
telefone VARCHAR(20),
cpf VARCHAR(11) UNIQUE NOT NULL,
CHECK (char_length(cpf) = 11)
);

CREATE TABLE bicicletas(
id_bicicleta SERIAL PRIMARY KEY,
modelo VARCHAR(150) NOT NULL,
status VARCHAR(20) NOT NULL
);

CREATE TABLE alugueis(
id_aluguel SERIAL PRIMARY KEY,
fk_cliente INT NOT NULL,
fk_bicicleta INT NOT NULL,
data_aluguel TIMESTAMP NOT NULL,
data_devolucao TIMESTAMP, 
valor_total NUMERIC(10, 2) NOT NULL,
FOREIGN KEY (fk_cliente) REFERENCES clientes(id_cliente),
FOREIGN KEY (fk_bicicleta) REFERENCES bicicletas(id_bicicleta)
);