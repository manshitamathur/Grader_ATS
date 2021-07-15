from typing import ContextManager
from django.shortcuts import render
from .forms import ATS_Form, ResumeForm
from . models import Document, Document_ATS

from nltk.tokenize import word_tokenize 
# from nltk.corpus import stopwords
# set(stopwords.words('english'))

from .utils import get_plot

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import PyPDF2
import random
import string
import sys,os,math
from django.core.files.storage import default_storage
import os
import re
# import slate3k as slate
import pdfplumber , pdfminer 

import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

def home(request):
    try:
        if request.method == 'POST':
            file2=request.FILES['myfile']
            print(file2)
            res="Resume_"
            res+= ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
            resume=Document.objects.create(filename=res,document=file2)
            resume.save()
            my_id=resume.id
            myresume=Document.objects.get(filename=res)
            f = default_storage.open(os.path.join('', str(myresume.document)), 'rb')
            val=request.POST.get('Domain')
            index=int(val)
            # text= slate.PDF(f)
            # text=str(text)
            # text = text.translate(str.maketrans('','',string.punctuation))
            # text = re.sub(r'\n','',text)
            # text=re.sub("nn•",'',text)
            # text=re.sub("n●",'',text)
            # pattern = r'[0-9]'
            # text=re.sub(pattern, '',text)
            # text= re.sub(r'[^\x00-\x7f]',r' ', text) 
            
            with pdfplumber.open(f) as pdf:
                page=pdf.pages[0]
                text1=page.extract_text()
                text1.replace('\n','')
                text=text1.lower()
                print(text.split())
                datascince = {'Skills':['python','sql','powerbi','power bi', 'jupyter', 'pandas', 'excel', 'data science',
                            'machine learning', 'machine', 'analytics', 'tableau','cdp', 'ai', 'artificial intelligence',
                            'intelligence', 'leader', 'leadership','supervised learning','unsupervised learning'],
                    'Projects': ['program','project', 'application', 'efficiency', 'efficient', 'prediction', 'predicted',
                                'predictive','api', 'big data', 'mining', 'deep learning', 'databases', 'dbms', 'programming',]}
                web_dev = {'Skills':['html','css','responsive','javascript','testing','debugging','seo','search engine optimization','sql',
                    'front-end','bootstrap','expressjs','hosting','node.js','angular','react','ajax','deployment','firebase','user-friendly'], 
                'Projects':['layout','javascript','seo-friendly','responsive','counter','social','transcript','react','visualer','notifier','front-end',
                        'expressjs','editor','hosting','deployment','jwt','jquery','development','firebase','plugin']}

                soft_dev = {'Skills':['java','python','c#','.net','mean','ruby','object oriented design','testing','debugging',
                    'problem solving' ,'logical','thinking','verbal' ,'communication','teamwork','data structures and algorithms','data structures',
                    'dsa','coding','databases','operating systems','sdlc','software development lifecycle','c programming','c++','deployment'],
                'Projects':['android','algorithm','json','game','social','website','application','chatbot','sclabale','product','platform',
                            'tool','deployment','user-friendly']}
                testing = {'Skills':['communication','selenium','problem-solving','documentation','c++','java','analysis','php',
                    'quality assurance','qa','automated testing','troubleshooting','software','testing','manual testing','test reports',
                    'metrics','scripting','databases','programming','design','c' ,'devoops','agile','web','sdlc','software development lifecycle',
                    'scrum','lean','waterfall','application development','rational analysis','thinking','reasoning','testing tools','gui',
                    'penetration testing','security','black box','planning','project management','reporting','linux','apache','mysql'],
                'projects':['estimation','functional','lamp','linux','apache','mysql','php','application','interface','maintainance',
                    'operations','smoke testing','tracking','regression','sanity testing','comprehensive','non-functional','usablity',
                    'performance','test-cases','verify','precondition','webdriver','commands','selenium','test','scenario','model','design','user']}

                human_resource = {'Skills':['communication','decision-making','training','developmental','empathic','finance','organizational',
                    'business','management','leadership','strategic','thinking' ,'technical' ,'multi-tasking',
                    'interactive','written','content','strategy','experience','manager','sessions','performance',
                    'development','efficient','productive','recruitment','databases','microsoft office',
                    'proficient','organized','communicator','attentive','applicant','screening','analysis','respectful','mba'],
                'Projects':['ats','applicant tracking systems','feedback','mechanisms',
                    'recruitment','managed','hiring','posting','compensation','Conduct','operational',
                    'review','performance','cost-effective','workforce','planning','business','strategy',
                    'training','team building','information system']
                }

                ui_ux= {'Skills' :['scenario','information','architecture','navigation','wireframing','prototyping',
                    'visual communication','typography','design','soft skills','collaboration','writing',
                    'empathy','interaction design','coding','analytics','photoshop','design tools','saas',
                    'seo','html','css','bootstrap'],
                'Projects':['website','responsive','saas','seo','cta','pr','logical',
                'user-friendly','opt-in forms','digital','prototype','problem solving',
                'javascript','debugging','jquery','axure','proto.io','collaboration','webflow',
                'bootstrap','interaction design','html','css']}
                
                data_analyst = {
                'Skills' : ['python','sql','r','data' ,'visualization','statistics','tableau',
                'power bi','matlab','spreadsheets','preprocessing','excel','interpretation',
                'machine learning','regression' 'analysis','nosql','data cleaning','pattern',
                'recognition','data analysis','exploratory data analysis','communication',
                'presentation' ],
                'Projects' : ['matplotlib','pandas','numpy','jupyter','spyder',
                'seaborn','report writing','problem solving','business acumen',
                'detail','management','collaboration','teamwork','data science',
                'r','model','python','databases','collaboratory','tools','anaconda',
                'eda','research','data','modelling','structured query language','sas','apache',]

                }
                S_and_M={'Skills':['communication','prospecting','discovery','business' 
                ,'acumen','social','selling','storytelling','active','listening','handling',
                'presentation', 'negotiation' ,'territory' ,'management','technology','buyer'
                 ,'research','time management','planning','curiosity','judgment','collaboration',
                 'product'],
                'Projects':['digital','marketing','study','analysis','strategy',
                'brand','management','promotion','digitalization','industry','satisfaction',
                'sale','services','acquisition','event','comparative','evaluation','tools',
                'techniques','report','company','product','research']
                }

                my_domains = [datascince,web_dev,testing,human_resource,ui_ux,data_analyst,S_and_M,soft_dev]
                        
                skills = 0
                projects = 0
                scores = []
                skills_list=[]
                projects_list=[]
                for area in my_domains[index].keys():
                    if area == 'Skills':
                        for word in my_domains[index][area]:
                            if word in text.split():
                                skills+=1   
                                print(word)        
                        scores.append(skills)
                    else:
                        for word in my_domains[index][area]:
                            if word in text.split():
                                projects+=1
                                print(word)
                        scores.append(projects)
                print(skills,projects)
                print("SKILLS {}",skills)
                print("PROJECTS {}",projects)
                if skills<=3:
                    skills_percentage = random.uniform(15,25)
                elif skills>3 and skills <5:
                    skills_percentage = random.uniform(26,40)
                elif skills>=5 and skills<=6:
                    skills_percentage= random.uniform(41,55) 
                elif skills>6 and skills<=8:
                    skills_percentage = random.uniform(56,70)
                elif skills>8 and skills<=10 :
                    skills_percentage = random.uniform(71,85)
                else :
                    skills_percentage = random.uniform(85,95)

                if projects<=3:
                    projects_percentage = random.uniform(15,25)
                elif projects>3 and projects <5:
                    projects_percentage = random.uniform(26,40)
                elif projects>=5 and projects<=6:
                    projects_percentage= random.uniform(41,55) 
                elif projects>6 and projects<=8:
                    projects_percentage = random.uniform(56,70)
                elif projects>8 and projects<=10 :
                    projects_percentage = random.uniform(71,85)
                else :
                    projects_percentage = random.uniform(85,95)


                skills_star=round((skills_percentage*5)/100)

                projects_star = round((projects_percentage*5)/100)

                projects_final = "{:.1f}".format(projects_percentage)
                skills_final = "{:.1f}".format(skills_percentage)

                pro= "width :"+"{:.2f}".format(projects_percentage)+"%"
                ski= "width :"+"{:.2f}".format(skills_percentage)+"%"
                print("projcts-star {}".format(projects_star))
                print("skills-star {}".format(skills_star))

                for i in range(skills_star):
                    skills_list.append('a')
                for i in range(projects_star):
                    projects_list.append('a')
                skills_left_stars = 5-skills_star
                projects_left_stars = 5-projects_star
                skills_list_left=[]
                projects_list_left=[]
                for i in range(skills_left_stars):
                    skills_list_left.append('a')
                for i in range(projects_left_stars):
                    projects_list_left.append('a')  
                print("{}\n {}\n {}\n {}",projects_list,skills_list,projects_list_left,skills_list_left)      
                #print("skills :{} ,skills_star :{},projects :{},projects_star:{}".format(skills,skills_star,projects,projects_star))
                context={'skills':skills_final,'skills_star':skills_star,'projects':projects_final,'projects_star': projects_star,'pro':pro,'ski':ski,'projects_list':projects_list,'skills_list':skills_list,'projects_list_left':projects_list_left,'skills_list_left':skills_list_left}
                print(context)

                instance= Document.objects.filter(id=my_id)
                instance.delete()
                return render(request,'Results.html',context)

                        
        else:
            form = ResumeForm()

    except Exception as e:
        # exc_tb = sys.exc_info()
        # print(e,exc_tb.tb_lineno)
        #except Exception as e:
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return render(request,'home1.html')
        
        
    return render(request, 'home1.html')


