#!/usr/local/bin/python3
from tkinter import * 
from tkinter import filedialog
from tkinter import ttk
import io

from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import messagebox
import os
import time
import subprocess
import sys


#This creates a app window
root = Tk()
root.title('Hegele Tools') 
root.geometry('500x250')
#opt states the option for the process we can do 
opt=["CAD267_Analysis",
"Bed_file_Analysis"]
w = Label(root, text = "Welcome to Hegele Tools",  
        font = ("Helvetica", 20), pady = 10)
w.pack()

w2 = Label(root, text = "Select a process",  
        font = ("Helvetica", 14))
w2.pack()

var = StringVar(root)  # initialization of a common StringVar for both OptionMenu and Label widgets
# The following variables states the percentage of the work completed, progress, and status of the processes 
percent = Label(root, text="", anchor=S) 
progress = Progressbar(root, length=500, mode='determinate')    
status = Label(root, text="Select a Process from the drop down Menu and Follow the instructions", relief=SUNKEN, anchor=W, bd=2) 



status.pack(side=BOTTOM, fill=X)
percent.pack(side= BOTTOM)
progress.pack(side=BOTTOM)
class MyOptMenu(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        var.set(opt[0])  # give an initial value to the StringVar that will be displayed first on the OptionMenu
        self.om = OptionMenu(self, var, *opt, command = self.toggle) # this is the optionMenu widget itself
        self.om.pack(side=TOP)
        self.submit = Button(self, text = "submit")
        var.trace('w', self.getValue)   # continuously trace the value of the selected items in the OptionMenu and update the var variable, using the function self.getValue
    
    def getValue(self, *args):
        return(var.get())
        self.quit()  # return the current value of OptionMenu
    
    def toggle(self, item):
        #Packs the selected widget
        if item == 'CAD267_Analysis': 
            self.but = Button(self, text = "Click Me to start the analysis", # Click this button for starting CAD267 process
            command = self.cad_analysis).pack()
        if item == 'Bed_file_Analysis':
            self.but = Button(self, text = "Click Me to start the analysis", #Click this button for starting bedfile analysis 
            command = self.bed_analysis).pack()

    ##cad267 analysis starts here 

#-------------------------------------------------------------------------------------------------------------------------------
    
    def multiple_files(self):

    
    def normal_analysis(self):
        qmsgbox = messagebox.showinfo('Select a Directory', "Select your directory that contains the samples")
        path = filedialog.askdirectory()
        print(path)
        file_list = []
        for fn in os.listdir(path):
            if not fn.startswith((".")) and fn.endswith(('.vcf.gz')):
                file_list.append(fn)
        bmsgbox = messagebox.showinfo("Select Bed file", "Please select the bed file you are working with")
        bedfilename = filedialog.askopenfilename(initialdir=path , filetypes =[('Bed Files', '*.bed')])
        bedfilename = bedfilename.rsplit("/",1)[1]
        bedfilename_minusbed = bedfilename.rsplit(".",1)[0]
        subprocess.run(["mkdir Result"], shell=True)
        subprocess.run(["mkdir UnzippedCleanedVCFfiles"], shell=True)
        for filename in file_list:
            counter = 0
            alist = ["Cleaning " +str(bedfilename), "Cleaned " +str(bedfilename), "Preparing to clean " + str(filename),"Cleaning " + str(filename), "Cleaned " + str(filename), "Finding bed file instances in " + str(filename), "Found all instances in " + str(filename)]
            no_gz = filename.rsplit(".", 1)[0]
            
            for i in alist:
                if alist[0] == alist[counter]:
                    step= "{}".format(i) 
                    subprocess.run(["sed 's/chr//g' " + str(bedfilename)], shell=True)
                    progress["value"] = 15
                    percent['text'] = "{}%".format(15)
                    status["text"] = "{}".format(step)
                    counter += 1
                    root.update()
                    time.sleep(0.5)
                elif alist[1] == alist[counter]:
                    step= "{}".format(i)
                    progress["value"] = 30
                    percent['text'] = "{}%".format(30)
                    status["text"] = "{}".format(step)
                    counter += 1
                    root.update()
                    time.sleep(0.5)
                elif alist[2] == alist[counter]:
                    step= "{}".format(i)
                    subprocess.run(["Gzip -k -d " + str(no_gz)], shell=True)
                    progress["value"] = 45
                    percent['text'] = "{}%".format(45)
                    status["text"] = "{}".format(step)
                    counter += 1
                    root.update()
                    time.sleep(0.5)
                elif alist[3] == alist[counter]:
                    step= "{}".format(i)
                    subprocess.run(["sed -i -e 's/[<>,]//g' " + str(no_gz)], shell=True)
                    subprocess.run(["rm " + str(no_gz) + "-e"], shell=True)
                    progress["value"] = 60
                    percent['text'] = "{}%".format(60)
                    status["text"] = "{}".format(step)
                    counter += 1
                    root.update()
                    time.sleep(0.5)
                elif alist[4] == alist[counter]:
                    step= "{}".format(i)
                    progress["value"] = 75
                    percent['text'] = "{}%".format(75)
                    status["text"] = "{}".format(step)
                    counter += 1
                    root.update()
                    time.sleep(0.5)
                elif alist[5] == alist[counter]:
                    step= "{}".format(i)
                    subprocess.run(["bedtools intersect -a " + str(no_gz) + " -b " + str(bedfilename) + " -header > " + str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf"], shell=True)
                    progress["value"] = 90
                    percent['text'] = "{}%".format(90)
                    status["text"] = "{}".format(step)
                    counter += 1
                    root.update()
                    time.sleep(0.5)
                elif alist[6] == alist[counter]:
                    step= "{}".format(i)
                    progress["value"] = 100
                    percent['text'] = "{}%".format(100)
                    status["text"] = "{}".format(step)
                    subprocess.run(["mv " + str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf Result"], shell=True)
                    subprocess.run(["mv " + str(no_gz) + " UnzippedCleanedVCFfiles"], shell=True) 
                    counter += 1
                    root.update()
                    time.sleep(0.5)

        msgbox = messagebox.askquestion('Info', "Process completed! Would you like to do any additional steps?")
        if msgbox == "no":
            sys.exit()
        else:
            messagebox.showinfo("Return", "You will now return to the application screen")



    def zerozeroremoval(self):
        try: # this is to help see if the process can be completed so it will "try"
            qmsgbox = messagebox.askquestion('Question', "Would you like to run the bed file against all the samples in this directory?") #qmsgbox asks if you want to compare the bed file to all the vcf samples in the directory or would you like to select a specific one
            if qmsgbox == "yes":
                qmsgbox = messagebox.showinfo('Select a Directory', "Select your directory that contains the samples")
                path = filedialog.askdirectory()
                print(path)
                file_list = []
                for fn in os.listdir(path):
                    if not fn.startswith((".")) and fn.endswith(('.vcf.gz')):
                        file_list.append(fn)
                bmsgbox = messagebox.showinfo("Select Bed file", "Please select the bed file you are working with")
                bedfilename = filedialog.askopenfilename(initialdir=path , filetypes =[('Bed Files', '*.bed')])
                bedfilename = bedfilename.rsplit("/",1)[1]
                bedfilename_minusbed = bedfilename.rsplit(".",1)[0]
                subprocess.run(["mkdir Result"], shell=True)
                subprocess.run(["mkdir UnzippedCleanedVCFfiles"], shell=True)
                zmsgbox = messagebox.askquestion("0/0 Instances", "Would you like to remove all 0/0 instances from the result file?")
                if zmsgbox == "yes":
                    subprocess.run(["mkdir ZeroZeroRemoved"], shell=True)
                    for filename in file_list:
                        alist = ["Cleaning " +str(bedfilename), "Cleaned " +str(bedfilename), "Preparing to clean " + str(filename),"Cleaning " + str(filename), "Cleaned " + str(filename), "Finding bed file instances in " + str(filename), "Found all instances in " + str(filename)]
                        counter = 0
                        no_gz = filename.rsplit(".", 1)[0]
                        for i in alist:
                            if alist[0] == alist[counter]:
                                step= "{}".format(i) 
                                subprocess.run(["sed 's/chr//g' " + str(bedfilename)], shell=True)
                                progress["value"] = 15
                                percent['text'] = "{}%".format(15)
                                status["text"] = "{}".format(step) 
                                counter += 1
                                root.update()
                                time.sleep(0.5)
                            elif alist[1] == alist[counter]:
                                step= "{}".format(i)
                                progress["value"] = 30
                                percent['text'] = "{}%".format(30)
                                status["text"] = "{}".format(step)
                                counter += 1
                                root.update()
                                time.sleep(0.5)
                            elif alist[2] == alist[counter]:
                                step= "{}".format(i)
                                subprocess.run(["Gzip -k -d " + str(filename)], shell=True)
                                progress["value"] = 45
                                percent['text'] = "{}%".format(45)
                                status["text"] = "{}".format(step)
                                counter += 1
                                root.update()
                                time.sleep(0.5)
                            elif alist[3] == alist[counter]:
                                step= "{}".format(i)
                                subprocess.run(["sed -i -e 's/[<>,]//g' " + str(no_gz)], shell=True)
                                subprocess.run(["rm " + str(no_gz) + "-e"], shell=True)
                                progress["value"] = 60
                                percent['text'] = "{}%".format(60)
                                status["text"] = "{}".format(step) 
                                counter += 1
                                root.update()
                                time.sleep(0.5)
                            elif alist[4] == alist[counter]:
                                step= "{}".format(i)
                                progress["value"] = 75
                                percent['text'] = "{}%".format(75)
                                status["text"] = "{}".format(step) 
                                counter += 1
                                root.update()
                                time.sleep(0.5)
                            elif alist[5] == alist[counter]:
                                step= "{}".format(i)
                                subprocess.run(["bedtools intersect -a " + str(no_gz) + " -b " + str(bedfilename) + " -header > " + str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf"], shell=True)
                                progress["value"] = 90
                                percent['text'] = "{}%".format(90)
                                status["text"] = "{}".format(step) 
                                counter += 1
                                root.update()
                                time.sleep(0.5)
                            elif alist[6] == alist[counter]:
                                step= "{}".format(i)
                                progress["value"] = 100
                                percent['text'] = "{}%".format(100)
                                status["text"] = "{}".format(step) 
                                subprocess.run(["grep -v 0/0 " + str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf > " + str(filename) + "_lipidseqls_" + str(bedfilename_minusbed) + "zeroremoved.vcf"], shell=True)
                                subprocess.run(["mv " +  str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + "zeroremoved.vcf ZeroZeroRemoved"], shell=True)
                                subprocess.run(["mv " + str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf Result"], shell=True)
                                subprocess.run(["mv " + str(no_gz) + " UnzippedCleanedVCFfiles"], shell=True) 
                                counter += 1
                                root.update()
                                time.sleep(0.5)

                    msgbox = messagebox.askquestion('Info', "Process completed! Would you like to do any additional steps?")
                    if msgbox == "no":
                        sys.exit()
                    else:
                        messagebox.showinfo("Return", "You will now return to the application screen")

    #if bed analysis is selected the function below will run   
    def bed_analysis(self):
        try: # this is to help see if the process can be completed so it will "try"
            qmsgbox = messagebox.askquestion('Question', "Would you like to run the bed file against all the samples in this directory?") 
            zmsgbox = messagebox.askquestion("0/0 Instances", "Would you like to remove all 0/0 instances from the result file?")#qmsgbox asks if you want to compare the bed file to all the vcf samples in the directory or would you like to select a specific one
            if qmsgbox == "yes" and zmsgbox == "yes":
                zerozeroremoval(self)
            elif qmsgbox == "yes" and zmsgbox == "no":
                normal_analysis(self)
            elif qmsgbox == "no" and zmsgbox == "yes"
                #########################################################################################################################################################################################################################
               
                ## this is when you are running the whole directory of samples but don't want to remove the zero/zero instances  
                else:
                    normal_analysis(self)
            #############################################################################################################################################################################################################################
                   
            ## This is when you are running only an individual sample and not the whole directory 
            else:
                zmsgbox = messagebox.askquestion("0/0 Instances", "Would you like to remove all 0/0 instances from the result file?")
                if zmsgbox == "yes":
                    subprocess.run(["mkdir ZeroZeroRemoved"], shell=True)
                    qmsgbox = messagebox.showinfo('Select a Directory', "Select your directory that contains the sample")
                    newpath = filedialog.askdirectory()
                    

                    for filein in os.listdir(newpath):
                        #print(filename)
                        os.rename(os.path.join(newpath,filein),os.path.join(newpath, filein.replace(' ', '_').lower())) 
                    bmsgbox = messagebox.showinfo("Select Bed file", "Please select the bed file you are working with")
                    filename = filedialog.askopenfilename(initialdir="." , filetypes =[('Bed Files', '*.bed')])
            
                    filename = filename.rsplit("/",1)[1]
                    filename_minusbed = filename.rsplit(".",1)[0]
                    vmsgbox = messagebox.showinfo("Select VCF file", "Please select the sample vcf file you are working with")
                    vcffile = filedialog.askopenfilename(initialdir=".")

                    vcffile = vcffile.rsplit("/",1)[1]
                    no_gz = vcffile.rsplit(".", 1)[0]
                    subprocess.run(["mkdir Result"], shell=True)
                    subprocess.run(["mkdir UnzippedCleanedVCFfiles"], shell=True)
                    print(no_gz)
                    alist = ["Cleaning " + str(filename), "Cleaned " +str(filename), "Preparing to clean " + str(vcffile),"Cleaning " + str(vcffile), "Cleaned " + str(vcffile), "Finding bed file instances in " + str(vcffile), "Found all instances in " + str(vcffile)]
                    counter = 0
                    for i in alist:
                        if alist[0] == alist[counter]:
                            step= "{}".format(i) 
                            subprocess.run(["sed 's/chr//g' " + str(filename)], shell=True)
                            progress["value"] = 15
                            percent['text'] = "{}%".format(15)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[1] == alist[counter]:
                            step= "{}".format(i)
                            progress["value"] = 30
                            percent['text'] = "{}%".format(30)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[2] == alist[counter]:
                            step= "{}".format(i)
                            subprocess.run(["Gzip -k -d " + str(vcffile)], shell=True)
                            progress["value"] = 45
                            percent['text'] = "{}%".format(45)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[3] == alist[counter]:
                            step= "{}".format(i)
                            subprocess.run(["sed -i -e 's/[<>,]//g' " + str(no_gz)], shell=True)
                            subprocess.run(["rm " + str(no_gz) + "-e"], shell=True)
                            progress["value"] = 60
                            percent['text'] = "{}%".format(60)
                            status["text"] = "{}".format(step)
                            
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[4] == alist[counter]:
                            step= "{}".format(i)
                            progress["value"] = 75
                            percent['text'] = "{}%".format(75)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[5] == alist[counter]:
                            step= "{}".format(i)
                            subprocess.run(["bedtools intersect -a " + str(no_gz) + " -b " + str(filename) + " -header > " + str(no_gz) + "_lipidseqls_" + str(filename_minusbed) + ".vcf"], shell=True)
                            progress["value"] = 90
                            percent['text'] = "{}%".format(90)
                            status["text"] = "{}".format(step) 
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[6] == alist[counter]:
                            step= "{}".format(i)
                            progress["value"] = 100
                            percent['text'] = "{}%".format(100)
                            status["text"] = "{}".format(step) 
                            subprocess.run(["grep -v 0/0 " + str(no_gz) + "_lipidseqls_" + str(filename_minusbed) + ".vcf > " + str(no_gz) + "_lipidseqls_" + str(filename_minusbed) + "zeroremoved.vcf"], shell=True)
                            subprocess.run(["mv " +  str(no_gz) + "_lipidseqls_" + str(filename_minusbed) + "zeroremoved.vcf ZeroZeroRemoved"], shell=True)
                            subprocess.run(["mv " + str(no_gz) + "_lipidseqls_" + str(filename_minusbed) + ".vcf Result"], shell=True)
                            subprocess.run(["mv " + str(no_gz) + " UnzippedCleanedVCFfiles"], shell=True) 
                            counter += 1
                            root.update()
                            time.sleep(0.5)

                    msgbox = messagebox.askquestion('Info', "Process completed! Would you like to do any additional steps?")
                    if msgbox == "no":
                        sys.exit()
                    else:
                        messagebox.showinfo("Return", "You will now return to the application screen")

                #############################################################################################################################################################################################################################

                else:
                    qmsgbox = messagebox.showinfo('Select a Directory', "Select your directory that contains the sample")
                    newpath = filedialog.askdirectory()
                    

                    for filein in os.listdir(newpath):
                        #print(filename)
                        os.rename(os.path.join(newpath,filein),os.path.join(newpath, filein.replace(' ', '_').lower())) 
                    bmsgbox = messagebox.showinfo("Select Bed file", "Please select the bed file you are working with")
                    filename = filedialog.askopenfilename(initialdir="." , filetypes =[('Bed Files', '*.bed')])
            
                    filename = filename.rsplit("/",1)[1]
                    filename_minusbed = filename.rsplit(".",1)[0]
                    vmsgbox = messagebox.showinfo("Select VCF file", "Please select the sample vcf file you are working with")
                    vcffile = filedialog.askopenfilename(initialdir=".")
                    vcffile = vcffile.rsplit("/",1)[1]
                    no_gz = vcffile.rsplit(".", 1)[0]
                    subprocess.run(["mkdir Result"], shell=True)
                    subprocess.run(["mkdir UnzippedCleanedVCFfiles"], shell=True)
                    print(no_gz)
                    counter = 0
                    alist = ["Cleaning " +str(filename), "Cleaned " +str(filename), "Preparing to clean " + str(vcffile),"Cleaning " + str(vcffile), "Cleaned " + str(vcffile), "Finding bed file instances in " + str(vcffile), "Found all instances in " + str(vcffile)]
                    for i in alist:
                        if alist[0] == alist[counter]:
                            step= "{}".format(i) 
                            subprocess.run(["sed 's/chr//g' " + str(filename)], shell=True)
                            progress["value"] = 15
                            percent['text'] = "{}%".format(15)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        felif alist[1] == alist[counter]:
                            step= "{}".format(i)
                            progress["value"] = 30
                            percent['text'] = "{}%".format(30)
                            status["text"] = "{}".format(step)
                            
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[2] == alist[counter]:
                            step= "{}".format(i)
                            subprocess.run(["Gzip -k -d " + str(vcffile)], shell=True)
                            progress["value"] = 45
                            percent['text'] = "{}%".format(45)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[3] == alist[counter]:
                            step= "{}".format(i)
                            subprocess.run(["sed -i -e 's/[<>,]//g' " + str(no_gz)], shell=True)
                            subprocess.run(["rm " + str(no_gz) + "-e"], shell=True)
                            progress["value"] = 60
                            percent['text'] = "{}%".format(60)
                            status["text"] = "{}".format(step)
                            
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[4] == alist[counter]:
                            step= "{}".format(i)
                            progress["value"] = 75
                            percent['text'] = "{}%".format(75)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[5] == alist[counter]:
                            step= "{}".format(i)
                            subprocess.run(["bedtools intersect -a " + str(no_gz) + " -b " + str(filename) + " -header > " + str(no_gz) + "_lipidseqls_" + str(filename_minusbed) + ".vcf"], shell=True)
                            progress["value"] = 90
                            percent['text'] = "{}%".format(90)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)
                        elif alist[6] == alist[counter]:
                            step= "{}".format(i)
                            progress["value"] = 100
                            subprocess.run(["mv " + str(no_gz) + "_lipidseqls_" + str(filename_minusbed) + ".vcf Result"], shell=True)
                            subprocess.run(["mv " + str(no_gz) + " UnzippedCleanedVCFfiles"], shell=True) 
                            percent['text'] = "{}%".format(100)
                            status["text"] = "{}".format(step)
                            counter += 1
                            root.update()
                            time.sleep(0.5)

                    msgbox = messagebox.askquestion('Info', "Process completed! Would you like to do any additional steps?")
                    if msgbox == "no":
                        sys.exit()
                    else:
                        messagebox.showinfo("Return", "You will now return to the application screen")
                


        except Exception as e:
            messagebox.showinfo('Info', "ERROR: {}".format(e))
            sys.exit()
 
#############################################################################################################################################################################################################################




  
               
   
class MyLabel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()
        self.lab = Label(self,textvariable = var, font=('Helvetica', 12), fg='red')  # use the same StringVar variable (var) as the OptionMenu. This allows changing the Label text instantaneously to the selected value of OptionMenu
        self.lab.pack(side=TOP)
        
a = MyOptMenu(root)
b = MyLabel(root)





# wid_frame = Frame(root)
# wid_frame.pack()
root.mainloop()