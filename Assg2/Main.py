from Assg2.Meadow import Meadow
from Assg2.Wolf import Wolf
from Assg2.Sheep import Sheep


def main():
    meadow = Meadow(sheep_count=5, wolf_count=2)

    print("Pozycja początkowa:")
    for animal_info in meadow.get_all_positions():
        print(animal_info)

    print("Pozycja po ruchu:")
    for animal in meadow.animals:
        meadow.move_animal(animal, 1, 1)

    for animal_info in meadow.get_all_positions():
        print(animal_info)



if __name__ == "__main__":
    main()
