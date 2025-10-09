import chardet

with open("../data/fra_perfumes.csv", "rb") as f:
    result = chardet.detect(f.read(100000))
print(result)
