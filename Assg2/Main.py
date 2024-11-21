from Assg2.Meadow import Meadow


def main():
    meadow = Meadow(15, 50)
    while meadow.start_simulation():
        print(
            f"Round {meadow.get_status()['round']} - Sheeps left on the meadow: "
            f"{meadow.get_status()['sheep_count']} - Wolf position: "
            f"{meadow.get_status()['wolf_position']}")
    print("Simulation finished.")


if __name__ == "__main__":
    main()
