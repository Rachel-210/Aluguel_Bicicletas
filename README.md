# 🚴 Dashboard Analítico - Sistema de Aluguel de Bicicletas

## 📋 Descrição do Projeto
Este projeto consiste em um **Dashboard de Indicadores (KPIs)** focado em um cenário real de mobilidade urbana: uma locadora de bicicletas de curto período (estilo *Bike Itaú*). O sistema visa monitorar o desempenho financeiro, a utilização da frota de bicicletas e o comportamento dos clientes para apoiar decisões estratégicas de balanceamento de estoque e manutenção preditiva.

A aplicação foi desenvolvida utilizando **Python (Streamlit)** para a interface visual e está conectada diretamente a um banco de dados relacional **PostgreSQL**, utilizando consultas SQL analíticas e avançadas para extração de dados em tempo real.

---

## 🏗️ Estrutura do Banco de Dados
O modelo relacional é composto por 3 tabelas principais altamente integradas:
* `clientes`: Cadastro de usuários contendo dados pessoais e validação de consistência de CPF.
* `bicicletas`: Controle de inventário da frota por modelo e status atual (Disponível, Alugada, Manutenção).
* `alugueis`: Tabela de fatos contendo os registros de locação, chaves estrangeiras (`FK`), marcas temporais de retirada/devolução e o valor financeiro cobrado.

---

## 📊 Requisitos Atendidos

### 1. Indicadores de Negócio (KPIs) 
* **Total de Aluguéis Realizados:** Volume geral utilizando agregação `COUNT`.
* **Faturamento Total:** Receita bruta gerada no período utilizando `SUM`.
* **Ticket Médio por Locação:** Valor médio gasto por aluguel calculada via `AVG`.
* **Clientes Atendidos:** Quantidade de usuários únicos ativos utilizando `COUNT(DISTINCT...)`.

### 2. Elementos Visuais e Gráficos 
* **Gráfico de Linhas:** Linha temporal de evolução dos aluguéis diários para análise de sazonalidade (`GROUP BY DATE`).
* **Gráfico de Barras Horizontais:** Ranking de popularidade e uso dos modelos de bicicletas (`JOIN` + `ORDER BY DESC`).
* **Gráfico de Pizza/Rosca:** Proporção atual do status da frota de veículos para gestão de manutenção.

### 3. Filtros Dinâmicos
* Filtros temporais por **Data Inicial** e **Data Final** que recalculam instantaneamente todos os KPIs e gráficos através de parâmetros dinâmicos (`WHERE data_aluguel BETWEEN %s AND %s`).

---

## ⚙️ Tecnologias Utilizadas
* **Banco de Dados:** PostgreSQL
* **Linguagem de Programação:** Python 
* **Interface e Dashboard:** Streamlit
* **Manipulação e Conexão de Dados:** Pandas e Psycopg2 
* **Gráficos Interativos:** Plotly Express 

---

## 🚀 Como Executar o Projeto Localmente

### 1. Configurar o Banco de Dados
No seu terminal ou gerenciador PostgreSQL (pgAdmin/DBeaver), execute o script de criação e população das tabelas:
```sql
-- Execute os comandos contidos nos arquivos:
-- 1. estrutura_banco.sql
-- 2. dados_ficticios.sql
