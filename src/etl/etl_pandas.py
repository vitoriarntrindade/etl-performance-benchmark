import pandas as pd 
import time


def process_temperatures(file_path: str) -> dict[str, str]:
    """Processa arquivo de temperaturas e retorna estatísticas formatadas.

    Args:
        file_path (str): O caminho para o arquivo iterável de medições.

    Returns:
        dict[str, str]: Um dicionário com as estações como chaves e as
            temperaturas formatadas como variáveis concatenadas com `/`.
    """
    print("Iniciando processamento...")
    start_time = time.time()

    # Carrega dados com tipos de dados otimizados na leitura
    df = pd.read_csv(
        file_path, 
        sep=";", 
        header=None, 
        names=["station_name", "temperature"],
        dtype={"station_name": "category", "temperature": "float32"},
        engine="c"
    )
         
    # Calcula estatísticas diretamente agrupando pela categoria (rápido)
    result = df.groupby("station_name", 
                        observed=True)["temperature"].agg(["min", "mean", "max"])
    
    # Ordena o index
    sorted_result = result.sort_index()
    
    # Formatação vetorizada com map (muito mais rápido que apply com lambda)
    formatted_result = (
        sorted_result["min"].map("{:.1f}".format) + "/" +
        sorted_result["mean"].map("{:.1f}".format) + "/" +
        sorted_result["max"].map("{:.1f}".format)
    )

    elapsed_time = time.time() - start_time
    print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

    return formatted_result.to_dict()


if __name__ == "__main__":
    FILE_PATH = "../../data/measurements.txt"
    result = process_temperatures(FILE_PATH)