from pathlib import Path

SOX = "sox"

def resize(
    wav_path: str,
    output_path: str,
    speed: float
) -> list[str]:
    return [
        SOX,
        wav_path,
        output_path,
        "tempo", "-s",
        str(speed)
    ]


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
