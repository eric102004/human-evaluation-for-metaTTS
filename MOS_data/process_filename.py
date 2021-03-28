import os
import shutil

def process_filename(mode, shot):
    if mode in {'real','reference'}:
        dirname = mode
    else:
        dirname = f'{mode}_shot{shot}'
    subdir_list = os.listdir(dirname)
    for subdir in subdir_list:
        file_dir = os.path.join(dirname, subdir)
        source_filename = os.listdir(file_dir)[0]
        source_filepath = os.path.join(file_dir, source_filename)
        if mode in {'real','reference'}:
            target_filename = f'{mode}_{subdir}.wav'
        else:
            target_filename = f'{mode}_{shot}_{subdir}.wav'
        target_filepath = os.path.join(file_dir, target_filename)
        shutil.copyfile(source_filepath, target_filepath)

if __name__ == '__main__':
    mode_list = ['baseline_emb','baseline_ft','baseline_emb_ftemb','meta_emb','meta_ft']
    shot_list = [1,5,20]
    for mode in mode_list:
        for shot in shot_list:
            process_filename(mode, shot)
    #process_filename('reference',1)
