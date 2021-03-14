#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def main(form_id, num_type):
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    script = ['script1']*num_type + ['script2']*num_type + ['script3']*num_type + ['script4']*num_type
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
            } for index in range(1,num_type*4+1)],
    )
    print(html)


if __name__ == "__main__":
    main(1,6)
