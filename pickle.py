#!/usr/bin/python

# working with pickle and files

import pickle

TEST_TAG = {[130, 81, 177, 239, 0, 0, 0]}
TAG_ARCHIVE = []

def read_tag_file():
    tag_file=open('tag_archive.p', 'rb')
    while 1:
        try:
            TAG_ARCHIVE.append(pickle.load(tag_file))
        except EOFError:
            break
    tag_file.close()
    return

def write_tag_file():
    tag_file=open('tag_archive.p', 'wb')
    pickle.dump(TEST_TAG, tag_file)
    tag_file.close()
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
