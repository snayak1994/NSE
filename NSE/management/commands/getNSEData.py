from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import logging
from io import BytesIO
from zipfile import ZipFile
from urllib import urlopen
from datetime import datetime, timedelta
import csv
import os
monthMap = {1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}
now = datetime.now()

logger = logging.getLogger(__name__)

class LoadNseData():
    def __init__(self,days=30):
        self.days = days
        self.index = 0
        self.readFiles = []

    def __len__(self):
        return len(self.readFiles)
    
    def deleteOldFiles(self):
        for (root,dirs,files) in os.walk(settings.FILES_PATH, topdown=True):
            for f in files:
        	os.unlink(os.path.join(root, f))
        	
    def getNseData(self):
        while len(self.readFiles)<self.days:
            new_date = now - timedelta(days=self.index)
            #print new_date
            dayNew = str("0"+str(new_date.day)) if len(str(new_date.day))==1 else str(new_date.day)
            if new_date.weekday()<5:
                requestUrl = "https://archives.nseindia.com/content/historical/EQUITIES/"+str(new_date.year)+"/"+monthMap[new_date.month]+"/cm"+dayNew+monthMap[new_date.month]+str(new_date.year)+"bhav.csv.zip"
                print requestUrl
                try:
                    url = urlopen(requestUrl)
                    with ZipFile(BytesIO(url.read()), 'r') as zip_ref:
                        zip_ref.extractall(settings.FILES_PATH)
                    with open(os.path.join(settings.FILES_PATH,"cm"+dayNew+monthMap[new_date.month]+str(new_date.year)+"bhav.csv"), 'r') as file:
                        print "cm"+dayNew+monthMap[new_date.month]+str(new_date.year)+"bhav.csv"
                        reader = csv.reader(file)
                        for row in reader:
                            if not row[0] == 'SYMBOL':
                                filename = os.path.join(settings.FILES_PATH,row[0]+".csv")
                                if os.path.exists(filename):
                                    with open(filename,"a") as resFile:
                                        writer = csv.writer(resFile)
                                        writer.writerow(row[:9]+[row[10]])
                                else:
                                    with open(filename,"w+") as resFile:
                                        writer = csv.writer(resFile)
                                        writer.writerow(row[:9]+[row[10]])
                    self.readFiles.append(filename)
                except Exception,e:#if url is not found
                    pass
            self.index+=1
    
class Command(BaseCommand):
    #print sys.argv
    args = ''
    help = 'Reads NSE data for last 30 days and populates in '+settings.FILES_PATH

    def handle(self, *args, **options):      
        try:
            runTasks()
        except Exception as e:                
            self.stdout.write('Error %s' % e) 
            logger.exception(e)
        self.stdout.write('done')      
        return

def runTasks() :
    try:
        print "Start Script"
        obj = LoadNseData(30)
        obj.deleteOldFiles()
        obj.getNseData()
        print len(obj)
    except Exception as E:
        logger.info(str(E));
