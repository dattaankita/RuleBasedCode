import os
import re
import csv

def predict(filePath):
    """Predicts whether the table is a rate table or not

    Parameters
    ----------
    filePath : string
        Path of the RCT format extracted text

    Returns
    -------
    arg : bool
        0 if the table isn't a rate table and 1 if it is a rate table
    """
    try:
        f=open(filePath,'r')    #table details from text files will be provided
        # print("File read")
    except(FileNotFoundError,IOError):  # handling exceptions
        # print("Exception thrown")
        return 0

    data=f.readlines()

    if len(data)>0:
        #if data exists in the file
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'headers.txt'),'r') as fx:
            rowNames=fx.readlines()

        rowNames=[x.strip() for x in rowNames]
#        rowNames=['employee','spouse & child','spouse','child','spouse!','i obacco','non- 1 obacco']  #to be provided by tulasi
        #columnNames=['employee','spouse & child','spouse','child','spouse!']   #to be provided by tulasi

        data = [p.strip() for p in data if p.strip()]
        # print("Data 1", data)
        data = [ [x1.strip() for x1 in x.split('||')] for x in data]
        # print("Data 2", data)
        sum = 0


        for x in data:
            rule1=0
            rule2=0
            rule3=0
            x= [ j.lower() for j in x if type(j)==str ]
            #if lot of characters (greater than 50) or if the end value has a date
            if (len(x[len(x)-1])>50) or len(re.findall('\d+\/\d+\/\d+',x[len(x)-1]))>0:
                rule1 = 0

            else:
                #if the end value has a $ or % or digits - highly probable of eing a useful value
                if len(re.findall('\$|\%|\d+',x[len(x)-1]))>0:
                    rule1 = 1
                else:
                #otherwise is usually not useful
                    rule1 = 0


            #case1: if row or column name exists then +1
            for i in range(len(x)-1):
                if((x[i] in rowNames) or len(re.findall('\<\d+|\d+\-\d+|\d+\+|\$\d+',x[i])))>0:
                    rule3 = 0.5
                    break


            for j in x:
                #case2: if subscriber|amount exist the replace 0
                if len(re.findall('subscriber|amount',j))>0:
                    break
                #case3: if keyword exists then +1
                if len(re.findall('rate*|month*|week*|per|premium|contribution',j))>0:
                    rule2 = 0.5
                    break
                else:
                    pass

            score = rule1 * (rule2 + rule3)
            sum = sum + score

        if not len(data):
            return 0

        if sum/(len(data))>=0.5:
            return 1
        else:
            return 0

    else:
        return 0


if __name__ == "__main__":
        # filePath = ''  #filepath
        file = "1-2018 Benefit Rates_page_1-0_extracted.txt"
        # filePath = os.path.join(r"C:\CYGWIN64\home\bhojanes\full_pipeline_debug_1\integeratedFiles\all_txt", file)
        filePath = os.path.join(r"C:\CYGWIN64\home\bhojanes\full_pipeline_debug_1\input\1-2018 Benefit Rates\pdf_2_image", file)
        result = predict(filePath)
        if result==1:
            # print('It is Rate table')
            #print(file + ":True")
            arr = [file, "True"]
        else:
            # print('It is not Rate table')
            #print(file + ":False")
            arr = [file, "False"]
        with open("output.csv", 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(arr)
            
        csvFile.close()
            
