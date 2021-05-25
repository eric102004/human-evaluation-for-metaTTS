#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment
import json
import sys
import os
import argparse
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open('MOS_data/mos_sheet2file.json') as f:
    mos_sheet2file = json.load(f)
    assert(len(mos_sheet2file)==30)
    assert(len(mos_sheet2file[0])==22)

def main(form_id):
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    filelist = mos_sheet2file[form_id]
    #filelist_row = sheet_file_dict_nat[form_id]
    #filelist = [os.path.join('https://github.com/eric102004/human-evaluation-for-metaTTS/blob/master', filepath)+'?raw=true' for filepath in filelist_row ]
    #print(filelist)
    num_q =22
    ''' 
    script = []
    num_q = 22
    for i in range(num_q):
        speaker_id = filelist[i].split('/')[-2]
        sentence = speaker_sen_dict[speaker_id] 
        script.append(sentence)
    '''
    html = template.render(
        page_title=f"MOS 實驗表單 {form_id}",
        form_url="https://script.google.com/macros/s/AKfycbwq551Zbsn_G7UPPpTL_FFHFBV_g0edf88U0C-3denwbla6leuaTIYYt_fFPQaWXgw/exec",
        form_id=form_id,
        questions=[
            {
                "title": f"問題 {index}",
                "script": filelist[index-1][1],
                "audio_path": filelist[index-1][0],
                "name": f"q{index}"
            } for index in range(1,num_q+1)],
    )
    print(html)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--form_id", type=int)
    args = parser.parse_args()
    main(args.form_id)
