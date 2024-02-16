# myapp/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core.files.storage import default_storage
from django.conf import settings

from .forms import CustomUserCreationForm, VideoForm, DecodeVideoForm
from .models import Video

import cv2
from moviepy.editor import *
import numpy as np
import os

# barat@mail.com
# lonew0lf

# admin
# admin@mail.com
# admin123

# aaa
# aaa@gmail.com
# akash@123

def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to the name of your home view
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Change 'home' to the name of your home view

def home(request):
    print(request)
    return render(request, 'home.html', {})

# ===================================================================================================

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)

        # Saving video to a folder
        vid = request.FILES.get('video_file')
        tit = request.POST['title'] + '.' + vid.name.split('.')[-1]
        file_path = default_storage.save(f"encoded/{tit}", vid)

        # Writing user data in image
        encoded_image = encode(image_name="black.png", secret_data="{ip: '106.15.25.43', email:'aaa@gmail.com'}", video = vid, path = file_path)
        embed(encoded_image, vid, tit)

        # Updating file path in database
        if form.is_valid():
            Video.objects.create(url = file_path, video_file=str(settings.BASE_DIR) + '/encoded/' + tit, title=tit)
            return redirect('../admin')  # Redirect to a page showing all uploaded videos
    else:
        form = VideoForm()
        return render(request, 'upload.html', {'form': form})

def videos(request):
    return render(request, 'videos.html', {})

def encode(image_name, secret_data, video, path):
    width, height = findVideoDim(path)

    # read the image
    image = cropImage(image_name, width, height)

    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8

    # add stopping criteria
    secret_data += "====="

    # convert data to binary
    binary_secret_data = to_bin(secret_data)

    # size of data to hide
    data_len = len(binary_secret_data)
    print("[*] Maximum number of bits we can encode:", n_bytes*8)
    print("[*] Number of bits to encode:", data_len)
    if len(secret_data) > n_bytes:  
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print('[+] Secret Data:', secret_data[:-5])
    print("[+] Encoding data...")

    data_index = 0
    for row in range(height):
        for col in range(width):
            # convert RGB values to binary format
            r, g, b = to_bin(image[row][col])

            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                image[row][col][0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1

            if data_index < data_len:
                # least significant green pixel bit
                image[row][col][1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1

            if data_index < data_len:
                # least significant blue pixel bit
                image[row][col][2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                return image

def findVideoDim(video): # To find dimension of the video
    vcap = cv2.VideoCapture(video)
    if vcap.isOpened():
        width  = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
        height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        print(f"[*] Dimension of the given video: {width}p x {height}p")
        return (width, height)
    else:
        print("[!] Error opening video ! Exiting ...")
        exit()

def cropImage(img, width, height): # To crop the image into video dimension
    image = cv2.imread(img)
    y=0
    x=0
    crop = image[y:y+height, x:x+width].copy()
    return crop

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, "08b") for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def embed(crop, video, title):
    temp_file = 'test.mp4'
    embed_image = 'embed.png'
    cv2.imwrite(embed_image, crop)

    os.system(f'ffmpeg -framerate 1 -i {embed_image} -c:v libx264rgb -crf 0 {temp_file} -y') # Convert Image to Video
    os.system(f'ffmpeg -i {temp_file} -c copy -bsf:v h264_mp4toannexb temp0.ts -y')
    os.system(f'ffmpeg -i {str(settings.BASE_DIR) + "/encoded/" + title} -c copy -bsf:v h264_mp4toannexb temp1.ts -y')
    os.system(f'ffmpeg -i "concat:temp0.ts|temp1.ts" -c copy -bsf:a aac_adtstoasc encoded/{title} -y')

    print(f'[*] Encoded video is saved as "{title}"')
    
    # Clean working directory
    for val in ['temp0.ts', 'temp1.ts', 'test.mp4', 'embed.png']:
        os.remove(val)

# ====================================================================================================

def decode_video(request):
    if request.method == 'GET':
        form = DecodeVideoForm()
        return render(request, 'decode.html', {'form': form})
    else:
        vid = request.FILES.get('video_file')
        tit = vid.name
        file_path = default_storage.save(f"uploads/{tit}", vid)
        vcap2 = cv2.VideoCapture(str(settings.BASE_DIR) + '/uploads/' + tit)

        success, image = vcap2.read()
        if success:
            cv2.imwrite("first_frame.png", image)  # save frame as PNG file
            print('[*] First frame of the video has been extracted')

        # decode the secret data from the image
        decoded_data = decode("first_frame.png")

        print("[+] Decoded data:", decoded_data)
        return HttpResponse(f'The hidden data in the video is {decoded_data} <a href="../">click to go home</a>')

def decode(image_name):
    print("[+] Decoding...")

    # read the image
    image = cv2.imread(image_name)
    binary_data = ""

    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
        break
    print('[+] Extracted binary data from the Video. Processing the data...')

    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]

    # convert from bits to characters
    decoded_data = ""

    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]
