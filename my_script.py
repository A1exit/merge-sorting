import json
import argparse

from pathlib import Path


def _merge_logs(path_to_logs_1, path_to_logs_2, output_file: Path) -> None:
    with open(path_to_logs_1.name, 'r', encoding='utf-8') as file1, \
            open(path_to_logs_2.name, 'r', encoding='utf-8') as file2, \
            open(output_file.name, 'w+', encoding='utf-8') as output_file:
        try:
            line_1 = file1.readline()
            line_2 = file2.readline()
            while True:
                if line_1 and line_2:
                    if json.loads(line_1).get('timestamp') <= json.loads(
                            line_2).get('timestamp'):
                        output_file.write(line_1)
                        line_1 = file1.readline()
                    else:
                        output_file.write(line_2)
                        line_2 = file2.readline()
                elif line_1 and not line_2:
                    output_file.write(line_1)
                    line_1 = file1.readline()
                elif not line_1 and line_2:
                    output_file.write(line_2)
                    line_2 = file2.readline()
                elif not line_1 and not line_2:
                    break
        finally:
            file1.close()
            file2.close()
            output_file.close()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge logs')

    parser.add_argument(
        'input_file_1',
        type=Path,
        help='path to the first log file',
    )

    parser.add_argument(
        'input_file_2',
        type=Path,
        help='the path to the second log file',
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='path to output file',
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    input_file_1 = Path(args.input_file_1)
    input_file_2 = Path(args.input_file_2)
    output_file = Path(args.output)
    _merge_logs(input_file_1, input_file_2, output_file)


if __name__ == '__main__':
    main()
