import argparse
import configparser
import os
import sys
import logging

from Meadow import Meadow


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Simulation of a wolf chasing sheep in a meadow."
    )
    parser.add_argument("-s", "--sheep", type=int, help="Number of sheep.")
    parser.add_argument("-r", "--rounds", type=int, help="Maximum number of rounds.")
    parser.add_argument("-c", "--config", type=str, help="Configuration file.")
    parser.add_argument("-w", "--wait", action="store_true", help="Pause after each round.")
    parser.add_argument("-l", "--log", type=str, default=None,
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level (default: NONE).")
    return parser.parse_args()


def setup_logging(log_level=None):
    if os.path.exists("chase.log"):
        os.remove("chase.log")
        print("Existing log file 'chase.log' removed.")

    if log_level:
        print(log_level)
        logging.basicConfig(filename="chase.log", level=log_level.upper(),
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging started.")


def load_config(file_path=None):
    config = configparser.ConfigParser()
    if file_path:
        try:
            config.read(file_path)
            if not config.sections():
                print(f"Config file '{file_path}' is empty or invalid. Using default values.")
            else:
                logging.debug(f"Configuration loaded from '{file_path}'.")
                for section in config.sections():
                    for key, value in config.items(section):
                        logging.debug(f"Loaded [{section}] {key} = {value}")
        except FileNotFoundError:
            print(f"Config file '{file_path}' not found. Using default values.")
        except configparser.Error as error:
            print(f"Error reading config file: {error}")
            sys.exit(1)
    else:
        config["Sheep"] = {
            "InitPosLimit": "10.0",
            "MoveDist": "0.5",
        }
        config["Wolf"] = {
            "MoveDist": "1"
        }
        logging.info("No config file provided. Using default configuration.")
        for section in config.sections():
            for key, value in config.items(section):
                logging.debug(f"Using default [{section}] {key} = {value}")

    return config


def main():
    args = parse_arguments()

    setup_logging(args.log)

    config = load_config(args.config)

    try:
        sheep_pos_limit = float(config.get("Sheep", "InitPosLimit", fallback=10.0))
        sheep_move_dist = float(config.get("Sheep", "MoveDist", fallback=0.5))
        wolf_move_dist = float(config.get("Wolf", "MoveDist", fallback=1.0))

        sheep_count = args.sheep if args.sheep is not None else int(config.get("Settings", "sheep_count", fallback=15))
        max_rounds = args.rounds if args.rounds is not None else int(config.get("Settings", "max_rounds", fallback=50))
    except KeyError as e:
        logging.error(f"Missing configuration value: {e}")
        sys.exit(1)

    if sheep_pos_limit < 0 or sheep_move_dist < 0 or wolf_move_dist < 0:
        logging.error(f"Missing configuration value: {e}")
        sys.exit(1)

    meadow = Meadow(sheep_count, max_rounds, sheep_pos_limit, sheep_move_dist, wolf_move_dist)
    while meadow.start_simulation():
        status = meadow.get_status()
        round_number = status['round']
        wolf_position = status['wolf_position']
        sheep_count_left = status['sheep_count']

        print(f"Round {round_number} - Wolf position: ({wolf_position[0]:.3f}, {wolf_position[1]:.3f}) "
              f"- Alive sheep: {sheep_count_left}")

        if args.wait:
            input("Press Enter to continue...")

    print("Simulation finished.")


if __name__ == "__main__":
    main()
