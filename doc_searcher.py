import sys
import cv2
from PIL import Image
import pytesseract
import argparse
import os
import pdf2image

ap = argparse.ArgumentParser()

ap.add_argument("-d", "--document", required=True, help="path to input document")
ap.add_argument("-w", "--words", required=True, help="list of key words to search for")
ap.add_argument("-p","--process", type=str, default="thresh",help="type of pre-processing to be performed")
ap.add_argument("-f","--format", required=True, help="The format of the provided document")

args = vars(ap.parse_args())

key_word_arguments = args["words"]
key_word_list = key_word_arguments.split(",")


'''
CHeck whether the document provided is in PDF format
if so, convery the pdf to image
'''

if args["format"] == "pdf":


    document = pdf2image.convert_from_path(args["document"], dpi=500)
    doc_dict = {index:pytesseract.image_to_string(page) for index,page in enumerate(document)}
    clean_indexed_pages = [[item for item in enumerate(doc_dict[i].split("\n")) if item[1] != ''] for i in range(len(doc_dict.keys()))]
    page_dict = {i+1:{index:line for index,line in clean_indexed_pages[i]} for i in range(0,len(clean_indexed_pages))}

else:
    document = args["document"]

    # Convert the image to grayscale

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    if args["process"] == "threshold":
        gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]

    elif args["process"] == "blurr":
        gray = cv2.medianBlur(gray,3)

    filename = f"{os.getpid()}.png"
    cv2.imwrite(filename,gray)

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)

    clean = [line for line in enumerate(text.split("\n")) if line[1] != '']
    page_dict = {index:line for index,line in clean}


if args["format"] == "pdf":
    result_dict = {}
    for page in page_dict.keys():
        for word in key_word_list:
            result_dict[word] = result_dict.get(word,{})
            result_dict[word][page] = result_dict[word].get(page,[])
            for index, line in page_dict[page].items():
                if word in line:
                    result_dict[word][page].append(index)
    
    print(result_dict)



else:
    result_list = []

    for index,line in page_dict.items():
        for word in key_word_list:
            if word in line:
                result_list.append(index)