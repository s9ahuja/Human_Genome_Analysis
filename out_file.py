#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import time
import numpy as np
import allel

#time measure start 
# start = time.time()

#get cad267 table 1 into dataframe
table_one_df = pd.read_excel("2020_05_05_CAD_PRS_267-converted.xlsx")
table_one_df.drop(["P-value", "Gene", "r2", "Genotyping","LD"], axis = 1, inplace = True)
table_one_df["Chromosome"] = table_one_df["Position"].str.split(":").str[0]
table_one_df["PositionNum"] = table_one_df["Position"].str.split(":").str[-1]
table_one_df = table_one_df.rename(columns= {"Effect\nAllele": "EffectAllele"})
print(table_one_df)

# get vcfsample file into df
# The following code just cleans up the vcf and creates a dataframe specific to out analysis needs
print("Reading in the vcf file")
callset = allel.read_vcf('220d9976-ebed-4ea1-8c09-46723ddac703 copy.vcf')
sorted(callset.keys())
print("Allele is doing its magic")
genotype = callset['calldata/GT']
print("Allele is doing its magic")
array = genotype.squeeze()
print("Allele is doing its magic")
VCF_sample_df= pd.DataFrame.from_records(array)
VCF_sample_df["Genotype"] = VCF_sample_df[0].astype(str) + "/" + VCF_sample_df[1].astype(str)
del VCF_sample_df[1]
del VCF_sample_df[0]
print("Creating Vcf df")
VCF_sample_df["VCFChrom"] = callset['variants/CHROM']
VCF_sample_df["VCFPos"] = callset['variants/POS']
VCF_sample_df["VCFid"] = callset['variants/ID']
VCF_sample_df["VCFRef"] = callset['variants/REF']
VCF_sample_df["VCFAlt"] = callset['variants/ALT'][:,0]
print("Created the VCf df")

# A new dataframe is created to make sure data type is the same as table 1 df
Clean_VCF_sample_df = VCF_sample_df.copy()
Clean_VCF_sample_df['VCFChrom'] = Clean_VCF_sample_df.VCFChrom.apply(str)
Clean_VCF_sample_df['VCFPos'] = Clean_VCF_sample_df.VCFPos.apply(str)
print(Clean_VCF_sample_df)
print("Vcf df cleaned")
# This part makes the chromosome number and position number data type to be the same as the data type for the vcf
table_one_df['Chromosome'] = table_one_df.Chromosome.apply(str)
table_one_df['PositionNum'] = table_one_df.PositionNum.apply(str)
print("table 1 df cleaned")
#this is when we merge the two dataframes and find out what is found on the vcf sample 
print("merging")
merged_df = table_one_df.merge(Clean_VCF_sample_df, left_on=['Chromosome', 'PositionNum'], right_on=['VCFChrom', 'VCFPos'], how='inner')
print(merged_df)
print("merging is done")
#Here is when we determine the 0,1,2 value based on the chromsome and position and if the nucleotide is hetrozygous or homozygous
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

#now we add the score 0,1,2 list to the merged_df
merged_df["Score"] = pd.Series(score)
print("Added score to the df")

#Now we check if the rs_ids match from both the table_1 df and the vcf_df
merged_df = merged_df[merged_df['rsID'] == merged_df['VCFid']].copy()
print("checked if rs_id matches")

#Now we multiply the score 0,1,2 with the weight so we can do weighted score analysis
merged_df["Score*Weight"] = merged_df["Score"] * merged_df["Weight"]
print(merged_df)

#Now we do the final analysis to calculated the weighed and unweighted score for the sample
print("starting analysis")

results = [["Observed_Score_Sum", merged_df["Score"].sum()], ["Maximum_Expected_Score_Sum", merged_df["Score*Weight"].sum()], ["Observed_Weighted_Sum", merged_df["Score*Weight"].sum()], ["Maximum_Expected_Weight", merged_df["Weight"].sum()]]
analysis_df = pd.DataFrame(results, columns = ["Analysis", "Results"])
print(analysis_df)
print("finished analysis")
#Percentile calculation comparison
# percentile_df = pd.read_excel("percentile.xlsx")
# search_percentile = percentile_df["FDR 267 score"]
# percentile_number = percentile_df["percentile"]
# percentile_index = search_percentile.searchsorted(value = analysis_df["Observed_Weighted_Sum"])
# percentile_final = percentile_number[percentile_index,:]
# print(percentile_final)
# #Now we put the output pf the analysis into the files that we expect 

# new_df.to_excel("220d9976-ebed-4ea1-8c09-46723ddac703 copy.xlsx")



#end of time measure
# end = time.time()
# print(end - start)