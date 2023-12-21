
import os
import sys
import hashlib

def extract_paragraphs(filename):
    try:
        with open(filename, "r", encoding="latin1") as f:
            paragraphs = []
            paragraph = ""
            for line in f:
                if line.strip() == "":
                    if paragraph != "":
                        paragraphs.append(paragraph)
                    paragraph = ""
                else:
                    paragraph += line
        if paragraph != "":
            paragraphs.append(paragraph)
        return paragraphs
    except UnicodeDecodeError:
        print("UnicodeDecodeError: " + filename)
        return []

import re
pattern = "^Content-Transfer-Encoding: base64$"
base64pattern = "[A-Za-z0-9+/  \t\n]+" # base64 pattern

all_base64 = set()

def seek_base64(file_path, paragraphs):
    for i, p in enumerate(paragraphs):
        match = re.search(pattern, p, flags=re.MULTILINE)
        if(match):
            if(i + 1 < len(paragraphs)):
                candidate = paragraphs[i+1].strip()
                if(candidate.endswith("--")):
                    candidate_last_line = candidate.splitlines()[-1].strip()
                    candidate = candidate[:-len(candidate_last_line)]
                if(re.fullmatch(base64pattern, candidate)):
                    h = hashlib.md5()
                    h.update(candidate.encode("utf-8"))
                    print("matches ", file_path, " paragraph ", i+1, " bytes ", len(candidate), h.hexdigest())
                    all_base64.add(candidate)



if(len(sys.argv) != 2):
    print("Usage: python findallbase64.py <directory>")
    sys.exit(0)

directory = sys.argv[1]


for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    if os.path.getsize(file_path) < 1024*1024*64: # 64MB
        seek_base64(file_path, extract_paragraphs(file_path))
    

print("Total base64: ", len(all_base64))

counter = 0
for b in all_base64:
    counter += 1
    file = "enron"+str(counter)+".txt"
    with open(file, "w") as f:
        f.write(b)
    print(f"The string has been written to the file {file}.")