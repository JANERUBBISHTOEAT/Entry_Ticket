from make_png import paste_qr
from make_png import makea_qr
from os.path import dirname, join
import threading
import hashlib
# u know what's new in gamma

# Constants
QRC_DIREC = ".\\qr\\"
OUT_DIREC = ".\\out\\"
POS_DIREC = "in.png"
FILE_TYPE = ".png"
TXTRECORD = "res.txt"
SEPERATOR = '#'
VERSION   = str(hex(20200409))


# Global Var
prev_Data = ""
code_List = []
name_List = []
is_processed = []
cnt = 0


def run_paste(post_path, i):
    # print ("开始线程：" + self.name)
    qr_path  = QRC_DIREC + name_List[i] + FILE_TYPE
    out_path = OUT_DIREC + name_List[i] + FILE_TYPE
    qr_path  = join(dirname(__file__), qr_path  )
    out_path = join(dirname(__file__), out_path )
    post_path= join(dirname(__file__), post_path)
    paste_qr(post_path, qr_path, out_path)

def run_mkqr(i):
    # print ("开始线程：" + self.name)
    makea_qr(code_List[i], name_List[i])


def open_record():
    global cnt
    global is_processed
    global code_List
    global name_List
    # print(sys.getdefaultencoding())

    print("----------------------------")
    print("Reading record from " + TXTRECORD + ":")
    
    fp = open(join(dirname(__file__),TXTRECORD), mode = 'r', encoding = "utf-8")
    # "Check#Code#Name"
    text = fp.read()
    fp.close()
    print(text)
    for line in text.split('\n'):
        if SEPERATOR in line:
            is_processed.append(line.split(SEPERATOR)[0])

            md_5 = hashlib.md5((line.split(SEPERATOR)[1]).encode(encoding='UTF-8')).hexdigest()
            code_List.append(md_5)

            name_List.append(line.split(SEPERATOR)[2].rstrip('\n'))
            if (is_processed[cnt]):
                print("|-√- " + name_List[cnt])
            else:
                print("|--- " + name_List[cnt])
            cnt += 1
        else:
            print("Unexpected Format Detected")
    print("{} records read succesfully".format(cnt))
    print("-----------------------\n")

    fp = open(join(dirname(__file__), "out.txt"), mode = 'w', encoding = "utf-8")
    for i in range(cnt):
        fp.write(is_processed[i] + SEPERATOR + code_List[i] + SEPERATOR + name_List[i] + '\n')
        



if __name__ == '__main__':
    print("Running on ver." + VERSION[2:])
    open_record()
    post_path = join(dirname(__file__),POS_DIREC)
    Thread_List = []

    # Make QRcode
    for i in range(cnt):
        t = threading.Thread(target = run_mkqr, args = (i,))
        Thread_List.append(t)

    for t in Thread_List:
        # print ("Starting thread" + str(t))
        t.start()

    for t in Thread_List:
        t.join()
        
    Thread_List.clear()
    # Paste QRcode on Post
    for i in range(cnt):
        t = threading.Thread(target = run_paste, args = (post_path, i))
        Thread_List.append(t)

    for t in Thread_List:
        t.start()

    for t in Thread_List:
        t.join()