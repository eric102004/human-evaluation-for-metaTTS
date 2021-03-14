#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment
import sys
import os
import argparse
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from MOS_data.sheet_file_dict import sheet_file_dict_sim

def main(form_id):
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("pair_comparison.html.jinja2")


    filelist_row = sheet_file_dict_sim[form_id]
    filelist = []
    for file_real, file_gen in filelist_row:
        file_real_path = os.path.join('https://github.com/eric102004/human-evaluation-for-metaTTS/blob/master', file_real) + '?raw=true'
        file_gen_path = os.path.join('https://github.com/eric102004/human-evaluation-for-metaTTS/blob/master', file_gen) + '?raw=true'
        filelist.append((file_real_path, file_gen_path))
    
    if form_id<49:
        num_q = 12
    elif form_id == 49:
        num_q = 11
    
    html = template.render(
        page_title=f"語者判別實驗表單 {form_id}",
        form_url="https://script.google.com/macros/s/AKfycbyeCBqch0-qhvc3_-ummqt1H6rWAt5SfaNudfiwbRThf7rDRzPpbPT1FuMGbOZXBHPm/exec",
        form_id=form_id,
        questions=[
            {
                "title": f"問題 {index}",
                "audio_paths": [
                    filelist[index-1][0],
                    filelist[index-1][1]
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
