from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

session = requests.Session()
session.headers.update({"User-Agent": "pandas-api-homework/1.0"})


def load_json(url, params=None):
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_table(frame, name):
    frame.to_csv(RESULTS_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")


cat_data = load_json("https://catfact.ninja/facts", {"limit": 10})
cats = pd.DataFrame(cat_data["data"])[["fact"]]
cats["length"] = cats["fact"].str.len()
shortest_fact = cats.loc[cats["length"].idxmin()]
longest_fact = cats.loc[cats["length"].idxmax()]
save_table(cats, "task1_cat_facts")

print("Завдання 1")
print(cats.to_string(index=False))
print(f"\nНайкоротший факт ({shortest_fact['length']} символів): {shortest_fact['fact']}")
print(f"Найдовший факт ({longest_fact['length']} символів): {longest_fact['fact']}")


universities_url = "http://universities.hipolabs.com/search"
ukraine = pd.DataFrame(load_json(universities_url, {"country": "Ukraine"}))
poland = pd.DataFrame(load_json(universities_url, {"country": "Poland"}))
universities = pd.concat([ukraine, poland], ignore_index=True)
university_counts = universities["country"].value_counts().rename_axis("country").reset_index(name="count")
save_table(universities, "task2_universities")
save_table(university_counts, "task2_university_counts")

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(university_counts["country"], university_counts["count"], color=["#4f86f7", "#dc3545"])
ax.set_title("Кількість університетів")
ax.set_xlabel("Країна")
ax.set_ylabel("Кількість")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "task2_university_counts.png", dpi=160)
plt.close(fig)

print("\n\nЗавдання 2")
print(university_counts.to_string(index=False))
print(f"Загальна кількість: {len(universities)}")


europe_url = "https://restcountries.com/v3.1/region/europe"
europe_data = load_json(europe_url)

if not isinstance(europe_data, list):
    archive_url = "https://gist.githubusercontent.com/mertowitch/42898df6781aecd51fe53104e4175cb3/raw/country-list-v2.json"
    all_countries = load_json(archive_url)
    europe_data = [country for country in all_countries if country.get("region") == "Europe"]

country_rows = []

for country in europe_data:
    country_rows.append(
        {
            "name": country["name"]["common"],
            "capital": ", ".join(country.get("capital", [])),
            "population": country.get("population", 0),
            "area": country.get("area", 0),
            "languages": ", ".join(country.get("languages", {}).values()),
        }
    )

countries = pd.DataFrame(country_rows)
countries["density"] = countries["population"].div(countries["area"]).where(countries["area"].gt(0))
largest_area = countries.nlargest(5, "area")
largest_population = countries.nlargest(5, "population")
dense_countries = countries.nlargest(10, "density").sort_values("density")
save_table(countries, "task3_european_countries")
save_table(largest_area, "task3_top5_area")
save_table(largest_population, "task3_top5_population")

fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(countries["area"], countries["population"], alpha=0.7, color="#4169e1")
ax.set_title("Площа та населення країн Європи")
ax.set_xlabel("Площа, км²")
ax.set_ylabel("Населення")
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "task3_area_population.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(dense_countries["name"], dense_countries["density"], color="#2a9d8f")
ax.set_title("Топ-10 країн Європи за густотою населення")
ax.set_xlabel("Осіб на км²")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "task3_top10_density.png", dpi=160)
plt.close(fig)

print("\n\nЗавдання 3")
print("Топ-5 за площею")
print(largest_area[["name", "area"]].to_string(index=False))
print("\nТоп-5 за населенням")
print(largest_population[["name", "population"]].to_string(index=False))


forecast_params = {
    "latitude": 50.4501,
    "longitude": 30.5234,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "forecast_days": 14,
    "timezone": "Europe/Kyiv",
}
forecast_data = load_json("https://api.open-meteo.com/v1/forecast", forecast_params)["daily"]
weather = pd.DataFrame(
    {
        "date": pd.to_datetime(forecast_data["time"]),
        "temp_max": forecast_data["temperature_2m_max"],
        "temp_min": forecast_data["temperature_2m_min"],
        "rain": forecast_data["precipitation_sum"],
    }
)
average_temperature = weather[["temp_max", "temp_min"]].mean().mean()
minimum_temperature = weather["temp_min"].min()
maximum_temperature = weather["temp_max"].max()
rainiest_day = weather.loc[weather["rain"].idxmax()]
save_table(weather, "task4_kyiv_forecast")

fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(weather["date"], weather["temp_max"], marker="o", label="Максимальна")
ax.plot(weather["date"], weather["temp_min"], marker="o", label="Мінімальна")
ax.fill_between(weather["date"], weather["temp_min"], weather["temp_max"], alpha=0.2)
ax.set_title("Прогноз температури в Києві на 14 днів")
ax.set_xlabel("Дата")
ax.set_ylabel("Температура, °C")
ax.tick_params(axis="x", rotation=45)
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "task4_kyiv_temperature.png", dpi=160)
plt.close(fig)

