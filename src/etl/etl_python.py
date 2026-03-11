import time
from csv import reader
from collections import defaultdict
from pathlib import Path

TXT_PATH = "data/measurements.txt"


def load_temperatures(file_path: str) -> dict[str, list[float]]:
    """Carrega temperaturas do arquivo de texto.

    Args:
        file_path (str): O caminho para o arquivo de texto com as medições.

    Returns:
        dict[str, list[float]]: Um dicionário mapeando os nomes das estações
            para uma lista de suas respectivas temperaturas.
    """
    temperatures_by_station = defaultdict(list)
    with open(file_path, "r", encoding="utf-8") as f:
        csv_reader = reader(f, delimiter=";")
        for row in csv_reader:
            station_name = str(row[0])
            temperature = float(row[1])
            temperatures_by_station[station_name].append(temperature)
    return temperatures_by_station


def calculate_statistics(
    temperatures_by_station: dict[str, list[float]],
) -> dict[str, tuple[float, float, float]]:
    """Calcula mínima, média e máxima de temperaturas por estação.

    Args:
        temperatures_by_station (dict[str, list[float]]): Dicionário com
            temperaturas agregadas por estação.

    Returns:
        dict[str, tuple[float, float, float]]: Dicionário mapeando os nomes
            das estações para uma tupla de (mínima, média, máxima).
    """
    result = {}
    for station_name, temperatures in temperatures_by_station.items():
        min_temp = min(temperatures)
        mean_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        result[station_name] = (min_temp, mean_temp, max_temp)
    return result


def format_result(
    sorted_result: dict[str, tuple[float, float, float]],
) -> dict[str, str]:
    """Formata resultado para exibição.

    Args:
        sorted_result (dict[str, tuple[float, float, float]]): Dicionário
            ordenado com as estatísticas por estação.

    Returns:
        dict[str, str]: Dicionário formatado em string.
    """
    return {
        station_name: f"{min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}"
        for station_name, (min_temp, mean_temp, max_temp) in sorted_result.items()
    }


def process_temperatures(file_path: str) -> dict[str, str] | None:
    """Processa arquivo de temperaturas e retorna estatísticas formatadas.

    Args:
        file_path (str): Caminho do arquivo de origem.

    Returns:
        dict[str, str] | None: Resultados formatados.
    """
    print("Iniciando processamento...")
    start_time = time.time()

    # Carrega dados
    temperatures_by_station = load_temperatures(file_path)
    print("Processamento finalizado.")

    # Calcula estatísticas
    result = calculate_statistics(temperatures_by_station)
    print("Estatísticas calculadas. Ordenando...")

    # Ordena e formata resultado
    sorted_result = dict(sorted(result.items()))
    formatted_result = format_result(sorted_result)

    elapsed_time = time.time() - start_time
    print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

    return formatted_result


if __name__ == "__main__":
    TXT_PATH = "../../data/measurements.txt"
    process_temperatures(TXT_PATH)

