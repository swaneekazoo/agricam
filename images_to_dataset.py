import os
import shutil
import argparse

if __name__ == '__main__':
    TIME_ONSCREEN = 18

    parser = argparse.ArgumentParser()
    parser.add_argument('dir')
    args = parser.parse_args()

    files = sorted((f for f in os.listdir(args.dir) if not f.startswith(".")), key=str.lower)

    cow_num = 0
    for i, img in enumerate(files):
        if i % TIME_ONSCREEN == 0:
            cow_num += 1
            os.makedirs(f'{args.dir}/cow{cow_num}/')
        print(img, cow_num)
        shutil.copy(f'{args.dir}/{img}', f'{args.dir}/cow{cow_num}/')
