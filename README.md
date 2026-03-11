# Comparativo de ETL: Python, Pandas, DuckDB e PySpark

Este projeto tem como objetivo principal testar e comparar o mesmo processo de ETL (Extração, Transformação e Carga) implementado de diferentes formas. Através da mesma tarefa — processar um arquivo de medições meteorológicas para calcular as temperaturas mínima, média e máxima por estação —, exploramos o desempenho, a sintaxe e as particularidades de quatro abordagens diferentes no ecossistema de dados do Python.

## 🎯 A Ideia do Projeto

Quando lidamos com engenharia de dados, muitas vezes temos a mesma demanda, porém com volumes de dados muito distintos. A ideia deste projeto é mostrar, na prática, como uma mesma regra de negócio pode ser resolvida usando diferentes ferramentas, destacando as vantagens, desvantagens e os cenários ideais para cada uma delas.

## 📁 Estrutura e Arquivos

Os arquivos de ETL foram organizados dentro da pasta `src/etl/` e foram padronizados de acordo com as boas práticas (PEP-8, tipagem e docstrings).

### 1. `etl_python.py` (Python Puro / Vanilla)
Implementação utilizando apenas as bibliotecas built-in do Python, como `csv` e `collections.defaultdict`.
- **Funções Principais**: `load_temperatures` (lê o CSV iterativamente), `calculate_statistics` (calcula min, max, e média com laços) e `format_result` (formata a saída de texto).
- **Vantagens**: Não possui dependências externas. Simples de debugar.
- **Quando usar**: Em scripts do dia a dia, projetos com extrema restrição de pacotes externos, ou quando o volume de dados é pequeno o suficiente para não comprometer o tempo de execução.
- **Desvantagem**: Extremamente lento para grandes volumes de dados (milhões de linhas).

### 2. `etl_pandas.py` (Pandas)
Utiliza a famosa biblioteca `pandas` para ler o arquivo e fazer operações vetorizadas.
- **Funções Principais**: `process_temperatures` aproveita os métodos otimizados como `read_csv` (com `engine='c'`) e agregações nativas via `groupby().agg()`.
- **Vantagens**: Muito expressivo, código limpo e conciso. Altamente rápido em memória.
- **Quando usar**: Melhor escolha para exploração de dados, ciência de dados e cargas de trabalho que cabem confortavelmente na memória RAM da máquina (geralmente arquivos de até alguns gigabytes).
- **Desvantagem**: Limitado pela memória (In-memory computing). Se o dado extrapolar a RAM, o processo falhará (Out Of Memory Error).

### 3. `etl_duckdb.py` (DuckDB)
DuckDB é um banco de dados analítico (OLAP) embutido que entende sintaxe SQL e executa de forma incrivelmente rápida em arquivos locais.
- **Funções Principais**: `process_temperatures` utiliza queries SQL (`duckdb.sql`) diretamente sobre o arquivo CSV e salva o resultado particionado e comprimido em formato Parquet (`write_parquet`).
- **Vantagens**: Execução extremamente otimizada, capacidade de realizar processamento "Out-of-Core" (processar arquivos maiores que a RAM) e uso de sintaxe SQL clássica.
- **Quando usar**: Perfeito para rodar pipelines modernos locais ou em servidores únicos ("single-node"), processando gigabytes de dados muito rapidamente e economizando em infraestrutura distribuída em nuvem.

### 4. `etl_pyspark.py` (PySpark)
Spark é o mecanismo padrão da indústria para Big Data. Usamos a API do PySpark.
- **Vantagens**: Processamento distribuído ("cluster-computing"). Ele consegue paralelizar a computação de terabytes de dados em múltiplas máquinas sob o capô.
- **Quando usar**: Cenários reais de Big Data, onde o volume chega aos Terabytes ou Petabytes, ou ao orquestrar jobs robustos na nuvem via Databricks ou EMR.
- **Desvantagem**: "Overhead" de tempo para inicializar a sessão do Spark ("SparkSession"). Em pequenos arquivos, inicializar o Spark demora mais do que o cálculo de fato.

## 🚀 Como Executar

Garanta que as dependências estejam instaladas (ex: `pandas`, `duckdb`, `pyspark`) e que você esteja na raiz do repositório.

```bash
# Executando Python Puro
python src/etl/etl_python.py

# Executando Pandas
python src/etl/etl_pandas.py

# Executando DuckDB
python src/etl/etl_duckdb.py

# Executando PySpark
python src/etl/etl_pyspark.py
```