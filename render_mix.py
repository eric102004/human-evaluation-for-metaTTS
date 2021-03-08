#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mix.html.jinja2")

    form_id = 4
    script = ['script7']*5 + ['script8']*5
    html = template.render(
        page_title=f"MOS 實驗表單 {form_id}",
        form_url="https://script.google.com/macros/s/AKfycbyOYo43xTRKdQDReFUvv4ILAmBW3P26M2Drs4wdfSRzSrayGtxPpe4kmz3KNBkeYMq13w/exec",
        form_id=form_id,
        questions=[
            {
                "title": f"問題 {index}",
                "script": script[index-1],
                "audio_path": f"wavs/test_{form_id}_{index}.wav",
                "name": f"q{index}"
            } for index in range(1,11)],
        questions_pair=[
            {
                "title": f"問題 {index}",
                "audio_paths": [
                    f"wavs/test_{form_id}_{index}_real.wav",
                    f"wavs/test_{form_id}_{index}_gen.wav"
                ],
                "name": f"q{index}"
            } for index in range(11,21)],
    )
    print(html)


if __name__ == "__main__":
    main()
