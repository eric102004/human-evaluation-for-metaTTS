import os
import shutil
import json

import config

class collect:
    def __init__(self):
        self.target_step = config.target_step
        self.n_LibriTTS_speaker = config.n_LibriTTS_speaker
        self.n_VCTK_speaker = config.n_VCTK_speaker
        self.n_sample = config.n_sample
        self.model_list = config.model_list
        self.dataset_list = config.dataset_list
        self.mode_list = config.mode_list
        self.speaker_testid_dict = config.speaker_testid_dict
        self.data_dir_dict = config.data_dir_dict

        self.sq_list  = dict()
        with open('LibriTTS_SQids.json', 'r+') as f:
            self.sq_list['LibriTTS'] = json.load(f)
        with open('VCTK_SQids.json', 'r+') as f:
            self.sq_list['VCTK'] = json.load(f)

        self.get_speaker_id_map()


    def get_speaker_id_map(self):
        self.speaker_id_map = dict()  # pseudo id to actual id
        self.inv_speaker_id_map = dict() # actual id to pseudo id
        for dataset in self.dataset_list:
            self.speaker_id_map[dataset] = dict()
            self.inv_speaker_id_map[dataset]= dict()

        #LibriTTS
        for speaker_id in range(self.n_LibriTTS_speaker):
            search_dict = self.sq_list['LibriTTS'][speaker_id * self.n_sample]
            real_speaker_id = search_dict['qry_id'][0].split('_')[0]
            self.speaker_id_map['LibriTTS'][speaker_id] = real_speaker_id
            self.inv_speaker_id_map['LibriTTS'][real_speaker_id] = speaker_id
        #VCTK
        for speaker_id in range(self.n_VCTK_speaker):
            search_dict = self.sq_list['VCTK'][speaker_id * self.n_sample]
            real_speaker_id = search_dict['qry_id'][0].split('_')[0]
            self.speaker_id_map['VCTK'][speaker_id] = real_speaker_id
            self.inv_speaker_id_map['VCTK'][real_speaker_id] = speaker_id
        
 
    def generate_dir(self):
        for model in self.model_list:
            if not os.path.exists(model):
                os.mkdir(model)
            for dataset in self.dataset_list:
                if not os.path.exists(os.path.join(model, dataset)):
                    os.mkdir(os.path.join(model, dataset))
                for mode in self.mode_list:
                    if not os.path.exists(os.path.join(model, dataset, mode)):
                        os.mkdir(os.path.join(model, dataset, mode))
                    for sid in self.speaker_testid_dict[dataset][mode]:
                        if not os.path.exists(os.path.join(model,dataset,mode,self.speaker_id_map[dataset][sid])):
                            os.mkdir(os.path.join(model,dataset,mode,self.speaker_id_map[dataset][sid]))


    def move_file(self):
        for model in self.model_list:
            for dataset in self.dataset_list:
                for mode in self.mode_list:
                    for sid,tid in self.speaker_testid_dict[dataset][mode].items():
                        # get source_path
                        if model == 'real':
                            source_filename = self.sq_list[dataset][tid]['qry_id'][0]
                            if dataset == 'LibriTTS':
                                sdir = source_filename.split('_')[0]
                                subdir = source_filename.split('_')[1]
                                source_wav_filename = source_filename + '.wav'
                                source_lab_filename = source_filename + '.original.txt'
                                source_wav_path = os.path.join(self.data_dir_dict[dataset][model],sdir,subdir, source_filename+'.wav')
                                source_lab_path = os.path.join(self.data_dir_dict[dataset][model],sdir,subdir, source_filename+'.original.txt')
                            elif dataset == 'VCTK':
                                sdir = source_filename.split('_')[0]
                                source_wav_filename = source_filename + '.wav'
                                source_lab_filename = source_filename + '.lab'
                                source_wav_path = os.path.join(self.data_dir_dict[dataset][model],sdir,source_filename+'.wav')
                                source_lab_path = os.path.join(self.data_dir_dict[dataset][model],sdir,source_filename+'.lab')
                        else:
                            wav_dir = os.path.join(self.data_dir_dict[dataset][model], f'test_{tid:03d}')
                            if model == 'recon':
                                for filename in os.listdir(wav_dir):
                                    if filename.endswith('recon.wav'):
                                        source_wav_filename = filename
                                        source_path = os.path.join(wav_dir, filename)
                                        break
                            else:
                                for filename in os.listdir(wav_dir):
                                    if filename.endswith(f'_{self.target_step}.synth.wav'):
                                        source_wav_filename = filename
                                        source_path = os.path.join(wav_dir, filename)
                                        break
                        #get target path
                        target_wav_path = os.path.join(model, dataset, mode,self.speaker_id_map[dataset][sid], source_wav_filename)
                        if model == 'real':
                            target_lab_path = os.path.join(model , dataset, mode,self.speaker_id_map[dataset][sid], source_lab_filename)
                        # move file
                        #print('source_wav_path:',source_wav_path)
                        #print('target_wav_path:',target_wav_path)
                        shutil.copyfile(source_wav_path, target_wav_path) 
                        if model == 'real':
                            #print('source_lab_path:',source_lab_path)
                            #print('target_lab_path:',target_lab_path)
                            shutil.copyfile(source_lab_path, target_lab_path)
    def get_file_script(self):
        pass

    def get_sheet_to_filelist_dict(self):
        pass


if __name__ == '__main__':
    main = collect()
    main.generate_dir()
    main.move_file()
