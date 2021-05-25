import os
import shutil
import json
import random

import config

class collect:
    def __init__(self):
        self.total_nq = config.total_nq
        self.mos_nq = config.mos_nq      # 300 / 25 = 12
        self.sim_nq = config.sim_nq      # 300 / 15 = 20
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
        # get enroll filelist
        self.refer_filelist = dict()
        for dataset in self.dataset_list:
            self.refer_filelist[dataset] = dict()
            # get enrollment filelist:
            with open(f'{dataset}_enroll.txt', 'r+') as f:
                lines = f.readlines()
            for i,line in enumerate(lines):
                if line.strip() == '':
                    continue
                sid = int(line.strip().split('\t')[1])
                assert(sid in self.speaker_testid_dict[dataset]['sim'])
                enroll = line.strip().split('\t')[3] + '.wav'
                self.refer_filelist[dataset][sid] = enroll
        # move file
        for dataset in self.dataset_list:
            for sid,r_file in self.refer_filelist[dataset].items():
                real_id = self.speaker_id_map[dataset][sid]
                if dataset == 'LibriTTS':
                    subdir = r_file.split('_')[1]
                    source_path = os.path.join(self.data_dir_dict[dataset]['real'],real_id,subdir,r_file)
                else:
                    source_path = os.path.join(self.data_dir_dict[dataset]['real'],real_id,r_file)
                target_path = os.path.join('refer',dataset,'sim',real_id,r_file)
                shutil.copyfile(source_path, target_path)
        '''
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

        with open('refer_file_dict.json', 'w') as f:
            json.dump(self.refer_filelist, f)
        '''
    def get_filelist(self):
        ## mos element ##
        # (wav_fileurl, script)
        ## sim element ##
        # (test_wav_fileurl, refer_wav_fileurl)
        suffix_dict = {'LibriTTS':'original.txt', 'VCTK':'.lab'}
        self.mos_filelist = []
        self.sim_filelist = []
        url_pref = 'https://github.com/eric102004/human-evaluation-for-metaTTS/blob/master/MOS_data'
        url_suf = '?raw=true'
        # collect mos filelist
        for model in self.model_list:
            for dataset in self.dataset_list:
                for sid in self.speaker_testid_dict[dataset]['mos']:
                    real_id = self.speaker_id_map[dataset][sid]
                    # get wav_fileurl
                    for fn in os.listdir(os.path.join(model, dataset, 'mos',real_id)):
                        if fn.endswith('.wav'):
                            wav_fn = fn
                            break
                    wav_fileurl = os.path.join(url_pref, model,dataset,'mos',real_id,wav_fn)+url_suf
                    # get script
                    for fn in os.listdir(os.path.join('real',dataset,'mos',real_id)):
                        if fn.endswith(suffix_dict[dataset]):
                            script = self.get_script(os.path.join('real',dataset,'mos',real_id,fn))
                            break
                    self.mos_filelist.append((wav_fileurl, script))
        assert(len(self.mos_filelist)==self.total_nq)
        # collect sim filelist
        for model in self.model_list:
            for dataset in self.dataset_list:
                for sid in self.speaker_testid_dict[dataset]['sim']:
                    real_id = self.speaker_id_map[dataset][sid]
                    # get test_wav_fileurl
                    for fn in os.listdir(os.path.join(model, dataset, 'sim',real_id)):
                        if fn.endswith('.wav'):
                            wav_fn = fn
                            break
                    test_wav_fileurl = os.path.join(url_pref, model,dataset,'sim',real_id,wav_fn)+url_suf
                    # get refer_wav_fileurl
                    for fn in os.listdir(os.path.join('refer',dataset,'sim',real_id)):
                        if fn.endswith('.wav'):
                            wav_fn = fn
                            break
                    refer_wav_fileurl = os.path.join(url_pref,'refer',dataset,'sim',real_id,wav_fn)+url_suf
                    self.sim_filelist.append((test_wav_fileurl, refer_wav_fileurl))
        assert(len(self.sim_filelist)==self.total_nq)

        # shuffle filelist
        random.shuffle(self.mos_filelist)
        random.shuffle(self.sim_filelist)

        with open('mos_filelist.json', 'w') as f:
            json.dump(self.mos_filelist, f)
        with open('sim_filelist.json', 'w') as f:
            json.dump(self.sim_filelist, f)

    
    def get_script(self, filepath):
        with open(filepath, 'r+') as f:
            lines = f.readlines()
        return lines[0].strip()

    def load_filelist(self):
        with open('mos_filelist.json', 'r') as f:
            self.mos_filelist = json.load(f)
        with open('sim_filelist.json', 'r') as f:
            self.sim_filelist = json.load(f)


    def get_sheet2file_matrix(self):
        self.mos_sheet2file_matrix = []
        for i in range(self.total_nq//self.mos_nq):
            self.mos_sheet2file_matrix.append(self.mos_filelist[i*self.mos_nq:(i+1)*self.mos_nq])
        self.sim_sheet2file_matrix = []
        for i in range(self.total_nq//self.sim_nq):
            self.sim_sheet2file_matrix.append(self.sim_filelist[i*self.sim_nq:(i+1)*self.sim_nq])
        
        with open('mos_sheet2file.json', 'w') as f:
            json.dump(self.mos_sheet2file_matrix, f)
        with open('sim_sheet2file.json', 'w') as f:
            json.dump(self.sim_sheet2file_matrix, f)


if __name__ == '__main__':
    main = collect()
    main.generate_dir()
    main.move_file()
    main.get_refer_file()
    main.get_filelist()
    main.load_filelist()
    main.get_sheet2file_matrix()
