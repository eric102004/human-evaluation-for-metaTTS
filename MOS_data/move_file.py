import os
import shutil

speaker_sen_dict = {'1221': '"I have no Heavenly Father!"', '3729': '"Here, go and get me change for a Louis."', '1188': 'Then he comes to the beak of it.', '5105': 'Side by side they fought in two campaigns.', '7176': 'The Fisher in the Chutes', '7127': '"Certainly, sire; but I must have money to do that."', '4992': '"Perhaps I am mistaken," answered she.', '121': 'Hence, full of strains.', '4507': 'Where are we at this moment?', '672': 'What is it like?"', '5639': 'In mercy kill me this moment!', '260': 'The horizon seems extremely distant.', '3570': 'Any such consumption by others can take place only on a basis of sufferance.', '2300': 'This does him an injustice.', '8455': '"We are quite satisfied now, Captain Battleax," said my wife.', '1580': '"I should much prefer that you called in the aid of the police."', '7729': 'This was at the March election, 1855.', '3575': 'Why are we to be divided?', '4446': "She's apt to grow a bit stale after a time.", '8463': 'It is hardly necessary to say more of them here.', '8555': 'But you were mistaken.', '8224': 'or hath he given us any gift?', '6930': 'Concord returned to its place amidst the tents.', '2830': 'This is a LibriVox recording.', '908': 'born but to smile & fall. Ah!', '1320': 'Has Uncas no counsel to offer in such a strait?"', '2961': 'Socrates begins the Timaeus with a summary of the Republic.', '5142': 'There, far off, is my country, across the water.', '8230': 'What sort of evidence is there?', '5683': 'THE ACE OF HEARTS.', '4970': '"Oh, it\'s easy enough to make a fortune," Henry said.', '1089': '--Is that you, pigeon?', '4077': 'The awful work was carried out with dread dispatch.', '1284': 'The Crooked Magician', '237': 'POLLY IS COMFORTED', '7021': '"Why can\'t you take me?" asks Mary.', '6829': '"I can\'t see it in that light," said the old lawyer.', '1995': '"Been looking up Tooms County.', '61': 'Go to her."'}
speaker_file_dict = {'1221': '1221_135766_000025_000001.wav', '3729': '3729_6852_000028_000000.wav', '1188': '1188_133604_000018_000000.wav', '5105': '5105_28233_000019_000003.wav', '7176': '7176_88083_000001_000000.wav', '7127': '7127_75946_000012_000000.wav', '4992': '4992_23283_000019_000000.wav', '121': '121_121726_000008_000002.wav', '4507': '4507_16021_000014_000000.wav', '672': '672_122797_000011_000002.wav', '5639': '5639_40744_000003_000011.wav', '260': '260_123286_000003_000002.wav', '3570': '3570_5694_000008_000004.wav', '2300': '2300_131720_000004_000004.wav', '8455': '8455_210777_000009_000000.wav', '1580': '1580_141083_000004_000001.wav', '7729': '7729_102255_000002_000003.wav', '3575': '3575_170457_000010_000005.wav', '4446': '4446_2271_000003_000005.wav', '8463': '8463_287645_000006_000001.wav', '8555': '8555_284447_000008_000001.wav', '8224': '8224_274384_000005_000006.wav', '6930': '6930_75918_000001_000000.wav', '61': '61_70970_000007_000001.wav', '2830': '2830_3979_000000_000000.wav', '908': '908_157963_000010_000001.wav', '1320': '1320_122612_000008_000002.wav', '2961': '2961_961_000002_000000.wav', '5142': '5142_33396_000002_000001.wav', '8230': '8230_279154_000004_000003.wav', '5683': '5683_32865_000001_000000.wav', '4970': '4970_29093_000002_000000.wav', '1089': '1089_134686_000004_000000.wav', '4077': '4077_13751_000019_000005.wav', '1284': '1284_1180_000001_000000.wav', '237': '237_126133_000001_000000.wav', '7021': '7021_79730_000061_000000.wav', '6829': '6829_68769_000005_000000.wav', '1995': '1995_1826_000010_000000.wav'}


def move_file(source_dir, target_dir):
    speaker_list = os.listdir(target_dir)
    for speaker in speaker_list:
        source_dir_sub = os.path.join(source_dir, speaker)
        target_dir_sub = os.path.join(target_dir, speaker)
        sentence = speaker_sen_dict[speaker]
        for filename in os.listdir(source_dir_sub):
            if filename.endswith('.wav') and filename[:-4].split('_')[3]==sentence:
                source_path = os.path.join(source_dir_sub, filename)
                target_path = os.path.join(target_dir_sub, filename)
                print(f'{speaker}:copy file from {source_path}')
                shutil.copyfile(source_path, target_path)
                break

    '''
    speaker_list = os.listdir(f'meta_emb_shot{shot}')
    speaker_sen_dict = dict()
    for speaker in speaker_list:
        filename = os.listdir(f'meta_emb_shot5/{speaker}')[0]
        sentence = filename[:-4].split('_')[3]
        print(speaker, sentence)
        speaker_sen_dict[speaker] = sentence
    speaker_sen_dict['61'] = "Go to her.\""
    print(speaker_sen_dict)
    '''

def get_speaker_file_dict():
    source_dir = '../test_compare/meta_emb246_90k_1shot'
    speaker_list = os.listdir(source_dir)
    speaker_file_dict = dict()
    for speaker in speaker_list:
        with open(os.path.join(source_dir, speaker, 'sen-file.txt'), 'r+') as F:
            lines = F.readlines()
            for line in lines:
                if line.split('|')[0] == speaker_sen_dict[speaker]:
                    speaker_file_dict[speaker] = line.split('|')[1].strip()[:-12] + 'wav'
    print(speaker_file_dict)
def move_file_real():
    source_dir = '../../real/LibriTTS/test-clean'
    target_dir = './real'
    speaker_list = os.listdir(target_dir)
    for speaker in speaker_list:
        sub_dir = speaker_file_dict[speaker].split('_')[1]
        source_path = os.path.join(source_dir, speaker, sub_dir, speaker_file_dict[speaker])
        target_path = os.path.join(target_dir, speaker, speaker_file_dict[speaker])
        print(f'{speaker}:copy file from {source_path}')
        shutil.copyfile(source_path, target_path)
def move_file_reference():
    source_dir = '../../real/LibriTTS/test-clean'
    target_dir = './reference'
    speaker_list = os.listdir(target_dir)
    for speaker in speaker_list:
        if speaker in ['1221','3729','7176']:
            continue
        sub_dir = speaker_file_dict[speaker].split('_')[1]
        file_digit = int(speaker_file_dict[speaker][-5]) + 1
        filename = speaker_file_dict[speaker][:-5] + str(file_digit) + '.wav'
        source_path = os.path.join(source_dir, speaker, sub_dir, filename)
        target_path = os.path.join(target_dir, speaker, filename)
        print(f'{speaker}:copy file from {source_path}')
        shutil.copyfile(source_path, target_path)
if __name__ == '__main__':
    move_file_reference()
