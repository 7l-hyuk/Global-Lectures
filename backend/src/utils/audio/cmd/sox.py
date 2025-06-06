from pathlib import Path

SOX = "sox"

def sync(
    input_file_path: Path,
    output_file_path: Path,
    speed: float
) -> list[str]:
    return [
        SOX,
        input_file_path,
        output_file_path,
        "tempo", "-s",
        str(speed)
    ]


# TODO: 싱크가 정확히 안 맞음
def merge_audio(
    segments: list[dict],
    output_file_path: Path
) -> str:
    temp_output = output_file_path.with_suffix(".temp.wav")

    command = [SOX, "-m"]
    for segment in segments:
        command.append(f'"|sox {segment["file"]} -p pad {segment["start"]}"')
    command.append(str(temp_output))

    # Step 1: mix all files into temp file
    mix_command = " ".join(command)

    # Step 2: normalize gain
    gain_command = f'sox {temp_output} {output_file_path} gain -n'

    # Combine the two commands with && so the second runs only if the first succeeds
    return f"{mix_command} && {gain_command} && rm {temp_output}"
