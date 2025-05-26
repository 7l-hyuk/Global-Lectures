from pathlib import Path


def sync(
    input_file_path: Path,
    output_file_path: Path,
    speed: float
) -> list[str]:
    return [
        "sox",
        input_file_path,
        output_file_path,
        "tempo",
        str(speed)
    ]


def merge_audio(
    segments: list[dict],
    output_file_path: Path
) -> str:
    command = ["sox", "-m"]

    for segment in segments:
        command.append(f'"|sox {segment["file"]} -p pad {segment["start"]}"')
    command.append(str(output_file_path))
    return " ".join(command)
