import argparse
import csv
import functools
import glob
import logging
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

logging.basicConfig(level=logging.DEBUG)

def main():
    logging.info('Begin Main')

    # Parse command line arguments
    logging.info('Parsing input arguments')
    parser = argparse.ArgumentParser(
        description='Script to parse PDF resumes, and create a csv file'
                    'and required fields')
    parser.add_argument('--data_path', help='Path to folder containing documents ending in .pdf',
                        required=True)
    parser.add_argument('--output_path', help='Path to place output .csv file',
                        default='C:/Users/shrij/Desktop/data/data/output/Resume_Output.csv')

    args = parser.parse_args()

    logging.info('Command line arguments: %s', vars(args))

    # Create resume resume_df
    resume_df = create_resume_df(args.data_path)
    # Output to CSV
    resume_df.to_csv(args.output_path, quoting=csv.QUOTE_ALL, encoding='utf-8')
    logging.info('End Main')


def convert_pdf_to_txt(input_pdf_path):
    try:
        logging.debug('Converting pdf to txt: ' + str(input_pdf_path))
        # Setup pdf reader
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        # Iterate through pages
        path_open = file(input_pdf_path, 'rb')
        for page in PDFPage.get_pages(path_open, pagenos, maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            interpreter.process_page(page)
        path_open.close()
        device.close()

        # Get full text from PDF
        full_string = retstr.getvalue()
        retstr.close()

        # Normalize a bit, removing line breaks
        full_string = full_string.replace("\r", "\n")
        full_string = full_string.replace("\n", " ")

        # Remove Bullet characters
        full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
        return full_string.encode('ascii', errors='ignore')

    except Exception, exception_instance:
        logging.error('Error in file: ' + input_pdf_path + str(exception_instance))
        return ''


def check_phone_number(string_to_search):
    #Extract PhoneNumber Information
    try:
        regular_expression = re.compile(r"\(?"
                                        r"(\d{3})?"  
                                        r"\)?"  
                                        r"[\s\.-]{0,2}?"  
                                        r"(\d{3})"  
                                        r"[\s\.-]{0,2}"  
                                        r"(\d{4})",  
                                        re.IGNORECASE)
        result = re.search(regular_expression,string_to_search)
        flag=0
        if result:
            res=result.groups()
            for i in res:
                if(i==None):
                    flag=1
                    break
            if(flag==1):
                regular_expression = re.compile(r"(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}",re.IGNORECASE)
                result = re.search(regular_expression,string_to_search)
            result=result.group()
        return result
    except Exception, exception_instance:
        logging.error('Issue parsing phone number: ' + string_to_search + str(exception_instance))
        return None


def check_email(string_to_search):
    #Extract Email Information
    try:
        regular_expression = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", re.IGNORECASE)
        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.group()
        return result
    except Exception, exception_instance:
        logging.error('Issue parsing email number: ' + string_to_search + str(exception_instance))
        return None

def Extract_Links(string_to_search,term):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',string_to_search)
    flag=0
    for i in urls:
        if term in i:
            s=i
            flag=1
            break
    if flag==1:
        if s[len(i)-1]=='.' or s[len(i)-1]==',':
            if not s[len(i)-1].isalnum():
                return s[:len(i)-2]
            else:
                return s[:len(i)-1]
        elif not s[len(i)-1].isalnum():
            return s[:len(i)-1]
        else:
            return s
    return 0

def check_address(string_to_search):
    try:
        regular_expression = re.compile(r"[0-9]+[\/][0-9]+[ ]?[a-zA-Z0-9,\.# ]+", re.IGNORECASE)
        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.group()
        return result
    except Exception, exception_instance:
        logging.error('Issue parsing email number: ' + string_to_search + str(exception_instance))
        return None

def check_cgpa(string_to_search):    
    regular_expression=re.compile(r"[cC]?[gG][Pp][aA]"
                                  r"[ ]?[:]?[ ]?[-]?[ ]?[0-9].?[0-9]+",re.IGNORECASE)
    result=re.search(regular_expression,string_to_search)
    if result:
        result = result.group()
        result="".join(result)
    regular_expression=re.compile(r"[0-9].?[0-9]+",re.IGNORECASE)
    res=re.search(regular_expression,result)
    gpa=float(res.group())
    regular_expression=re.compile(r"[\/][0-9]",re.IGNORECASE)
    result=re.search(regular_expression,string_to_search)
    regular_expression=re.compile(r"[cC]?[gG][Pp][aA]"
                                  r"[ ]?[:]?[ ]?[-]?[ ]?[0-5][.0-9]{0,2}[\/]?[a-zA-Z]?[ ]?5",re.IGNORECASE)
    result=re.search(regular_expression,string_to_search)
    if result:
        result=result.group()
    if gpa<5 and result!=None:
        gpa*=2
    return gpa

def check_gpa(string_to_search,term):
    rgpa=term
    regular_expression=re.compile(r"[cC]?[gG][Pp][aA]"
                                  r"[ ]?[:]?[ ]?[-]?[ ]?[0-9].?[0-9]+",re.IGNORECASE)
    result=re.search(regular_expression,string_to_search)
    if result:
        result = result.group()
        result="".join(result)
    #print result
    regular_expression=re.compile(r"[0-9].?[0-9]+",re.IGNORECASE)
    res=re.search(regular_expression,result)
    gpa=float(res.group())
    regular_expression=re.compile(r"[cC]?[gG][Pp][aA]"
                                  r"[ ]?[:]?[ ]?[-]?[ ]?[0-5][.0-9]{0,2}[\/]?[ ]?[a-zA-Z ]?[ ]?5",re.IGNORECASE)
    result=re.search(regular_expression,string_to_search)
    if result:
        result=result.group()
    if gpa<5 and result!=None:
        gpa*=2
    if gpa>=rgpa:
        string="Shortlisted"
        return string
    else:
        threshold=0.05*rgpa
        if gpa>=rgpa-threshold:
            regular_expression=re.compile(r"[mM][aA][cC][hH][iI][nN][eE] [lL][eE][aA][rR][nN][iI][nN][gG]",re.IGNORECASE)
            result=re.search(regular_expression,string_to_search)
            if result:
                string="ShortListed"
            else:
                regular_expression=re.compile(r"[iI][mM][aA][gG][eE] [a-zA-z]",re.IGNORECASE)
                result=re.search(regular_expression,string_to_search)
                if result:
                    string="ShortListed"
                else:
                    regular_expression=re.compile(r"[dD][aA][tT][aA] [mM][iI][nN][iI][nN][gG]",re.IGNORECASE)
                    result=re.search(regular_expression,string_to_search)
                    if result:
                        string="ShortListed"
                    else:
                        regular_expression=re.compile(r"[tT][eE][xX][tT] [mM]?[iI]?[nN]?[iI]?[nN]?[gG]?",re.IGNORECASE)
                        result=re.search(regular_expression,string_to_search)
                        if result:
                            string="ShortListed"
                        else:
                            regular_expression=re.compile(r"[aA][nN][dD][rR][oO][iI][dD]",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                if 0.2+gpa>=rgpa:
                                    string="Shortlisted"
                                    return string
                            regular_expression=re.compile(r"[tT][rR][eE][eE][sS]?",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.05
                            regular_expression=re.compile(r"[lL][iI][nN][kK][eE][dD][ ]?[lL][iI][sS][tT][']?[sS]?",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.05
                            if gpa>=rgpa:
                                string="Shortlisted"
                                return string
                            java_score=0.035
                            python_score=0.035
                            cpp_score=0.015
                            csharp_score=0.015
                            regular_expression=re.compile(r"[jJ][aA][vV][aA]",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.035
                            regular_expression=re.compile(r"[pP][yY][tT][hH][oO][nN]",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.035
                            regular_expression=re.compile(r"[cC][pP+][pP+]",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.010
                            regular_expression=re.compile(r"[cC][#]?",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.010
                            if gpa>=rgpa:
                                string="Shortlisted"
                                return string
                            regular_expression=re.compile(r"[wW][eE][bB][ ]?[a-zA-Z]",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.21
                            if gpa>=rgpa:
                                string="Shortlisted"
                                return string
                            regular_expression=re.compile(r"[a-zA-Z][ ][Aa][pP][iI][']?[sS]?",re.IGNORECASE)
                            result=re.search(regular_expression,string_to_search)
                            if result:
                                gpa+=0.21
                            if gpa>=rgpa:
                                string="Shortlisted"
                                return string
                            #print gpa
                            string="Not Shortlisted"
                            return string
        else:
            string="Not ShortListed"
        return string

def term_count(string_to_search, term):
    try:
        regular_expression = re.compile(term, re.IGNORECASE)
        result = re.findall(regular_expression, string_to_search)
        return len(result)
    except Exception, exception_instance:
        logging.error('Issue parsing term: ' + str(term) + ' from string: ' + str(string_to_search) + ': ' + str(exception_instance))
        return 0

def term_match(string_to_search, term):
    try:
        regular_expression = re.compile(term, re.IGNORECASE)
        result = re.findall(regular_expression, string_to_search)
        return result[0]
    except Exception, exception_instance:
        logging.error('Issue parsing term: ' + str(term) + ' from string: ' + str(string_to_search) + ': ' + str(exception_instance))
        return None


def create_resume_df(data_path):
    # Create a list of documents to scan
    logging.info('Searching path: ' + str(data_path))

    # Find all files in the data_path which end in `.pdf`. These will all be treated as resumes
    path_glob = os.path.join(data_path, '*.pdf')

    # Create list of files
    file_list = glob.glob(path_glob)
    
    name_list=[]*len(file_list)
    namelist=[]*len(file_list)
    for i in file_list:
        for j in range(0,len(i)):
            if i[j]=='\\':
                s1=i[j+1:len(i)]
                name_list.append(s1)
    for i in name_list:
        name_string=i.split('_') 
        s=name_string[1]
        if s[len(s)-1]=='f' and s[len(s)-2]=='d' and s[len(s)-3]=='p' and s[len(s)-4]=='.': 
            namelist.append(name_string[0]+" "+s[:len(s)-4])
        else:
            namelist.append(name_string[0]+" "+name_string[1])
    rgpa=float(input("Enter The Pointer Criteria: "))
    #logging.info('Iterating through file_list: ' + str(file_list))
    resume_summary_df = pd.DataFrame()
    
    #Store metadata, raw text(ResumeText),and word count
    resume_summary_df["file_path"] = file_list
    resume_summary_df["raw_text"] = resume_summary_df["file_path"].apply(convert_pdf_to_txt)
    resume_summary_df["num_words"] = resume_summary_df["raw_text"].apply(lambda x: len(x.split()))

    #contact information
    resume_summary_df["Name"]=namelist
    resume_summary_df["phone_number"] = resume_summary_df["raw_text"].apply(check_phone_number)
    resume_summary_df["email"] = resume_summary_df["raw_text"].apply(check_email)
    resume_summary_df["email_domain"] = resume_summary_df["email"].apply(functools.partial(term_match, term=r"@(.+)"))
    resume_summary_df["HackerRankProfile"] = resume_summary_df["raw_text"].apply(functools.partial(Extract_Links,term=r"hackerrank"))
    resume_summary_df["CodechefProfile"] = resume_summary_df["raw_text"].apply(functools.partial(Extract_Links,term=r"codechef"))
    resume_summary_df["LinkedinProfile"] = resume_summary_df["raw_text"].apply(functools.partial(Extract_Links, term=r"linkedin"))
    resume_summary_df["GithubProfile"] = resume_summary_df["raw_text"].apply(functools.partial(Extract_Links,term=r"github"))

    #skill information
    resume_summary_df["Java_Skills"] = resume_summary_df["raw_text"].apply(functools.partial(term_count, term=r"java"))
    resume_summary_df["Python_Skills"] = resume_summary_df["raw_text"].apply(functools.partial(term_count, term=r"[pP][yY][tT][hH][oO][nN]"))
    resume_summary_df["C++_Skills"] = resume_summary_df["raw_text"].apply(functools.partial(term_count, term=r"c[\+][\+]"))
    resume_summary_df["MySql_Skills"] = resume_summary_df["raw_text"].apply(functools.partial(term_count, term=r"mysql"))
    resume_summary_df["OracleSql_Skills"] = resume_summary_df["raw_text"].apply(functools.partial(term_count, term=r"sql"))
    resume_summary_df["Analytics"] = resume_summary_df["raw_text"].apply(functools.partial(term_count, term=r"analytics"))
    resume_summary_df["API"]= resume_summary_df["raw_text"].apply(functools.partial(term_count, term=r"API[']?[sS]?"))

    resume_summary_df["CGPA"]=  resume_summary_df["raw_text"].apply(check_cgpa)
    resume_summary_df["shortlist"]=  resume_summary_df["raw_text"].apply(functools.partial(check_gpa,term=rgpa))
    #Return DF
    return resume_summary_df

if __name__ == '__main__':
    main()
