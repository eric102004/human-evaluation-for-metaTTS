target_step = 10
n_LibriTTS_speaker = 38
n_VCTK_speaker = 108
n_sample = 16

model_list = ['real','recon','base_emb_vad','meta_emb_vad','base_emb1_vad','meta_emb1_vad']
dataset_list = ['LibriTTS','VCTK']
mode_list = ['mos','sim']


LibriTTS_mos_speaker_list = [11,5,14,10,25,15,36,2,22,13,26,8,35,12,33,37,1,3,18,17] 
LibriTTS_mos_testid_list = [191,86,233,166,407,254,579,42,357,213,418,140,575,201,537,600,29,50,290,272] 
LibriTTS_sim_speaker_list = [14,12,15,25,19,10,31,7,9,13,16,0,29,20,18,28,22,23,27,3]
LibriTTS_sim_testid_list = [233,201,240,402,309,175,501,112,157,209,269,8,466,327,301,456,360,377,432,56]
VCTK_mos_speaker_list = [36,55,68,27,17,26,5,59,78,23,7,72,28,39,16,101,75,35,70,53,98,82,37,52,65,81,18,71,93,24] 
VCTK_mos_testid_list = [588,895,1095,436,282,427,84,954,1260,368,124,1166,452,630,259,1629,1211,563,1132,849,1581,1317,599,840,1045,1309,290,1141,1492,389] 
VCTK_sim_speaker_list = [78,97,37,14,9,59,4,66,57,84,52,95,17,23,75,98,7,92,105,11,88,51,101,99,15,76,96,58,6,13] 
VCTK_sim_testid_list = [1249,1558,594,234,156,955,74,1060,914,1352,837,1520,282,368,1212,1568,120,1482,1692,178,1410,823,1621,1584,246,1223,1549,933,103,213] 

for i in range(20):
    assert(LibriTTS_mos_testid_list[i]//16==LibriTTS_mos_speaker_list[i])
    assert(LibriTTS_sim_testid_list[i]//16==LibriTTS_sim_speaker_list[i])
    assert(VCTK_mos_testid_list[i]//16==VCTK_mos_speaker_list[i])
    assert(VCTK_sim_testid_list[i]//16==VCTK_sim_speaker_list[i])

speaker_testid_dict = dict()
for data in dataset_list:
    speaker_testid_dict[data] = dict()
speaker_testid_dict['LibriTTS']['mos'] = {s:t for s,t in zip(LibriTTS_mos_speaker_list,LibriTTS_mos_testid_list)}
speaker_testid_dict['LibriTTS']['sim'] = {s:t for s,t in zip(LibriTTS_sim_speaker_list,LibriTTS_sim_testid_list)}
speaker_testid_dict['VCTK']['mos'] = {s:t for s,t in zip(VCTK_mos_speaker_list,VCTK_mos_testid_list)}
speaker_testid_dict['VCTK']['sim'] = {s:t for s,t in zip(VCTK_sim_speaker_list,VCTK_sim_testid_list)}

data_dir_dict = dict()
for dataset in dataset_list:
    data_dir_dict[dataset] = dict()
    if dataset == 'LibriTTS':
        data_dir_dict[dataset]['real'] = '~/remote_disk/LibriTTS/test-clean'
    elif dataset == 'VCTK':
        data_dir_dict[dataset]['real'] = '~/remote_disk/VCTK'
    source_dir = f'~/remote_disk/output/result/{dataset}'
    data_dir_dict[dataset]['recon'] = f'{source_dir}/672c4ace93c04b57a48911549ef0e609/base_emb_vad/audio/Testing'
    data_dir_dict[dataset]['base_emb_vad'] = f'{source_dir}/672c4ace93c04b57a48911549ef0e609/base_emb_vad/audio/Testing'
    data_dir_dict[dataset]['meta_emb_vad'] = f'{source_dir}/960dba64771045a9b1d4e48dd90b2270/meta_emb_vad/audio/Testing'
    data_dir_dict[dataset]['base_emb1_vad'] = f'{source_dir}/b3d4b916db01475d94fd690da6f25ae2/base_emb1_vad/audio/Testing'
    data_dir_dict[dataset]['meta_emb1_vad'] = f'{source_dir}/8f1d5e4c2db64bfd886d5f981b58974c/meta_emb1_vad/audio/Testing'

