import csv
import logging
import os
import sys
from zipfile import ZipFile, ZIP_DEFLATED


logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)


def make_dir(outp):
    if not os.path.exists(outp):
        logging.info("[Creating output directory in " + outp + "]")
        os.makedirs(outp)


def read_csv(csv_file):
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        return list(reader)


def add_to_zip(path, zipf, alt_name=None):
    ''' zipf is zipfile handle
    '''
    if not os.path.isdir(path):
        name_in_arhive = alt_name if alt_name is not None else os.path.basename(path) 
        zipf.write(path, name_in_arhive)
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))


def build_arhive_subiecte(studenti_subiecte, extra_data, output_path):
    '''
    studenti - o lista de tupluri: email_student, path/subiect1.pdf, path/subiect2.pdf ... path/subiectn.pdf
    extra_data - o lista de path-uri cu extra date ce trebuie adaugate in arhiva
    output_path - unde sa se construiasca arhivele
    '''
    make_dir(output_path)
    perechi_studenti_arhive = set()
    for elem in studenti_subiecte:
        email_student = elem[0]
        out_zipfile = os.path.join(output_path, email_student) + '.zip'
        with ZipFile(out_zipfile, 'w', ZIP_DEFLATED) as zipf:
            for idx, subiect in enumerate(elem[1:]):
                _, file_ext = os.path.splitext(subiect)
                alt_name = 'Subiect_' + str(idx + 1) + file_ext
                add_to_zip(subiect, zipf, alt_name)
            for xtra in extra_data:
                add_to_zip(xtra, zipf)
        if (email_student, out_zipfile) in perechi_studenti_arhive:
            logging.error("Something went wrong, student " + perechi_studenti_arhive + "appears twice")
            sys.exit(-1)
        perechi_studenti_arhive.add((email_student, out_zipfile))
    return list(perechi_studenti_arhive)


def main():
    '''
    input:
        cs - fisier csv care contine numele studentului, cale_catre/subiectul1, cale_catre/subiectul2
        extra_data - lista cu fisiere extra care trebuie adaugate in fiecare arhiva
        output_path - directorul in care se construieste arhiva cu subiecte
    '''
    cs = read_csv('subiecte.csv')
    extra_data = ['Problema_1/data/',
                  'Problema_1/problema_1_solutie.py']
    output_path = './arhive_subiecte'
    build_arhive_subiecte(cs, extra_data, output_path)


if __name__ == '__main__':
    main()

