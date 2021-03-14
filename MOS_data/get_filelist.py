import os
import random
from sheet_file_dict import sheet_file_dict_nat, sheet_file_dict_sim
#sheet_file_dict = dict()

def get_filelist_naturalness():
    '''
    filelist = []
    sheet_file_dict_nat = dict()
    dir_list = os.listdir('.')
    for dirname in dir_list:
        if dirname.endswith('.py'):
            dir_list.remove(dirname)
    dir_list.remove('reference')
    dir_list.remove('__pycache__')
    modelist1 = ['baseline_emb', 'baseline_emb_ftemb','baseline_ft','meta_emb','meta_ft']
    modelist2 = ['real']
    for mode in modelist1:
        for shot in [1,5,20]:
            dirname = f'{mode}_shot{shot}'
            for speaker in os.listdir(dirname):
                #filename = os.listdir(os.path.join(dirname, speaker))[0]
                filename = f'{mode}_{shot}_{speaker}.wav'
                filepath = os.path.join('MOS_data',dirname,speaker, filename)
                filelist.append(filepath)
    for mode in modelist2: 
        dirname = mode
        for speaker in os.listdir(dirname):
            #filename = os.listdir(os.path.join(dirname, speaker))[0]
            filename = f'{mode}_{speaker}.wav'
            filepath = os.path.join('MOS_data',dirname,speaker, filename)
            filelist.append(filepath)

    random.shuffle(filelist)

    for i in range(29):
        sheet_file_dict_nat[i] = filelist[20*i:20*(i+1)]
    sheet_file_dict_nat[29] = filelist[20*29:]
    print(sheet_file_dict_nat)
    '''
    for speaker in sheet_file_dict_nat.keys():
        print(speaker, len(sheet_file_dict_nat[speaker]))
    
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
    modelist1 = ['baseline_emb', 'baseline_emb_ftemb','baseline_ft','meta_emb','meta_ft']
    modelist2 = ['real']
    for mode in modelist1:
        for shot in [1,5,20]:
            dirname = f'{mode}_shot{shot}'
            for speaker in os.listdir(dirname):
                filename_gen = f'{mode}_{shot}_{speaker}.wav'
                filename_ref = f'reference_{speaker}.wav'
                filepath_gen = os.path.join('MOS_data',dirname,speaker, filename_gen)
                filepath_ref = os.path.join('MOS_data','reference',speaker, filename_ref)
                filelist.append((filepath_ref,filepath_gen))
    for mode in modelist2:
        dirname = mode
        for speaker in os.listdir(dirname):
            filename_gen = f'{mode}_{speaker}.wav'
            filename_ref = f'reference_{speaker}.wav'
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
    #get_filelist_naturalness()
    get_filelist_similarity()
