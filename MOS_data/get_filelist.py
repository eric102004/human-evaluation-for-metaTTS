import os
import random
from sheet_file_dict import sheet_file_dict_nat, sheet_file_dict_sim
#sheet_file_dict = dict()

def get_filelist_naturalness():
    '''
    filelist = []
    dir_list = os.listdir('.')
    for dirname in dir_list:
        if dirname.endswith('.py'):
            dir_list.remove(dirname)
    dir_list.remove('reference')
    for dirname in dir_list:
        for speaker in os.listdir(dirname):
            filename = os.listdir(os.path.join(dirname, speaker))[0]
            filepath = os.path.join('MOS_data',dirname,speaker, filename)
            filelist.append(filepath)

    random.shuffle(filelist)

    for i in range(29):
        sheet_file_dict[i] = filelist[20*i:20*(i+1)]
    sheet_file_dict[29] = filelist[20*29:]
    print(sheet_file_dict)
    '''
    for speaker in sheet_file_dict_nat.keys():
        print(speaker, sheet_file_dict_nat[speaker])

def get_filelist_similarity():
    '''
    filelist = []
    sheet_file_dict_sim = dict()
    dir_list = os.listdir('.')
    for dirname in dir_list:
        if dirname.endswith('.py'):
            dir_list.remove(dirname)
    dir_list.remove('reference')
    dir_list.remove('__pycache__')
    for dirname in dir_list:
        for speaker in os.listdir(dirname):
            filename_gen = os.listdir(os.path.join(dirname, speaker))[0]
            filename_ref = os.listdir(os.path.join('reference', speaker))[0]
            filepath_gen = os.path.join('MOS_data',dirname,speaker, filename_gen)
            filepath_ref = os.path.join('MOS_data','reference',speaker, filename_ref)
            filelist.append((filepath_ref,filepath_gen))

    random.shuffle(filelist)

    for i in range(49):
        sheet_file_dict_sim[i] = filelist[12*i:12*(i+1)]
    sheet_file_dict_sim[49] = filelist[12*49:]
    print(sheet_file_dict_sim)
    '''
    for form_id in sheet_file_dict_sim.keys():
        print(form_id, len(sheet_file_dict_sim[form_id]))


if __name__ == '__main__':
    get_filelist_similarity()
