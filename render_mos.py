#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment
import sys
import os
import argparse
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from MOS_data.sheet_file_dict import sheet_file_dict_nat
from MOS_data.speaker_sen import speaker_sen_dict

def main(form_id):
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    filelist_row = sheet_file_dict_nat[form_id]
    filelist = [os.path.join('https://github.com/eric102004/human-evaluation-for-metaTTS/blob/master', filepath)+'?raw=true' for filepath in filelist_row ]
    #print(filelist)
   
    script = []
    if form_id<29:
        num_q = 20
    elif form_id==29:
        num_q = 19
    for i in range(num_q):
        speaker_id = filelist[i].split('/')[-2]
        sentence = speaker_sen_dict[speaker_id] 
        script.append(sentence)
    
    html = template.render(
        page_title=f"MOS 實驗表單 {form_id}",
        form_url="https://script.google.com/macros/s/AKfycbys0SzKRa--zMxnDAIIXEWGAnkh2HOWC5zUD9eaQphn5KvyIOMYx9Ezd08PRqv21C67/exec",
        form_id=form_id,
        questions=[
            {
                "title": f"問題 {index}",
                "script": script[index-1],
                "audio_path": filelist[index-1],
                "name": f"q{index}"
            } for index in range(1,num_q+1)],
    )
    print(html)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--form_id", type=int)
    args = parser.parse_args()
    main(args.form_id)
