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
import pandas as pd 
import numpy as np
import allel

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
                
                print("step 1")
                counter += 1
                subprocess.run(["sed 's/chr//g' " + str(bed_path)], shell=True)
                self.step_count(i)
            elif alist[1] == alist[counter]:
                print("step 2")
                counter += 1
                self.step_count(i)
            elif alist[2] == alist[counter]:
                print("step 3")
                counter += 1
                subprocess.run(["Gzip -k -d "+ str(path) + "/" + str(filename)], shell=True)
                self.step_count(i)
            elif alist[3] == alist[counter]:
                print("step 4")
                counter += 1
                subprocess.run(["sed -i -e 's/[<>,]//g' " + str(path) + "/" +str(vcf_nogz)], shell=True)
                subprocess.run(["rm " + str(path) + "/" +str(vcf_nogz) + "-e"], shell=True)
                self.step_count(i)
            elif alist[4] == alist[counter]:
                print("step 5")
                counter += 1
                self.step_count(i)
            elif alist[5] == alist[counter]:
                print("step 6")
                counter += 1
                subprocess.run(["bedtools intersect -a " + str(path) + "/" +str(vcf_nogz) + " -b " + (bed_path) + " -header > " + str(path) + "/" +str(vcf_nogz) + "_lipidseqls_" + str(bed_minusbed) + ".vcf"], shell=True)
                self.step_count(i)
            elif alist[6] == alist[counter]:
                print("step 7")
                counter += 1
                subprocess.run(["mv " + str(path) + "/" +str(vcf_nogz) + " " +  str(path) + "/UnzippedCleanedVCFfiles"], shell=True) 
                step= "{}".format(i) 
                progress["value"] += 10
                percent['text'] = "{}%".format(progress["value"])
                status["text"] = "{}".format(step)
                root.update()


    def cad_step_count(self, x):
        step= "{}".format(x) 
        progress["value"] += 10
        percent['text'] = "{}%".format(progress["value"])
        status["text"] = "{}".format(step) 
        root.update()
        time.sleep(0.5)
    
    def cad_process(self, path, vcffile, vcf_nogz, snp_listpath,  snp_listnopath, percentfile, percentfile_nopath):
        alist = ["Created " + str(snp_listnopath) + " dataframe", "Creating " + str(vcffile) + " dataframe", "Created " + str(vcffile) + " dataframe", "Cleaning " + str(vcffile) + " dataframe", "Cleaning " + str(snp_listnopath) + " dataframe", "Merging the " + str(vcffile) + " dataframe and " + str(vcffile) + " dataframe", "Merging is done", "Determining what snps will get a 0,1 or 2", "Checking if rsids match", "Calculating Weights", "Starting Analysis", "Creating output files"]
        counter = 0
        #get cad267 table 1 into dataframe
        for i in alist:
            if alist[0] == alist[counter]:
                print("step 1")
                counter += 1
                table_one_df = pd.read_excel(str(snp_listpath))
                table_one_df.drop(["P-value", "Gene", "r2", "Genotyping","LD"], axis = 1, inplace = True)
                table_one_df["Chromosome"] = table_one_df["Position"].str.split(":").str[0]
                table_one_df["PositionNum"] = table_one_df["Position"].str.split(":").str[-1]
                table_one_df = table_one_df.rename(columns= {"Effect\nAllele": "EffectAllele"})
                print(table_one_df)
                self.cad_step_count(i) 
            elif alist[1] == alist[counter]:
                print("step 2")
                counter += 1
                callset = allel.read_vcf(str(path) + "/" + str(vcffile))
                sorted(callset.keys())
                genotype = callset['calldata/GT']
                array = genotype.squeeze()
                VCF_sample_df= pd.DataFrame.from_records(array)
                VCF_sample_df["Genotype"] = VCF_sample_df[0].astype(str) + "/" + VCF_sample_df[1].astype(str)
                del VCF_sample_df[1]
                del VCF_sample_df[0]
                VCF_sample_df["VCFChrom"] = callset['variants/CHROM']
                VCF_sample_df["VCFPos"] = callset['variants/POS']
                VCF_sample_df["VCFid"] = callset['variants/ID']
                VCF_sample_df["VCFRef"] = callset['variants/REF']
                VCF_sample_df["VCFAlt"] = callset['variants/ALT'][:,0]
                self.cad_step_count(i)   
            elif alist[2] == alist[counter]:
                counter += 1
                print("step 3")
                self.cad_step_count(i)
            elif alist[3] == alist[counter]: 
                counter += 1
                print("step 4")
                Clean_VCF_sample_df = VCF_sample_df.copy()
                Clean_VCF_sample_df['VCFChrom'] = Clean_VCF_sample_df.VCFChrom.apply(str)
                Clean_VCF_sample_df['VCFPos'] = Clean_VCF_sample_df.VCFPos.apply(str)
                self.cad_step_count(i)
            elif alist[4] == alist[counter]:
                counter += 1
                print("step 5")
                table_one_df['Chromosome'] = table_one_df.Chromosome.apply(str)
                table_one_df['PositionNum'] = table_one_df.PositionNum.apply(str)
                self.cad_step_count(i)
            elif alist[5] == alist[counter]:
                print("step 6")
                counter += 1
                merged_df = table_one_df.merge(Clean_VCF_sample_df, left_on=['Chromosome', 'PositionNum'], right_on=['VCFChrom', 'VCFPos'], how='inner')
                self.cad_step_count(i)
                print("step 7")
            elif alist[6] == alist[counter]:
                print("step 8")
                counter += 1
                self.cad_step_count(i)
            elif alist[7] == alist[counter]:
                print("step 9")
                counter += 1
                score = []
                for index, row in merged_df.iterrows():
                    print("finding 0,1,2")
                    if row["Genotype"] == "1/1" and row["VCFRef"] == row["EffectAllele"]:
                        score.append(0)
                    elif row["Genotype"] == "1/1" and row["VCFAlt"] == row["EffectAllele"]:
                        score.append(2)
                    elif row["Genotype"] == "0/0" and row["VCFRef"] == row["EffectAllele"]:
                        score.append(2)
                    elif row["Genotype"] == "0/0" and row["VCFAlt"] == row["EffectAllele"]:
                        score.append(0)
                    else:
                        score.append(1)
                merged_df["Score"] = pd.Series(score)
                self.cad_step_count(i)
            elif alist[8] == alist[counter]:
                print("step 10")
                counter += 1
                merged_df = merged_df[merged_df['rsID'] == merged_df['VCFid']].copy()
                print("checked if rs_id matches")
                self.cad_step_count(i)
            elif alist[9] == alist[counter]:
                counter += 1
                merged_df["Score*Weight"] = merged_df["Score"] * merged_df["Weight"]
                print(merged_df)
                self.cad_step_count(i)
            elif alist[10] == alist[counter]:
                counter += 1
                results = [["Observed_Score_Sum", merged_df["Score"].sum()], ["Maximum_Expected_Score_Sum", len(merged_df)*2], ["Observed_Weighted_Sum", merged_df["Score*Weight"].sum()], ["Maximum_Expected_Weight", merged_df["Weight"].sum()]]
                analysis_df = pd.DataFrame(results, columns = ["Analysis", "Results"])
                analysis_df.set_index('Analysis', inplace= True)
                print(analysis_df)
                print("finished analysis")
                self.cad_step_count(i)
            elif alist[11] == alist[counter]:
                counter += 1
                #Percentile calculation comparison
                print("starting percentile calculation")
                percentile_df = pd.read_excel(percentfile)
                print(percentile_df)
                print(analysis_df.loc["Observed_Weighted_Sum"])
                search_percentile = percentile_df["FDR 267 score"]
                percentile_number = percentile_df["percentile"]
                print(search_percentile)
                print(analysis_df.loc["Observed_Weighted_Sum", "Results"])
                percentile_index = min(range(len(search_percentile)), key=lambda x:abs(search_percentile[x]- analysis_df.loc["Observed_Weighted_Sum", "Results"]))
                print(percentile_index)
                percentile_final = percentile_number.iloc[percentile_index]
                print(percentile_final)
                print("finished percentile calculation")
                self.cad_step_count(i)
            elif alist[12] == alist[counter]:
                counter += 1
                no_exstension_name = filename.split(".")[0]
                #Output file for BGI
                print("creating the dataframe")
                bgi_output_dataframe = pd.DataFrame()
                bgi_output_dataframe["Sample_Name"] = callset['samples']
                bgi_output_dataframe["Weighted_Score"] = analysis_df.loc["Observed_Weighted_Sum", "Results"]
                bgi_output_dataframe["Percentile"] = percentile_final
                print(bgi_output_dataframe)
                print("creating the file")
                writer = pd.ExcelWriter(str(no_exstension_name) + '_BGI.xlsx', engine='xlsxwriter')
                bgi_output_dataframe.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                print("created the file")
                writer_two = pd.ExcelWriter(str(no_exstension_name) + '_Hegele.xlsx', engine='xlsxwriter')
                merged_df.to_excel(writer_two, sheet_name='Sheet1')
                analysis_df.to_excel(writer_two, sheet_name='Sheet2')
                writer_two.save()
                self.cad_step_count(i)
        msgbox = messagebox.askquestion('Info', "Process completed! Would you like to do any additional steps?")
        if msgbox == "no":
            sys.exit()
        else:
            messagebox.showinfo("Return", "You will now return to the application screen")

   
    def cad_analysis(self):
        try:
            qmsgbox = messagebox.askquestion('Question', "Would you like to find snps on all samples in the directory?") #qmsgbox asks if you want to compare the bed file to all the vcf samples in the directory or would you like to select a specific one
            if qmsgbox == "yes":
                qmsgbox = messagebox.showinfo('Select a Directory', "Select your directory that contains the samples")
                path = filedialog.askdirectory()
                pmsgbox = messagebox.showinfo("Select Percentile Distribution file", "Please select the excel file that contains the percentile distribution")
                percent_file = filedialog.askopenfilename(initialdir=path , filetypes =[('Excel Files', '*.xlsx')])
                npathpercent_file = percent_file.rsplit("/",1)[1]
                print(npathpercent_file)
                emsgbox = messagebox.showinfo("Select Excel file", "Please select the excel file that contains the 267 snps")
                excelfilename = filedialog.askopenfilename(initialdir=path , filetypes =[('Excel Files', '*.xlsx')])
                npath = excelfilename.rsplit("/",1)[1]
                print(npath)
                file_list = []
                for fn in os.listdir(path):
                    if fn.endswith(('.vcf.gz')) or fn.endswith(('.vcf')):
                        file_list.append(fn)
                subprocess.run(["mkdir " + str(path) + "/HegeleResult"], shell=True)
                subprocess.run(["mkdir " + str(path) + "/BGIResult"], shell=True)
                for filename in file_list:
                    no_gz = filename.rsplit(".", 1)[0]
                    print("done")
                    self.cad_process(path, filename, no_gz, excelfilename, npath, percent_file, npathpercent_file)
                print("------ going to other function --------")
              
        except Exception as e:
            messagebox.showinfo('Info', "ERROR: {}".format(e))
            sys.exit()

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