print("\n\nЗавдання 4")
print(weather.to_string(index=False))
print(f"\nСередня температура: {average_temperature:.1f} °C")
print(f"Мінімальна температура: {minimum_temperature:.1f} °C")
print(f"Максимальна температура: {maximum_temperature:.1f} °C")
print(f"Найбільше опадів: {rainiest_day['date'].date()}, {rainiest_day['rain']:.1f} мм")


pokemon_rows = []

for pokemon_id in range(1, 31):
    pokemon = load_json(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    stats = {item["stat"]["name"]: item["base_stat"] for item in pokemon["stats"]}
    pokemon_rows.append(
        {
            "name": pokemon["name"].title(),
            "type": pokemon["types"][0]["type"]["name"].title(),
            "hp": stats["hp"],
            "attack": stats["attack"],
            "defense": stats["defense"],
            "speed": stats["speed"],
            "height": pokemon["height"],
            "weight": pokemon["weight"],
        }
    )

pokemons = pd.DataFrame(pokemon_rows)
strongest = pokemons.loc[pokemons["attack"].idxmax()]
fastest = pokemons.loc[pokemons["speed"].idxmax()]
heaviest = pokemons.loc[pokemons["weight"].idxmax()]
type_stats = pokemons.groupby("type")[["hp", "attack", "defense", "speed"]].mean().round(2)
type_counts = pokemons["type"].value_counts()
save_table(pokemons, "task5_pokemons")
save_table(type_stats.reset_index(), "task5_average_stats_by_type")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
type_counts.plot(kind="bar", ax=axes[0, 0], color="#457b9d")
axes[0, 0].set_title("Кількість покемонів за типом")
axes[0, 0].set_xlabel("Тип")
axes[0, 0].set_ylabel("Кількість")
axes[0, 0].tick_params(axis="x", rotation=45)

axes[0, 1].scatter(pokemons["attack"], pokemons["defense"], color="#e76f51", alpha=0.8)
axes[0, 1].set_title("Attack та Defense")
axes[0, 1].set_xlabel("Attack")
axes[0, 1].set_ylabel("Defense")

axes[1, 0].hist(pokemons["hp"], bins=8, color="#2a9d8f", edgecolor="white")
axes[1, 0].set_title("Розподіл HP")
axes[1, 0].set_xlabel("HP")
axes[1, 0].set_ylabel("Кількість")

type_stats["attack"].sort_values(ascending=False).plot(kind="bar", ax=axes[1, 1], color="#f4a261")
axes[1, 1].set_title("Середній Attack за типом")
axes[1, 1].set_xlabel("Тип")
axes[1, 1].set_ylabel("Середній Attack")
axes[1, 1].tick_params(axis="x", rotation=45)

fig.tight_layout()
fig.savefig(RESULTS_DIR / "task5_pokemon_subplots.png", dpi=160)
plt.close(fig)

print("\n\nЗавдання 5")
print(pokemons.to_string(index=False))
print(f"\nНайсильніший: {strongest['name']} — attack {strongest['attack']}")
print(f"Найшвидший: {fastest['name']} — speed {fastest['speed']}")
print(f"Найважчий: {heaviest['name']} — weight {heaviest['weight']}")
print("\nСередні характеристики за типом")
print(type_stats.to_string())


selected_countries = ["Ukraine", "Poland", "Germany", "France", "Italy"]
country_by_name = {item["name"]["common"]: item for item in europe_data}
capital_rows = []

for country_name in selected_countries:
    country = country_by_name[country_name]
    latitude, longitude = country["capitalInfo"]["latlng"]
    current = load_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "timezone": "auto",
        },
    )["current_weather"]
    capital_rows.append(
        {
            "country": country_name,
            "capital": country["capital"][0],
            "population": country["population"],
            "temperature": current["temperature"],
            "wind": current["windspeed"],
        }
    )

capitals = pd.DataFrame(capital_rows)
capitals.to_csv(RESULTS_DIR / "task6_capitals_weather.csv", index=False, encoding="utf-8-sig")
capitals.to_json(RESULTS_DIR / "task6_capitals_weather.json", orient="records", force_ascii=False, indent=2)

fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#4f86f7" if value >= 0 else "#6c9bd2" for value in capitals["temperature"]]
ax.bar(capitals["capital"], capitals["temperature"], color=colors)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("Поточна температура у п'яти столицях")
ax.set_xlabel("Столиця")
ax.set_ylabel("Температура, °C")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "task6_capital_temperatures.png", dpi=160)
plt.close(fig)

print("\n\nЗавдання 6")
print(capitals.to_string(index=False))
print(f"\nРезультати збережено в {RESULTS_DIR}")
