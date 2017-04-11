import os
import bs4 as bs
import urllib.request
import re
import warnings
import tabula_wrapper
import pandas as pd

def get_pdf_links():            #function to parse the pdfs links from webpage to make a dictonaries of key as year and value as corr. pdf
    page_handle = urllib.request.urlopen("https://www.apollohospitals.com/corporate/investor-relations/annual-reports")
    webpage = page_handle.read()
    page_handle.close()
    
    soup = bs.BeautifulSoup(webpage, 'html.parser') 
    
    req_tag = soup.find_all('div', itemprop="articleBody")
    tag = req_tag[0]
    pdf_tags = tag.find_all('a')
    
    pdf_links = ['https://www.apollohospitals.com'+link.get('href') for link in reversed(pdf_tags)]
    years = list(range(2006,2017))
    coll = dict(zip(years, pdf_links))

    return coll

def download_pdf(download_url):                                        #function to download pdfs
    print('downloading the requested PDF......')
    response = urllib.request.urlopen(download_url)
    file = open("appolo.pdf", 'wb')
    file.write(response.read())
    file.close()
    response.close()
    print("Download Completed\n\nFile name is : appolo.pdf")

def get_table_coordinates(directory):                                #function returns the coordinates of the tables on the pdf page
    dir_coords = directory
    coord = []
    for i in list(range(4)):
        f = open(dir_coords+str(i+1)+'.sh', 'r')
        str_coord = re.findall("\d+\.\d+", f.read())
        float_coord = [float(string) for string in str_coord]
        coord.append(float_coord)
        f.close()
    
    return coord

def output_tables_csv(pages):                                       #function output the tabels of the pages in .csv format 
    for i,page,j in zip(coordinates, pages,range(4)):
        df = tabula_wrapper.read_pdf("appolo.pdf", area=i, pages=page)
        df.to_csv("table"+str(j+1)+".csv")
        print('\n\n\ntable',j+1,'extracted\n')
        print('open table'+str(j+1)+'.csv\n\n\n')


# Main PROGRAMME
warnings.filterwarnings("ignore")

links = get_pdf_links()       # get all the pdfs links
download_pdf(links[2015])     # Enter the required year for which the ANNUAL Report is to be downloaded 


#pdf analysis is done for annual report 2015
pages = [21, 21, 24, 25]      #page numbers for the required pages for 2015
coordinates = get_table_coordinates(os.getcwd()+'/sh_files15/table') #get the coordinates of the tables in the pages mentioned
output_tables_csv(pages)      

