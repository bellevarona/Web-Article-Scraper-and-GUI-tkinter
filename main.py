from newspaper import Article
import nltk
import urllib.request
import os
from tkinter import *
from tkinter import filedialog

def dl_article_images(article,dir):
    os.chdir(dir)
    print("All Images: \n")
    count = 1
    for i in article.images:
        # all_images_url.append(i)
        # filename = i.split('/')[-1]
        
        try:
            urllib.request.urlretrieve(i, str(count)+'.jpg')
            print('success: '+i+'\n')
            count += 1
                
        except:
            print('fail: '+i+'\n')
            count += 1
            continue
    os.chdir("../")
    
def get_authors(authors):
    strAuthors=''
    try:
        for p in authors:
            strAuthors += p + ','
        strAuthors=strAuthors[:-1]

        if len(authors)==0:
            return "No authors found"
    except:
        strAuthors+= "No authors found"
    return strAuthors

def get_keywords(keywords):
    strKeywords=''
    try:
        for k in keywords:
            strKeywords += k + ', '
        strKeywords=strKeywords[:-2]
    except:
        strKeywords+= "No keywords found"
    return strKeywords

def get_pubDate(pubDate):
    try:
        return pubDate.strftime("%m-%d-%Y")
    except:
        return "No published date found"

def check_titleName(title):
    invalid = ['*', '.', '"', '/','[', ']', ':', ';', '|', ',','?']
    for i in title:
        print('i')
        if i in invalid:
            title = title.replace(i,'-')
    while(title[len(title)-1]==' '):
        title=title[:-1]
    return title

def create_metadata(url):
    # url = URL_gui.get()
    article = Article(url)
    article.download()
    article.parse()

    nltk.download('punkt')
    article.nlp()

    # Create folder according to name
    title = str(article.title)
    print(title + '\n')

    new_folder_name = os.path.join(os.getcwd(),check_titleName(title))
    os.mkdir(new_folder_name)

    # Create txt file to save metadata
    metadata_FileName = os.path.join(new_folder_name,'metadata.txt')

    l1 = "Article Title: " + title
    l2 = "\n\nAuthor/s: " + get_authors(article.authors) 
    l3 = "\n\nDate Published: " + get_pubDate(article.publish_date)
    l4 = "\n\nSummary: " + article.summary
    l5 = "\n\nKeywords: " + get_keywords(article.keywords)

    metadata = l1+l2+l3+l4+l5

    with open(metadata_FileName,'w') as f:
        f.write(metadata)
    os.startfile(metadata_FileName)     

    
    # Create txt file to save the full article
    article_FileName = os.path.join(new_folder_name,'article.txt')
    with open(article_FileName,'w', encoding="utf-8") as f:
        f.write(str(article.text))

    dl_article_images(article,new_folder_name)

# Choose txt file thru dialog box
root = Tk()
root.filename = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))

with open(root.filename) as file:
    urls = file.readlines()

# main
for i in urls:
    create_metadata(i)


