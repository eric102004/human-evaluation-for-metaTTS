import os

def gen_dir(shot=1):
    if shot==1 or shot==None:
        except_list = []
    elif shot==5:
        except_list = ['61']
    elif shot==20:
        except_list = ['61','1221','672','908']
    dir_list = os.listdir('.')
    for mom_dir in dir_list:
        if mom_dir.endswith(f'shot{shot}'):
            for speaker in speaker_list:
                if speaker in except_list:
                    continue
                os.mkdir(os.path.join(mom_dir, speaker))
            

if __name__ == '__main__':
    speaker_list = os.listdir('../../../libriTTS_log/real/LibriTTS/test-clean')
    for shot in [1,5,20]:
        gen_dir(shot=shot)

