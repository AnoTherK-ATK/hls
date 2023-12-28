import numpy as np
import cv2
from subprocess import call
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from sys import argv
from moviepy.editor import *
key = []

def logistic(r, x, size):
    for i in range(size):
        x = r * x * (1 - x)
        key.append((int(x * 10000) % 256))

def dec(filename):
    r = 4
    x = 0.54321
    vid = cv2.VideoCapture(filename)
    success = True
    cnt = 0
    fps = vid.get(cv2.CAP_PROP_FPS)
    res = [int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))]
    audio = filename.split('.')[0]+".mp3"
    call(["ffmpeg", "-i", filename, "-vn", "-q:a", "0", "-map", "a",filename.split('.')[0]+".mp3"])
    logistic(r, x, int(vid.get(cv2.CAP_PROP_FRAME_COUNT)))
    print(str(int(vid.get(cv2.CAP_PROP_FRAME_COUNT))) + " frames")
    
    output = cv2.VideoWriter(filename.split('.')[0] + "_dec.mkv", cv2.VideoWriter_fourcc(*"FFV1"), fps, res)
    while success:
        success, image = vid.read() 
        if not success:
            break
        image = np.bitwise_xor(image, key[cnt % len(key)])
        output.write(image)
        cnt += 1
    output.release()
    call(["ffmpeg", "-i", filename.split('.')[0] + "_dec.mkv", "-i", audio, "-c:v", "copy", "-c:a", "aac", filename.split('.')[0] + "_dechq.mkv"])
    return str(filename.split('.')[0] + "_dechq.mkv")

def decAES(filename, enc_filename, output_filename):
    fkey = open(enc_filename, "rb")
    akey = fkey.read()
    fkey.close()
    f = open(filename, "rb")
    iv = f.read(16)
    data = f.read()
    f.close()
    cipher = AES.new(akey, AES.MODE_CBC, iv=iv)
    data = unpad(cipher.decrypt(data), AES.block_size)
    f = open(output_filename, "wb")
    f.write(data)
    f.close()


decAES(argv[1], argv[2], argv[3])
fname = dec(argv[3])
call(["ffmpeg", "-y", "-i", fname, "-hls_key_info_file", "enc.keyinfo","-hls_playlist_type", "vod", "-hls_time", "10", "-hls_segment_filename", fname.split('.')[0] + "%03d.ts", fname.split('.')[0] + ".m3u8"])    
