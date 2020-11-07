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


#This creates an app window
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
# initialization of a common StringVar for both OptionMenu and Label widgets
var = StringVar(root) 
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
        # give an initial value to the StringVar that will be displayed first on the OptionMenu
        var.set(opt[0])  
        # this is the optionMenu widget itself
        self.om = OptionMenu(self, var, *opt, command = self.toggle) 
        self.om.pack(side=TOP)
        self.submit = Button(self, text = "submit")
        # continuously trace the value of the selected items in the OptionMenu and update the var variable, using the function self.getValue
        var.trace('w', self.getValue)   
    
    def getValue(self, *args):
        # return the current value of OptionMenu 
        return(var.get())
        self.quit()  
    
    def toggle(self, item):
        #Packs the selected widget
        # Click this button for starting CAD267 process
        if item == 'CAD267_Analysis': 
            self.but = Button(self, text = "Click Me to start the analysis", 
            command = self.cad_analysis).pack()
        #Click this button for starting bedfile analysis 
        if item == 'Bed_file_Analysis':
            self.but = Button(self, text = "Click Me to start the analysis", 
            command = self.bed_analysis).pack()
    
    
    def step_count(self, x):
        step= "{}".format(x) 
        progress["value"] += 15
        percent['text'] = "{}%".format(progress["value"])
        status["text"] = "{}".format(step)
        root.update()

    def process_count(self, bed_path, bed_nopath, bed_minusbed, filename, path, vcf_nogz):
        alist = ["Cleaning " +str(bed_nopath), "Cleaned " +str(bed_nopath), "Preparing to clean " + str(filename),"Cleaning " + str(filename), "Cleaned " + str(filename), "Finding bed file instances in " + str(filename), "Found all instances in " + str(filename)]
        counter = 0
        for i in alist:
            if alist[0] == alist[counter]:
                counter += 1
                subprocess.run(["sed 's/chr//g' " + str(bed_path)], shell=True)
                self.step_count(i)
            elif alist[1] == alist[counter]:
                counter += 1
                self.step_count(i)
            elif alist[2] == alist[counter]:
                counter += 1
                subprocess.run(["Gzip -k -d "+ str(path) + "/" + str(filename)], shell=True)
                self.step_count(i)
            elif alist[3] == alist[counter]:
                counter += 1
                subprocess.run(["sed -i -e 's/[<>,]//g' " + str(path) + "/" +str(vcf_nogz)], shell=True)
                subprocess.run(["rm " + str(path) + "/" +str(vcf_nogz) + "-e"], shell=True)
                self.step_count(i)
            elif alist[4] == alist[counter]:
                counter += 1
                self.step_count(i)
            elif alist[5] == alist[counter]:
                counter += 1
                subprocess.run(["bedtools intersect -a " + str(path) + "/" +str(vcf_nogz) + " -b " + (bed_path) + " -header > " + str(path) + "/" +str(vcf_nogz) + "_lipidseqls_" + str(bed_minusbed) + ".vcf"], shell=True)
                self.step_count(i)
            elif alist[6] == alist[counter]:
                counter += 1
                subprocess.run(["mv " + str(path) + "/" +str(vcf_nogz) + " " +  str(path) + "/UnzippedCleanedVCFfiles"], shell=True) 
                step= "{}".format(i) 
                progress["value"] += 10
                percent['text'] = "{}%".format(progress["value"])
                status["text"] = "{}".format(step)
                root.update()

    def bed_analysis(self):
        try: 
            #The first message asks if you would like to run the bed file against all the vcf files in your directory 
            qmsgbox = messagebox.askquestion('Question', "Would you like to run the bed file against all the samples in this directory?") 
            #The second message asks if you would like to remove all 0/0 genotype instances in the result file
            zmsgbox = messagebox.askquestion("0/0 Instances", "Would you like to remove all 0/0 instances from the result file?")
            dmsgbox = messagebox.showinfo('Select a Directory', "Select your directory that contains the samples")
            path = filedialog.askdirectory()
            print(path)
            subprocess.run(["mkdir " + str(path) +"/Result"], shell=True)
            subprocess.run(["mkdir " + str(path) + "/UnzippedCleanedVCFfiles"], shell=True)
            bmsgbox = messagebox.showinfo("Select Bed file", "Please select the bed file you are working with")
            bedfilename = filedialog.askopenfilename(filetypes =[('Bed Files', '*.bed')])
            print(bedfilename)
            bedfilename_minuspath = bedfilename.rsplit("/",1)[1]
            print(bedfilename_minuspath)
            bedfilename_minusbed = bedfilename_minuspath.rsplit(".",1)[0]
            print(bedfilename_minusbed)
            print(qmsgbox)
            if qmsgbox == "yes":
                file_list = []
                for fn in os.listdir(path):
                    if not fn.startswith((".")) and fn.endswith(('.vcf.gz')):
                        file_list.append(fn)
                for filename in file_list:
                    no_gz = filename.rsplit(".", 1)[0]
                    self.process_count(bedfilename, bedfilename_minuspath, bedfilename_minusbed, filename, path, no_gz)
        
            else:
                vmsgbox = messagebox.showinfo("Select VCF file", "Please select the sample vcf file you are working with")
                filename = filedialog.askopenfilename(initialdir=path)
                filename = filename.rsplit("/",1)[1]
                no_gz = filename.rsplit(".", 1)[0]
                self.process_count(bedfilename, bedfilename_minuspath, bedfilename_minusbed, filename, path, no_gz)
            
            if zmsgbox == "yes":
                subprocess.run(["mkdir " + str(path) + "/ZeroZeroRemoved"], shell=True)
                subprocess.run(["grep -v 0/0 " + str(path) + "/" +str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf > " + str(path) + "/" + str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + "zeroremoved.vcf"], shell=True)
                subprocess.run(["mv " + str(path) + "/" +str(no_gz)  + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf " + str(path) + "/Result"], shell=True)
                subprocess.run(["mv " + str(path) + "/" +str(no_gz) + "_lipidseqls_" + str(bedfilename_minusbed) + "zeroremoved.vcf " +str(path) + "/ZeroZeroRemoved"], shell=True)
                 
            else:
                subprocess.run(["mv " + str(path) + "/" +str(no_gz)  + "_lipidseqls_" + str(bedfilename_minusbed) + ".vcf " + str(path) + "/Result"], shell=True)
            
            msgbox = messagebox.askquestion('Info', "Process completed! Would you like to do any additional steps?")
            if msgbox == "no":
                sys.exit()
            else:
                messagebox.showinfo("Return", "You will now return to the application screen")
        except Exception as e:
            messagebox.showinfo('Info', "ERROR: {}".format(e))
            sys.exit()
 
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