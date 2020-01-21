import os 

def main():
    urls_lines = open('./urls.txt','r',encoding='utf-8').read().splitlines()
    num = 0
    for url in urls_lines:
        print('\n==> Download start...\n')
        command = 'downloader.exe ' + url
        os.system(command)
        num += 1


if __name__ == "__main__":
    main()
    