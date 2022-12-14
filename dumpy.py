
import colorsys
import io

import numpy as np
import PIL
import requests
from PIL import Image


def dumpy(file):
    dotSlash:str = "./";
    background:str = "dumpy/black.png";

    input = "";
    extraoutput = "";
    mode = "default";

    ty = 20 #; // width value
    backgroundimg = Image.open(background).convert("RGB")
    
    #resp = requests.get(file.url)
    inputimg = Image.open((file)) 

    # Calculates size from height
    txd = inputimg.width / inputimg.height
    tx = int(round(ty * txd * 0.862))

    # Prepares source image
    inputimage = inputimg.resize((tx, ty))

    # sets up loop vars
    bufferedImageArraySize = 6
    count1Check = 6
    count2Reset = 5
    sourceX = 74
    sourceY = 63
    modestring = ""

    # Sets up BG
    pad = 10
    ix = (tx * sourceX) + (pad * 2)
    iy = (ty * sourceY) + (pad * 2)

    # Actually makes the frames
    frames = []

    # these constants are now variables.
    fac = 1.00
    mox = 74
    moy = 63
    moguses = [None]* bufferedImageArraySize
    for it in range(0,bufferedImageArraySize):
        temp = f"dumpy/{it}{modestring}.png"
        moguses[it] = Image.open(temp).convert("RGB");


    if (ix > 1000 or iy > 1000):
        if (ix > iy):
            fac = 1000.0 / ix
        else:
            fac = 1000.0 / iy
        
        mox = int(round(mox * fac))
        moy = int(round(moy * fac))
        for itt in range(0,bufferedImageArraySize):
            moguses[itt] = (moguses[itt].resize((mox, moy)))

        pad = (int(pad * fac))
        ix = (mox * tx) + (pad * 2);
        iy = (moy * ty) + (pad * 2);

    for index in range(0,bufferedImageArraySize):
        print(index)
        indexx = index;
        F_bg = backgroundimg;
        F_ty = ty;
        F_tx = tx;
        F_count1Check = count1Check;
        F_count2Reset = count2Reset;
        F_dotSlash = dotSlash;
        F_extraoutput = extraoutput;
        ixF = ix #// new series of "modified" variables
        iyF = iy
        moxF = mox;
        moyF = moy;
        padF = pad;
        # // Start of new thread
        # new Thread(() -> {
        #     try {
        #         // bg
        frames.append(F_bg.resize((ixF, iyF)))

        count = indexx;
        count2 = indexx;

        # iterates through pixels
        for y in range(0,F_ty):
            for x in range(0,F_tx):

                # Grabs appropriate pixel frame
                pixel = moguses[count]; # No more constant reading!
                pixelinputimg = inputimage.load()
                pixel = shader(pixel, pixelinputimg[x, y]);
                # overlays it (if not null)
                if (pixel is not None):
                    frames[indexx] = overlayImages(frames[indexx], pixel, (x * moxF) + padF,
                            (y * moyF) + padF);
                

                # Handles animating
                count+=1
                if (count == F_count1Check):
                    count = 0
                

            # Handles line resets
            count2-=1
            if (count2 == -1):
                count2 = F_count2Reset
            count = count2
        # Writes finished frames
        #ImageIO.write(frames[indexx], "PNG", new File(F_dotSlash + "F_" + indexx + F_extraoutput + ".png"));
        print(len(frames))
        for ii in frames:
            #ii.show()
            ii.save(f"{indexx}_img.png",)
        frame_one = frames[0]
        frame_one.save("my_awesome.gif",format="GIF",append_images=frames,save_all=True,duration=100,loop=0)
        # Gives an idea of progress
        print(indexx)

def shader(t, pRgb):
    c = (197, 17, 17)
    c2 = (122, 8, 56)
    entry = pRgb

    # brightness check. If the pixel is too dim, the brightness is floored to the
    # standard "black" level.
    hsb = colorsys.rgb_to_hsv(entry[0], entry[1], entry[2]);
    blackLevel = 0.200;
    if (hsb[2] < blackLevel):
        entry = (colorsys.hsv_to_rgb(hsb[0], hsb[1], blackLevel))
    # "Blue's Clues" shadow fix: Fixes navy blue shadows.
    shadeDefault = 0.66;
    factor = abs(shadeDefault -  hsb[0]);
    factor = (1.0 / 6.0) - factor;
    if (factor > 0):
        factor *= 2;
        # System.out.println(shadeDefault + ", " + factor);
        shadeDefault = shadeDefault - factor;
    shade = [0,0,0]
    try:
        shade = [int(entry[0] * shadeDefault),int(entry[1] * shadeDefault), int(entry[2] * shadeDefault)]
    except Exception as iae:
        print("ERROR: " + str(shadeDefault) + ", " + str(factor))
    
    hsb = list(colorsys.rgb_to_hsv(shade[0], shade[1], shade[2]))
    hsb[0] = hsb[0] - 0.0635;
    if (hsb[0] < 0.0):
        hsb[0] = 1.0 + hsb[0]
    shade = (colorsys.hsv_to_rgb(hsb[0], hsb[1], hsb[2]))
    # fills in img
    # BufferedImageOp lookup = new LookupOp(new ColorMapper(c, entry), null);
    # BufferedImageOp lookup2 = new LookupOp(new ColorMapper(c2, shade), null);

    #t = toARGB(t);
    #BufferedImage convertedImage = lookup.filter(t, null);
    tmatrix = np.array(t)
    tmatrix[(tmatrix[:,:,0] == c[0]) & (tmatrix[:,:,1] == c[1]) & (tmatrix[:,:,2] == c[2])] = entry 
    #convertedImage = lookup2.filter(convertedImage, null);
    tmatrix[(tmatrix[:,:,0] == c2[0]) & (tmatrix[:,:,1] == c2[1]) & (tmatrix[:,:,2] == c2[2])] = shade 
    convertedImage = Image.fromarray(tmatrix)
    return convertedImage;

def overlayImages(bgImage, fgImage, locateX:int, locateY:int):

    if (fgImage.height > bgImage.height or fgImage.width > fgImage.width):
        print("Foreground Image Is Bigger In One or Both Dimensions"
                + "nCannot proceed with overlay." + "nn Please use smaller Image for foreground")
        return None
    bgImage.paste(fgImage, (locateX, locateY))
    
    return bgImage;

dumpy("download.jpg")
