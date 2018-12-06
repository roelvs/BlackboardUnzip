__author__ = 'Roel Van Steenberghe'

import zipfile
import os
import sys
import getopt


extract_dir = os.curdir + "OUTPUT/"
toledo_filename = "toledo.zip"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "inputfile", "outputdir"])

    for opt, arg in opts:
        if opt in ("-h", "help"):
            print("usage: toledounzipper.py -i <inputfile> -o <outputdir> \\n default input file is toledo.zip, default olutput folder='OUTPUT'")
            sys.exit()
        if opt in ("-i", "--inputfile"):
            toledo_filename = arg
        if opt in ("-o", "--outputdir"):
            extract_dir = arg + "/"

except getopt.GetoptError() as err:
    print("=====error..." + str(err))
    sys.exit(2)

if (zipfile.is_zipfile(toledo_filename)):
    print("====valid input zip file...")
    file = open(toledo_filename, "rb")
    z = zipfile.ZipFile(file)
    for zipped_file in z.namelist():
        print("===== *** unzipping " + zipped_file + " to " + extract_dir)
        z.extract(zipped_file, extract_dir)
else:
    print("invalid input file")
    sys.exit()

for f in os.listdir(extract_dir):
    if f.endswith(".txt"):

        metafile = open(extract_dir + f).readlines()
        meta_student_name = metafile[0]
        meta_student_file = metafile[-2]

        # tekstbestand openen met info: regel 1= naam van student, laatste regel is bestandsnaam
        if (metafile[0].startswith("Naam:")):  # signature of a valid metadata file: starts with 'Naam:'
            clean_student_name = meta_student_name.lstrip("Naam:").rstrip("\n")
            print("= processing " + clean_student_name + "...")

            # create folder for each student
            try:
                os.mkdir(extract_dir + clean_student_name)
            except:
                print("=== warning: could not create folder. Already existing?... Operation will continue...")

            # move the files to the student directories. Unzip were necessary
            clean_student_file = meta_student_file.strip("\n").lstrip("\tBestandsnaam: ")

            print("=== copy file to " + extract_dir + clean_student_name + "/" + clean_student_file)
            if (clean_student_file.endswith(".zip")):
                try:
                    print("=== Student submission is a zipfile. Unzipping...")
                    file = open(extract_dir + clean_student_file, "rb")
                    z = zipfile.ZipFile(file)
                    for zipped_file in z.namelist():
                        print(zipped_file + "=== unzipping to " + extract_dir)
                        z.extract(zipped_file, extract_dir + clean_student_name)
                    file.close()
                    os.remove(extract_dir + clean_student_file)  # delete zip file from student
                except:
                    print("=== error while unzipping")

            else:
                try:
                    os.rename(extract_dir + clean_student_file, extract_dir + clean_student_name + "/" + clean_student_file)
                except:
                    print("=== error while moving files to student folder")
            os.remove(extract_dir + f)


