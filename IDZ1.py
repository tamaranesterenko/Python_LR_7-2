# !/usr/bin/env python3
# -*- cosing: utf-8 -*-

import argparse
import json
import os
from dotenv import load_dotenv
import pathlib


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def add_worker(staff, surname, name, zodiac, year):
    staff.append(
        {
            'surname': surname,
            'name': name,
            'zodiac': zodiac,
            'year': year,
        }
    )

    return staff


def display_workers(staff):
    if staff:
        line = '+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} | {:^20} |'.format(
                "№",
                "Фамилия",
                "Имя",
                "Знак зодиака",
                "Год рождения"
            )
        )
        print(line)

        for idx, worker in enumerate(staff, 1):
            print(
                '| {:^4} | {:^30} | {:^20} | {:^15} | {:^20} |'.format(
                    idx,
                    worker.get('surname', ''),
                    worker.get('name', ''),
                    worker.get('zodiac', ''),
                    worker.get('year', 0),
                )
            )
        print(line)

    else:
        print("Список пуст.")


def select_workers(staff, period):
    result = []
    for worker in staff:
        if worker.get('year', 0) == period:
            result.append(worker)
    return result


def save_workers(data_file, staff):
    with open(data_file, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(data_file):
    with open(data_file, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )

    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new worker"
    )
    add.add_argument(
        "-s",
        "--surname",
        action="store",
        required=True,
        help="The worker`s surname"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The worker`s name"
    )
    add.add_argument(
        "-z",
        "--zodiac",
        action="store",
        required=True,
        help="The year of zodiac"
    )
    add.add_argument(
        "-y",
        "--year",
        action="store",
        type=int,
        required=True,
        help="The year of date_obj"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all workers"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the workers"
    )
    select.add_argument(
        "-P",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The required period"
    )

    args = parser.parse_args(command_line)
    data_file = pathlib.Path.home() / args.data

    is_dirty = False
    if os.path.exists(data_file):
        workers = load_workers(data_file)
    else:
        workers = []

    if args.command == "add":
        add_worker(
            workers,
            args.surname,
            args.name,
            args.zodiac,
            args.year
        )
        is_dirty = True

    elif args.command == "display":
        display_workers(workers)

    elif args.command == "select":
        selected = select_workers(workers, args.period)
        display_workers(selected)

    if is_dirty:
        save_workers(data_file, workers)


if __name__ == "__main__":
    main()
