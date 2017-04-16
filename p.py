#!/usr/bin/python

# working with pickle and files

import pickle

TEST_TAG = {"Mario":[130, 81, 177, 239, 0, 0, 0]}
TAG_FILE = 'tag_archive.p'
TAG_ARCHIVE = []

def read_tag_file():
    tags=open(TAG_FILE, 'rb')
    while 1:
        try:
            TAG_ARCHIVE.append(pickle.load(tags))
        except EOFError:
            break
    tags.close()
    return

def write_tag_file():
    tags=open(TAG_FILE, 'wb')
    pickle.dump(TEST_TAG, tags)
    tags.close()
    return

def main():

    print ("Starting up...")
    print ("Calling write")
    print TEST_TAG
    write_tag_file()
    print ("Calling read")
    read_tag_file()
    print TAG_ARCHIVE
    

    return

if __name__ == '__main__':
    main()

#End