def ATS_HomePage(request):
    try:
        if request.method == 'POST':
            file2=request.FILES['myresume']
            print(file2)
            res="Resume_"
            res+= ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
            resume=Document.objects.create(filename=res,document=file2)
            resume.save()
            my_id=resume.id
            myresume=Document.objects.get(filename=res)
            f = default_storage.open(os.path.join('', str(myresume.document)), 'rb')
            job_description =request.POST.get('job_description')
            text = [resume, job_description]
            with pdfplumber.open(f) as pdf:
                page=pdf.pages[0]
                text1=page.extract_text()
                text1.replace('\n','')
                resume=text1.lower()
                print(resume)
                text = [resume, job_description]
                from sklearn.feature_extraction.text import CountVectorizer
                cv = CountVectorizer()
                count_matrix = cv.fit_transform(text)
                from sklearn.metrics.pairwise import cosine_similarity

                # Print similarity scores
                print("\nSimlarity Scores:")
                print(cosine_similarity(count_matrix))
                matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
                matchPercentage = round(matchPercentage)
                print("Your resume matches about " + str(matchPercentage) + "% of the job description.")
                return render(request,'demo.html')
        else:
            form = ATS_Form()

    except Exception as e:
        # exc_tb = sys.exc_info()
        # print(e,exc_tb.tb_lineno)
        #except Exception as e:
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return render(request,'ATS_Homepage.html')

    return render(request, 'ATS_Homepage.html')


