#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment
import json
import sys
import os
import argparse
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open('MOS_data/sim_sheet2file.json') as f:
    sim_sheet2file= json.load(f)
    assert(len(sim_sheet2file)==44)
    assert(len(sim_sheet2file[0])==15)

def main(form_id):
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("pair_comparison.html.jinja2")


    filelist = sim_sheet2file[form_id-30]

    num_q = 15
    
    html = template.render(
        page_title=f"語者判別實驗表單 {form_id-30}",
        form_url="https://script.google.com/macros/s/AKfycbzRkXi7oW_2uMlZpwIgM2rNwyOM4slGHtubS__AcmU0wV-vS6ldM6g8lCLbqSb9QiR3/exec",
        form_id=form_id,
        questions=[
            {
                "title": f"問題 {index}",
                "audio_paths": [
                    filelist[index-1][1],
                    filelist[index-1][0]
                ],
                "name": f"q{index}"
            } for index in range(1,num_q+1)]
    )
    print(html)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--form_id",type=int)
    args = parser.parse_args()
    main(args.form_id)
