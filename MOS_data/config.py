total_nq = 300
mos_nq = 25
sim_nq = 15
target_step = 10
n_LibriTTS_speaker = 38
n_VCTK_speaker = 108
n_sample = 16

model_list = ['real','recon','base_emb_vad','meta_emb_vad','base_emb1_vad','meta_emb1_vad']
dataset_list = ['LibriTTS','VCTK']
mode_list = ['mos','sim']


LibriTTS_mos_speaker_list = [11,5,14,10,25,15,36,2,22,13,26,8,35,12,33,37,1,3,18,17,30,29,4,9,34,27,32,6,7,21] 
LibriTTS_mos_testid_list = [191,86,233,166,407,254,579,42,357,213,418,140,575,201,537,600,29,50,290,272,486,467,76,150,549,446,516,103,123,337] 
LibriTTS_sim_speaker_list = [14,12,19,9,29,25,15,31,10,16,7,13,35,33,23,17,28,34,18,0,36,27,1,37,3,30,20,24,22,11]
LibriTTS_sim_testid_list = [233,201,316,150,467,412,251,499,175,271,123,221,563,542,375,277,456,555,294,8,578,445,16,607,56,481,327,395,362,188]
VCTK_mos_speaker_list = [36,55,68,27,17,26,5,59,78,23,7,72,28,39,16,101,75,35,70,53,98,82,37,52,65,81,18,71,93,24,22,25,104,19,76,79,95,96,43,67,33,73,32,102,74,6,42,92,21,94,41,51,80,54,15,31,99,50,105,9,10,3,29,34,62,14,11,100,56,38,64,44,4,77,2,60,87,106,13,103] 
VCTK_mos_testid_list = [588,895,1095,436,282,427,84,954,1260,368,124,1166,452,630,259,1629,1211,563,1132,849,1581,1317,599,840,1045,1309,290,1141,1492,389,355,413,1671,317,1217,1271,1525,1543,689,1081,530,1183,521,1635,1188,99,684,1487,343,1516,658,817,1286,875,251,506,1599,802,1680,150,173,62,465,555,998,233,184,1601,900,617,1032,717,73,1236,37,967,1392,1697,209,1661] 
VCTK_sim_speaker_list = [78,37,97,14,66,103,101,67,11,58,59,84,57,88,9,17,39,52,98,4,95,23,48,105,6,7,41,76,19,32,33,22,86,79,92,99,40,71,51,89,0,27,13,12,63,20,94,68,75,15,96,44,69,77,46,72,91,2,47,107,60,55,35,54,102,61,1,49,31,28,82,64,87,24,34,5,43,8,93,83] 
VCTK_sim_testid_list = [1249,594,1562,234,1065,1654,1619,1081,178,942,953,1352,925,1420,156,282,636,837,1568,64,1520,379,778,1686,100,120,659,1223,316,523,532,352,1381,1268,1482,1584,648,1146,823,1430,6,441,213,204,1016,334,1506,1095,1212,254,1549,718,1114,1239,748,1161,1456,42,764,1712,960,893,565,871,1635,987,30,790,496,450,1321,1038,1398,391,551,81,689,130,1497,1328] 

for i in range(30):
    assert(LibriTTS_mos_testid_list[i]//16==LibriTTS_mos_speaker_list[i])
    assert(LibriTTS_sim_testid_list[i]//16==LibriTTS_sim_speaker_list[i])
for i in range(80):
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
    source_dir_r = f'../..'
    if dataset == 'LibriTTS':
        data_dir_dict[dataset]['real'] = f'{source_dir_r}/LibriTTS/test-clean'
    elif dataset == 'VCTK':
        data_dir_dict[dataset]['real'] = f'{source_dir_r}/VCTK'
    source_dir = f'../../output/result/{dataset}'
    data_dir_dict[dataset]['recon'] = f'{source_dir}/672c4ace93c04b57a48911549ef0e609/base_emb_vad/audio/Testing'
    data_dir_dict[dataset]['base_emb_vad'] = f'{source_dir}/672c4ace93c04b57a48911549ef0e609/base_emb_vad/audio/Testing'
    data_dir_dict[dataset]['meta_emb_vad'] = f'{source_dir}/960dba64771045a9b1d4e48dd90b2270/meta_emb_vad/audio/Testing'
    data_dir_dict[dataset]['base_emb1_vad'] = f'{source_dir}/b3d4b916db01475d94fd690da6f25ae2/base_emb1_vad/audio/Testing'
    data_dir_dict[dataset]['meta_emb1_vad'] = f'{source_dir}/8f1d5e4c2db64bfd886d5f981b58974c/meta_emb1_vad/audio/Testing'

