import os

def main():
    with open('address_naturalness.txt','w+') as F:
        for form_id in range(30):
            F.write(f'https://eric102004.github.io/human-evaluation-for-metaTTS/naturalness_{form_id}.html'+'\n')
    with open('address_similarity.txt', 'w+') as F:
        for form_id in range(50):
            F.write(f'https://eric102004.github.io/human-evaluation-for-metaTTS/similarity_{form_id}.html'+'\n')
if __name__ == '__main__':
    main()
    
