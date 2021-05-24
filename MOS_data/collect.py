import os
import shutil
import json
import random

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
        self.real_filelist = dict()
        for dataset in self.dataset_list:
            self.real_filelist[dataset] = dict()
            for mode in self.mode_list:
                self.real_filelist[dataset][mode] = dict()
        for model in self.model_list:
            for dataset in self.dataset_list:
                for mode in self.mode_list:
                    for sid,tid in self.speaker_testid_dict[dataset][mode].items():
                        # get source_path
                        if model == 'real':
                            source_filename = self.sq_list[dataset][tid]['qry_id'][0]
                            self.real_filelist[dataset][mode][sid] = source_filename
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
    
    def get_refer_file(self):
        # generate dir
        if not os.path.exists('refer'):
            os.mkdir('refer')
        for dataset in self.dataset_list:
            if not os.path.exists(os.path.join('refer',dataset)):
                os.mkdir(os.path.join('refer',dataset))
            if not os.path.exists(os.path.join('refer', dataset, 'sim')):
                os.mkdir(os.path.join('refer',dataset, 'sim'))
            for sid in self.speaker_testid_dict[dataset]['sim']:
                real_id = self.speaker_id_map[dataset][sid]
                if not os.path.exists(os.path.join('refer',dataset,'sim',real_id)):
                    os.mkdir(os.path.join('refer',dataset,'sim',real_id))
        # get refer_filelist and move file
        self.refer_filelist = dict()
        #     LibriTTS
        self.refer_filelist['LibriTTS'] = dict()
        for sid in self.speaker_testid_dict['LibriTTS']['sim']:
            # get available filelist
            filelist = set()
            real_id = self.speaker_id_map['LibriTTS'][sid]
            for subdir in os.listdir(os.path.join(self.data_dir_dict['LibriTTS']['real'],real_id)):
                wav_dir = os.path.join(self.data_dir_dict['LibriTTS']['real'],real_id,subdir)
                for filename in os.listdir(wav_dir):
                    if filename.endswith('.wav'):
                        filelist.add(filename)
            #   remove filename in self.real_filelist
            rm_fileset = set()
            rm_fileset.add(self.real_filelist['LibriTTS']['sim'][sid] + '.wav')
            filelist = filelist - rm_fileset
            # choose one file, add to self.refer_filelist
            refer_filename = random.choice(list(filelist))
            self.refer_filelist['LibriTTS'][sid] = refer_filename
            #copy to target dir
            sdir = refer_filename.split('_')[0]
            subdir = refer_filename.split('_')[1]
            source_path = os.path.join(self.data_dir_dict['LibriTTS']['real'], sdir, subdir, refer_filename)
            target_path = os.path.join('refer','LibriTTS','sim',sdir,refer_filename)
            shutil.copyfile(source_path, target_path)
        #     VCTK
        self.refer_filelist['VCTK'] = dict()
        for sid in self.speaker_testid_dict['VCTK']['sim']:
            # get available filelist
            filelist = set()
            real_id = self.speaker_id_map['VCTK'][sid]
            wav_dir = os.path.join(self.data_dir_dict['VCTK']['real'],real_id)
            for filename in os.listdir(wav_dir):
                if filename.endswith('.wav'):
                    filelist.add(filename)
            #   remove filename in self.real_filelist
            rm_fileset = set()
            rm_fileset.add(self.real_filelist['VCTK']['sim'][sid] + '.wav')
            filelist = filelist - rm_fileset
            # choose one file, add to self.refer_filelist
            refer_filename = random.choice(list(filelist))
            self.refer_filelist['VCTK'][sid] = refer_filename
            #copy to target dir
            sdir = refer_filename.split('_')[0]
            source_path = os.path.join(self.data_dir_dict['VCTK']['real'], sdir, refer_filename)
            target_path = os.path.join('refer','VCTK','sim',sdir,refer_filename)
            shutil.copyfile(source_path, target_path)

    
    def get_filelist(self):
        ## mos element ##
        # (wav_filename, script)
        ## sim element ##
        # (test_wav_filename, refer_wav_filename)
        self.mos_filelist = []
        self.sim_filelist = []
    
    
    def get_script(self, filepath):
        with open(filepath, 'r+') as f:
            lines = f.readlines()
        return lines[0].strip()

    def get_sheet_to_filelist_dict(self):
        pass


if __name__ == '__main__':
    main = collect()
    main.generate_dir()
    main.move_file()
    main.get_refer_file()