def clean_job_decsription(jd):
    ''' a function to create a word cloud based on the input text parameter'''
    ## Clean the Text
    # Lower
    clean_jd = jd.lower()
    # remove punctuation
    clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
    # remove trailing spaces
    clean_jd = clean_jd.strip()
    # remove numbers
    clean_jd = re.sub('[0-9]+', '', clean_jd)
    # tokenize 
    # from nltk.tokenize import word_tokenize 
    clean_jd = word_tokenize(clean_jd)
    # remove stop words
    stop = stopwords.words('english')
    #stop.extend(["AT_USER","URL","rt","corona","coronavirus","covid","amp","new","th","along","icai","would","today","asks"])
    clean_jd = [w for w in clean_jd if not w in stop] 
    
    return(clean_jd)

def read_pdf_resume(f):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    # with open(pdf_doc, 'rb') as fh:
    for page in PDFPage.get_pages(f, 
                                caching=True,
                                check_extractable=True):
        page_interpreter.process_page(page)
            
        text = fake_file_handle.getvalue()
    
    # close open handles
    converter.close()
    fake_file_handle.close()
    
    if text:
        return text

def get_resume_score(text):
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(text)
    #Print the similarity scores
    print("\nSimilarity Scores:")
    #print(cosine_similarity(count_matrix))
    #get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2) # round to two decimal
    return matchPercentage


def ATS_HomePage1(request):
    try:
        # def clean_job_decsription(jd):
        #     ''' a function to create a word cloud based on the input text parameter'''
        #     ## Clean the Text
        #     # Lower
        #     clean_jd = jd.lower()
        #     # remove punctuation
        #     clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
        #     # remove trailing spaces
        #     clean_jd = clean_jd.strip()
        #     # remove numbers
        #     clean_jd = re.sub('[0-9]+', '', clean_jd)
        #     # tokenize 
        #     clean_jd = word_tokenize(clean_jd)
        #     # remove stop words
        #     stop = stopwords.words('english')
        #     #stop.extend(["AT_USER","URL","rt","corona","coronavirus","covid","amp","new","th","along","icai","would","today","asks"])
        #     clean_jd = [w for w in clean_jd if not w in stop] 
            
        #     return(clean_jd)
        if request.method == 'POST':
            file2=request.FILES['myresume']
            print(file2)
            res="Resume_"
            res+= ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
            resume=Document_ATS.objects.create(filename=res,document=file2)
            resume.save()
            my_id1=resume.id
            myresume=Document_ATS.objects.get(filename=res)
            f = default_storage.open(os.path.join('', str(myresume.document)), 'rb')
            jd =request.POST.get('job_description')
            res_text = read_pdf_resume(f)
            print(res_text)
            # clean_jd = clean_job_decsription(job_description)

            ## Clean the Text
            # Lower
            clean_jd = jd.lower()
            # remove punctuation
            clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
            # remove trailing spaces
            clean_jd = clean_jd.strip()
            # remove numbers
            clean_jd = re.sub('[0-9]+', '', clean_jd)
            # tokenize 
            # from nltk.tokenize import word_tokenize 
            clean_jd = clean_jd.split(' ')
            # clean_jd = word_tokenize(clean_jd)
            # clean_jd1 = clean_jd.replace('.','')
            # remove stop words
            # stop = stopwords.words('english')
            stop= {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than','done'}
            #stop.extend(["AT_USER","URL","rt","corona","coronavirus","covid","amp","new","th","along","icai","would","today","asks"])
            clean_jd = [w for w in clean_jd if not w in stop] 
            print(clean_jd)

            chart = get_plot(clean_jd)
            text = [res_text, jd]
            Result = get_resume_score(text)
            instance= Document_ATS.objects.filter(id=my_id1)
            instance.delete()

            return render(request,'samplechart.html',{'chart':chart,'Result':Result})
        else:
            form = ATS_Form()

    except Exception as e:
        # exc_tb = sys.exc_info()
        # print(e,exc_tb.tb_lineno)
        #except Exception as e:
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        return render(request,'exceptions.html',{'e':e})

    return render(request, 'ATS_Homepage.html')



    