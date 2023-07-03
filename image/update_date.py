from datetime import datetime
from datetime import timedelta
import piexif

import argparse



if __name__ == '__main__': 

    parser = argparse.ArgumentParser(
        prog='Modify File Date',
        description='Take a file path and a date time object to update the files modified/created timestamp.',
        epilog='modify_date.py <filePath> <newDateTime>'
    )

    parser.add_argument('filename') 
    parser.add_argument('newDateTime')  # 2023-06-23T02:25:41.389102 (isoformatted)
                                        # 2023-10-21@18:13:37.248956 
    # parser.add_argument('-c', '--count')      # option that takes a value
    # parser.add_argument('-v', '--verbose',
    #                     action='store_true')  # on/off flag

    print("\nModify File TimeStamps: \n")
    
    
    # preprocess argparse inputs 
    args = parser.parse_args()
    filename = args.filename
    
    # if file is jpeg or tiff use exif
    # otherwise use os.utime() and os.stat()
    
    print(filename[-4:])
    
    if (filename[-4:] == '.png'):
        import os, sys

        # Showing stat information of file
        stinfo = os.stat(filename)
        new_date = datetime.fromisoformat(args.newDateTime).timestamp()

        print ('Inputs processed succesfully.\n')

        print ("file stat info:")
        print (stinfo)
        print ()


        # Using os.stat to recieve atime and mtime of file
        print (f"original access time of {filename}: %s" % datetime.fromtimestamp(stinfo.st_atime))
        print (f"original modified time of {filename}: %s" % datetime.fromtimestamp(stinfo.st_mtime))

        # Modifying atime and mtime
        print("\nChanging Timestamp values.")
        # Add a random amount of time 1-4 seconds to the access time with a random microsecond
        modified_date = datetime.fromtimestamp(new_date)+timedelta(seconds=0, microseconds=949436)
        access_date = datetime.fromtimestamp(new_date)+timedelta(seconds=1, microseconds=149436)
        
        modified_date = modified_date.timestamp()
        access_date = access_date.timestamp()
        
        os.utime(filename,(access_date, modified_date)) # Set last accessed time to some random number of hours from a few days ago.


        # Using os.stat to recieve atime and mtime of file
        stinfo = os.stat(filename)
        print (f"New access time of {filename}: %s" % datetime.fromtimestamp(stinfo.st_atime))
        print (f"New modified time of {filename}: %s" % datetime.fromtimestamp(stinfo.st_mtime))

        print ("done!!")
    
    
    else:
        
        exif_dict = piexif.load(args.filename)
        new_date = datetime.fromisoformat(args.newDateTime).strftime("%Y:%m:%d %H:%M:%S") 

        
        try:
            # Get the original timestamps of the image as proof of change
            print(exif_dict['0th'])
            orig_date = exif_dict['0th'][piexif.ImageIFD.DateTime]
            print("Files current timestamp:", orig_date)
        except: exit(1)
        
        # update datetime location of file and save
        print('Updating file timestamps.')
        try:
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
            exif_bytes = piexif.dump(exif_dict) # convert piexif object into bytes?
            piexif.insert(exif_bytes, args.filename) # Updates bytecode with modified bytecode
        except: exit(1)
        
        
        try:
            # Get the timestamps of the file and display them to the user for validation. 
            exif_dict = piexif.load(args.filename)
            print(f'Old Timestamp {orig_date}')    
            print(f'New Timestamp {exif_dict["0t"][piexif.ImageIFD.DateTime]}')    
        except: exit(1)
        
    print ("Update Success:")
