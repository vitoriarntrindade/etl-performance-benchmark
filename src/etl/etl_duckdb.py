import duckdb 
import time

def process_temperatures(file_path: str) -> None:
    """Processa arquivo de temperaturas e retorna estatísticas formatadas.

    Args:
        file_path (str): O caminho do arquivo de temperaturas no formato CSV/TXT.

    Returns:
        None: Retorna None pois escreve os resultados em um arquivo parquet.
    """
    print("Iniciando processamento com DuckDB...")
    start_time = time.time()

    result = duckdb.sql(f"""
        SELECT 
            station, 
            MIN(temperature) AS min_temp, 
            AVG(temperature) AS mean_temp, 
            MAX(temperature) AS max_temp
        FROM read_csv('{file_path}', 
        AUTO_DETECT=FALSE, header=FALSE, delim=';', 
        columns={{'station': 'VARCHAR', 'temperature': 'DECIMAL(4,1)'}})
        GROUP BY station
        ORDER BY station
    """
    )


    result.write_parquet("../../data/temperaturas.parquet", 
                         compression="SNAPPY", 
                         )

    elapsed_time = time.time() - start_time
    print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

    return None

if __name__ == "__main__":
    FILE_PATH = "../../data/measurements.txt"
    process_temperatures(FILE_PATH)
