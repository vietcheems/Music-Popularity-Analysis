import re

# check=True return True if anything was replaced and False otherwise, check=False return the filtered string


def filter(name, check=False):

    remove = [
        'remastered',
        'radio edit',
        'version',
        'mono',
        'stereo',
        'single',
        'remaster',
        'revisited',
    ]

    replace = {
        "various artists": "song"
    }

    replaced = False

    for word in replace.keys():
        if word in name:
            name = name.replace(word, replace[word])
            replaced = True

    for word in remove:
        if word in name:
            name = name.replace(word, "")
            replaced = True

    if re.search("\d{4}", name):
        name = re.sub("\d{4}", "", name)
        replaced = True

    if check:
        return replaced

    return re.sub(" +", " ", name).strip(), replaced


if __name__ == "__main__":
    print(filter("alphaville - forever young remastered".lower()))
