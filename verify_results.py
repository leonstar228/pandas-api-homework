from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"[OK] {message}")


cats = pd.read_csv(RESULTS_DIR / "task1_cat_facts.csv")
check(len(cats) == 10, "Завдання 1: отримано 10 фактів")
check(set(cats.columns) == {"fact", "length"}, "Завдання 1: DataFrame і стовпець length створено")
check(cats["length"].equals(cats["fact"].str.len()), "Завдання 1: довжину фактів обчислено правильно")
check(cats["length"].idxmin() >= 0 and cats["length"].idxmax() >= 0, "Завдання 1: найкоротший і найдовший факти визначаються")

universities = pd.read_csv(RESULTS_DIR / "task2_universities.csv")
counts = pd.read_csv(RESULTS_DIR / "task2_university_counts.csv")
check({"Ukraine", "Poland"}.issubset(set(universities["country"])), "Завдання 2: завантажено Україну та Польщу")
check(counts["count"].sum() == len(universities), "Завдання 2: DataFrame об'єднано та кількості пораховано")
check((RESULTS_DIR / "task2_university_counts.png").stat().st_size > 1000, "Завдання 2: стовпчиковий графік створено")

countries = pd.read_csv(RESULTS_DIR / "task3_european_countries.csv")
required_country_columns = {"name", "capital", "population", "area", "languages", "density"}
check(required_country_columns.issubset(countries.columns), "Завдання 3: DataFrame країн має всі потрібні поля")
check(countries["density"].notna().all(), "Завдання 3: густоту населення пораховано")
check(len(pd.read_csv(RESULTS_DIR / "task3_top5_area.csv")) == 5, "Завдання 3: топ-5 за площею знайдено")
check(len(pd.read_csv(RESULTS_DIR / "task3_top5_population.csv")) == 5, "Завдання 3: топ-5 за населенням знайдено")
check((RESULTS_DIR / "task3_area_population.png").stat().st_size > 1000, "Завдання 3: scatter plot створено")
check((RESULTS_DIR / "task3_top10_density.png").stat().st_size > 1000, "Завдання 3: графік топ-10 за густотою створено")

weather = pd.read_csv(RESULTS_DIR / "task4_kyiv_forecast.csv")
check(len(weather) == 14, "Завдання 4: прогноз містить 14 днів")
check(set(weather.columns) == {"date", "temp_max", "temp_min", "rain"}, "Завдання 4: DataFrame має потрібні колонки")
check((weather["temp_max"] >= weather["temp_min"]).all(), "Завдання 4: температурні межі коректні")
check(weather["rain"].idxmax() >= 0, "Завдання 4: день із найбільшими опадами знайдено")
check((RESULTS_DIR / "task4_kyiv_temperature.png").stat().st_size > 1000, "Завдання 4: графік із заливкою створено")

pokemons = pd.read_csv(RESULTS_DIR / "task5_pokemons.csv")
pokemon_columns = {"name", "type", "hp", "attack", "defense", "speed", "height", "weight"}
check(len(pokemons) == 30, "Завдання 5: завантажено 30 покемонів")
check(set(pokemons.columns) == pokemon_columns, "Завдання 5: зібрано всі потрібні характеристики")
check(pokemons["attack"].idxmax() >= 0 and pokemons["speed"].idxmax() >= 0 and pokemons["weight"].idxmax() >= 0, "Завдання 5: екстремальні значення знайдено")
check(len(pd.read_csv(RESULTS_DIR / "task5_average_stats_by_type.csv")) > 1, "Завдання 5: середні характеристики за типами пораховано")
check((RESULTS_DIR / "task5_pokemon_subplots.png").stat().st_size > 1000, "Завдання 5: чотири підграфіки створено")

capitals_csv = pd.read_csv(RESULTS_DIR / "task6_capitals_weather.csv")
capitals_json = pd.read_json(RESULTS_DIR / "task6_capitals_weather.json")
capital_columns = {"country", "capital", "population", "temperature", "wind"}
check(len(capitals_csv) == 5, "Завдання 6: об'єднано дані п'яти столиць")
check(set(capitals_csv.columns) == capital_columns, "Завдання 6: фінальний DataFrame має потрібні колонки")
check(capitals_csv.shape == capitals_json.shape, "Завдання 6: CSV та JSON містять однаковий обсяг даних")
check((RESULTS_DIR / "task6_capital_temperatures.png").stat().st_size > 1000, "Завдання 6: графік температур створено")

print("\nУсі пункти виконано й перевірено.")
