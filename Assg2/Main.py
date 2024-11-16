from Assg2.Meadow import Meadow


def main():
    meadow = Meadow(15, 50)
    while meadow.start_simulation():
        print(
            f"Runda {meadow.get_status()['runda']} - Liczba pozostałych owiec na łące: "
            f"{meadow.get_status()['liczba_owiec']} - Pozycja wilka: "
            f"{meadow.get_status()['pozycja_wilka']}")
    print("Symulacja zakończona.")


if __name__ == "__main__":
    main()
