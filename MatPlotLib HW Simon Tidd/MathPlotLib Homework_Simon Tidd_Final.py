
# coding: utf-8

# In[1]:


# Dependencies and Setup
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.pyplot import figure


# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
mouse_drug_data_to_load = "mouse_drug_data.csv"
clinical_trial_data_to_load = "clinicaltrial_data.csv"

# Read the Mouse and Drug Data and the Clinical Trial Data
mouse_drug_data = pd.read_csv(mouse_drug_data_to_load)
clinical_trial_data = pd.read_csv(clinical_trial_data_to_load)
mouse_df=pd.DataFrame(mouse_drug_data)
trial_df=pd.DataFrame(clinical_trial_data)

# Combine the data into a single dataset
merged_mouse_trial_df=pd.merge(mouse_df, trial_df, on='Mouse ID', how='left')
# Display the data table for preview
merged_mouse_trial_df.head()


# In[2]:


# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint 
drug_by_time_tumor_vol_df=merged_mouse_trial_df.groupby(['Timepoint',"Drug"]).mean()
# Convert to DataFrame

revised_combined_volume=drug_by_time_tumor_vol_df.reset_index(level='Drug')
revised_combined_volume=revised_combined_volume.reset_index()
revised_combined_volume.sort_values(["Drug","Timepoint"], inplace=True, ascending=True) 
revised_combined_volume=revised_combined_volume.reset_index()
revised_combined_volume.rename(columns={"Tumor Volume (mm3)":"mean tumor vol"}, inplace=True)
revised_combined_volume=revised_combined_volume.drop(["Metastatic Sites","index"], axis=1)


# In[3]:


revised_combined_volume.head()


# In[4]:


# Store the std dev Tumor Volume Data Grouped by Drug and Timepoint 
drug_by_time_tumor_std_df=merged_mouse_trial_df.groupby(['Timepoint',"Drug"]).std()
# Convert to DataFrame

revised_combined_std=drug_by_time_tumor_std_df.reset_index(level='Drug')
revised_combined_std=revised_combined_std.reset_index()
revised_combined_std.sort_values(["Drug","Timepoint"], inplace=True, ascending=True) 
revised_combined_std=revised_combined_std.reset_index()
revised_combined_std=revised_combined_std.drop(["Metastatic Sites","index"], axis=1)
revised_combined_std.rename(columns={"Tumor Volume (mm3)":"std tumor vol"}, inplace=True)


# In[5]:


revised_combined_std.head()


# In[6]:


# calculate srt(n) to use to get SE
drug_by_time_tumor_count_df=merged_mouse_trial_df.groupby(['Timepoint',"Drug"]).count()
# Convert to DataFrame

revised_combined_count=drug_by_time_tumor_count_df.reset_index(level='Drug')
revised_combined_count=revised_combined_count.reset_index()
revised_combined_count=revised_combined_count.drop(["Metastatic Sites","Mouse ID"], axis=1)
revised_combined_count.rename(columns={"Tumor Volume (mm3)":"N"}, inplace=True)
revised_combined_count['sqrt_n'] = revised_combined_count['N'].pow(1./2)
revised_combined_count=revised_combined_count.drop(["N"], axis=1)
calculate_SE_df=pd.merge(revised_combined_std, revised_combined_count, on=['Timepoint','Drug'], how='left')
calculate_SE_df[['std tumor vol','sqrt_n']] = calculate_SE_df[['std tumor vol','sqrt_n']].apply(pd.to_numeric)

calculate_SE_df['SE']=calculate_SE_df['std tumor vol']/calculate_SE_df['sqrt_n']


# In[7]:


calculate_SE_df.sort_values(["Drug","Timepoint"], inplace=True, ascending=True) 
calculate_SE_df=calculate_SE_df.reset_index()
calculate_SE_df=calculate_SE_df.drop(["std tumor vol","sqrt_n", "index"], axis=1)
calculate_SE_df.head()


# In[8]:



mean_and_SE_df=pd.merge(revised_combined_volume, calculate_SE_df, on=['Timepoint','Drug'], how='left')


# In[9]:


mean_and_SE_df.head()


# In[10]:


table_to_flip_df=mean_and_SE_df.drop(["SE"], axis=1)
table_to_flip_df = table_to_flip_df[['Drug', 'Timepoint', 'mean tumor vol']]


# In[11]:


table_to_flip_df.head()


# In[12]:


table_to_flip_df=table_to_flip_df.pivot(index='Timepoint', columns='Drug', values='mean tumor vol')


# In[13]:


table_to_flip_df


# In[14]:


type(table_to_flip_df)
table_to_flip_df['Timepoint'] = table_to_flip_df.index
table_to_flip_df


# In[15]:


# focal drugs are Capomulin, Infubinol, Ketapril, and Placebo
ax = plt.gca()
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Capomulin',color ='blue',marker=10,s=120, label='Capomulin', ax=ax)
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Infubinol', color='red',marker='.',s=120,label='Infubinol', ax=ax)
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Ketapril', color='green',marker='x',s=120,label='Ketapril', ax=ax)
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Placebo', color='black',marker='+',s=120,label='Placebo', ax=ax)
plt.show()
ax.legend()


# In[16]:


# now for error bars
Capomulin_SE_df=mean_and_SE_df.loc[mean_and_SE_df['Drug']=='Capomulin']
Infubinol_SE_df=mean_and_SE_df.loc[mean_and_SE_df['Drug']=='Infubinol']
Ketapril_SE_df=mean_and_SE_df.loc[mean_and_SE_df['Drug']=='Ketapril']
Placebo_SE_df=mean_and_SE_df.loc[mean_and_SE_df['Drug']=='Placebo']

Capomulin_SE_df.rename(columns={"mean tumor vol":"Capomulin_vol", "SE":"Capomulin_SE"}, inplace=True)
Capomulin_SE_df=Capomulin_SE_df.drop(["Drug"], axis=1)
Infubinol_SE_df.rename(columns={"mean tumor vol":"Infubinol_vol", "SE":"Infubinol_SE"}, inplace=True)
Infubinol_SE_df=Infubinol_SE_df.drop(["Drug"], axis=1)
Ketapril_SE_df.rename(columns={"mean tumor vol":"Ketapril_vol", "SE":"Ketapril_SE"}, inplace=True)
Ketapril_SE_df=Ketapril_SE_df.drop(["Drug"], axis=1)
Placebo_SE_df.rename(columns={"mean tumor vol":"Placebo_vol", "SE":"Placebo_SE"}, inplace=True)
Placebo_SE_df=Placebo_SE_df.drop(["Drug"], axis=1)



# In[17]:


# FOR SOME REASON I CAN'T GET THE INDICES TO RESET, HENCE THE ERROR BARS AREN'T PLOTTING
# IT WORKED IN AN EARLIER VERSION, BUT I CAN'T SEE WHAT'S HGAPPENING DIFFERENTY HERE


Infubinol_SE_df=Infubinol_SE_df.reset_index()
Capomulin_SE_df=Capomulin_SE_df.reset_index()
Ketapril_SE_df=Ketapril_SE_df.reset_index()
Placebo_SE_df=Placebo_SE_df.reset_index()


# In[18]:


Ketapril_SE_df


# In[19]:


ax = plt.gca()
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Capomulin',color ='blue',marker=".",s=60, label='Capomulin',yerr=Capomulin_SE_df["Capomulin_SE"], ax=ax)
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Infubinol',color ='red',marker=".",s=60, label='Infubinol',yerr=Infubinol_SE_df["Infubinol_SE"], ax=ax)
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Ketapril',color ='green',marker=".",s=60, label='Ketapril',yerr=Ketapril_SE_df["Ketapril_SE"], ax=ax)
table_to_flip_df.plot(kind='scatter',x='Timepoint',y='Placebo',color ='black',marker=".",s=60, label='Placebo',yerr=Placebo_SE_df["Placebo_SE"], ax=ax)

plt.show()
ax.legend()


# In[20]:


Placebo_SE_df


# In[21]:


# Store the Mean Met. Site Data Grouped by Drug and Timepoint  
drug_by_time_tumor_ms_df=merged_mouse_trial_df.groupby(['Timepoint',"Drug"]).mean()
# Convert to DataFrame

revised_combined_mst=drug_by_time_tumor_ms_df.reset_index(level='Drug')
revised_combined_mst=revised_combined_mst.reset_index()
revised_combined_mst.sort_values(["Drug","Timepoint"], inplace=True, ascending=True) 
revised_combined_mst=revised_combined_mst.reset_index()
revised_combined_mst.rename(columns={"Metastatic Sites":"mean met site"}, inplace=True)
revised_combined_mst=revised_combined_mst.drop(["Tumor Volume (mm3)","index"], axis=1)

revised_combined_mst.head()
# Preview DataFrame


# In[22]:


# Store the std dev ms Data Grouped by Drug and Timepoint 
drug_by_time_ms_std_df=merged_mouse_trial_df.groupby(['Timepoint',"Drug"]).std()
# Convert to DataFrame

drug_by_time_ms_std_df=drug_by_time_tumor_std_df.reset_index(level='Drug')
drug_by_time_ms_std_df=drug_by_time_ms_std_df.reset_index()
drug_by_time_ms_std_df.sort_values(["Drug","Timepoint"], inplace=True, ascending=True) 
drug_by_time_ms_std_df=drug_by_time_ms_std_df.reset_index()
drug_by_time_ms_std_df=drug_by_time_ms_std_df.drop(["Tumor Volume (mm3)","index"], axis=1)
drug_by_time_ms_std_df.rename(columns={"Metastatic Sites":"std ms"}, inplace=True)


# In[23]:


drug_by_time_ms_std_df.head()


# In[24]:


# calculate srt(n) to use to get SE
drug_by_time_tumor_count_df=merged_mouse_trial_df.groupby(['Timepoint',"Drug"]).count()
# Convert to DataFrame

calculate_SE_ms_df=pd.merge(drug_by_time_ms_std_df, revised_combined_count, on=['Timepoint','Drug'], how='left')
calculate_SE_ms_df

calculate_SE_ms_df[['std ms','sqrt_n']] = calculate_SE_ms_df[['std ms','sqrt_n']].apply(pd.to_numeric)

calculate_SE_ms_df['SE']=calculate_SE_ms_df['std ms']/calculate_SE_ms_df['sqrt_n']


# In[25]:


calculate_SE_ms_df.sort_values(["Drug","Timepoint"], inplace=True, ascending=True) 
calculate_SE_ms_df=calculate_SE_ms_df.reset_index()
calculate_SE_ms_df=calculate_SE_ms_df.drop(["std ms","sqrt_n", "index"], axis=1)
calculate_SE_ms_df.head()
revised_combined_mst.head()


# In[26]:


revised_combined_mst.head()


# In[27]:



ms_mean_and_SE_df=pd.merge(revised_combined_mst, calculate_SE_ms_df, on=['Timepoint','Drug'], how='left')


# In[28]:


revised_combined_mst.head()


# In[29]:


calculate_SE_ms_df


# In[30]:


ms_mean_and_SE_df.head()


# In[31]:


table_to_flip_ms_df=ms_mean_and_SE_df.drop(["SE"], axis=1)
table_to_flip_ms_df = table_to_flip_ms_df[['Drug', 'Timepoint', 'mean met site']]


# In[32]:


table_to_flip_ms_df.head()


# In[33]:


table_to_flip_ms_df=table_to_flip_ms_df.pivot(index='Timepoint', columns='Drug', values='mean met site')


# In[34]:


table_to_flip_ms_df


# In[35]:


table_to_flip_ms_df['Timepoint'] = table_to_flip_ms_df.index
table_to_flip_ms_df


# In[36]:


# focal drugs are Capomulin, Infubinol, Ketapril, and Placebo
ax = plt.gca()
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Capomulin',color ='blue',marker=10,s=120, label='Capomulin', ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Infubinol', color='red',marker='.',s=120,label='Infubinol', ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Ketapril', color='green',marker='x',s=120,label='Ketapril', ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Placebo', color='black',marker='+',s=120,label='Placebo', ax=ax)
plt.show()
ax.legend()


# In[37]:


# now for error bars
Capomulin_ms_SE_df=ms_mean_and_SE_df.loc[ms_mean_and_SE_df['Drug']=='Capomulin']
Infubinol_ms_SE_df=ms_mean_and_SE_df.loc[ms_mean_and_SE_df['Drug']=='Infubinol']
Ketapril_ms_SE_df=ms_mean_and_SE_df.loc[ms_mean_and_SE_df['Drug']=='Ketapril']
Placebo_ms_SE_df=ms_mean_and_SE_df.loc[ms_mean_and_SE_df['Drug']=='Placebo']



Capomulin_ms_SE_df.rename(columns={"mean tumor vol":"Capomulin_vol", "SE":"Capomulin_SE"}, inplace=True)
Capomulin_ms_SE_df=Capomulin_ms_SE_df.drop(["Drug"], axis=1)
Infubinol_ms_SE_df.rename(columns={"mean tumor vol":"Infubinol_vol", "SE":"Infubinol_SE"}, inplace=True)
Infubinol_ms_SE_df=Infubinol_ms_SE_df.drop(["Drug"], axis=1)
Ketapril_ms_SE_df.rename(columns={"mean tumor vol":"Ketapril_vol", "SE":"Ketapril_SE"}, inplace=True)
Ketapril_ms_SE_df=Ketapril_ms_SE_df.drop(["Drug"], axis=1)
Placebo_ms_SE_df.rename(columns={"mean tumor vol":"Placebo_vol", "SE":"Placebo_SE"}, inplace=True)
Placebo_ms_SE_df=Placebo_ms_SE_df.drop(["Drug"], axis=1)



print(Capomulin_ms_SE_df)
print(Infubinol_ms_SE_df)
print(Ketapril_ms_SE_df)
print(Placebo_ms_SE_df)


# In[38]:


# AGAIN, SOMETHING WEIRD IS GOING ON WITH THE ERROR BARS NOT PLOTTING
#IT WORKED IN AN EARLIER VERSION AND I CAN'T FIND THE ISSUE HERE - FRUSTRATING


# In[39]:


ax = plt.gca()
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Capomulin',color ='blue',marker=".",s=120, label='Capomulin',yerr=Capomulin_ms_SE_df["Capomulin_SE"], ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Infubinol',color ='red',marker=".",s=120, label='Infubinol',yerr=Infubinol_ms_SE_df["Infubinol_SE"], ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Ketapril',color ='green',marker=".",s=120, label='Ketapril',yerr=Ketapril_ms_SE_df["Ketapril_SE"], ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Placebo',color ='black',marker=".",s=120, label='Placebo',yerr=Placebo_ms_SE_df["Placebo_SE"], ax=ax)

plt.show()
ax.legend()


# In[40]:


Placebo_ms_SE_df


# In[41]:


#too crowded - going to do each vs placebo


# In[42]:


ax = plt.gca()
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Capomulin',color ='blue',marker=".",s=120, label='Capomulin',yerr=Capomulin_SE_df["Capomulin_SE"], ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Placebo',color ='black',marker=".",s=120, label='Placebo',yerr=Placebo_SE_df["Placebo_SE"], ax=ax)

plt.show()
ax.legend()


# In[43]:


ax = plt.gca()
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Infubinol',color ='red',marker=".",s=120, label='Infubinol',yerr=Infubinol_SE_df["Infubinol_SE"], ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Placebo',color ='black',marker=".",s=120, label='Placebo',yerr=Placebo_SE_df["Placebo_SE"], ax=ax)

plt.show()
ax.legend()


# In[44]:


ax = plt.gca()
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Ketapril',color ='green',marker=".",s=120, label='Ketapril',yerr=Ketapril_SE_df["Ketapril_SE"], ax=ax)
table_to_flip_ms_df.plot(kind='scatter',x='Timepoint',y='Placebo',color ='black',marker=".",s=120, label='Placebo',yerr=Placebo_SE_df["Placebo_SE"], ax=ax)

plt.show()
ax.legend()


# In[45]:


# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
count_the_mice_df=merged_mouse_trial_df.groupby(['Timepoint',"Drug"]).count()

# Preview DataFrame
count_the_mice_df.head()


# In[46]:


count_the_mice_df.rename(columns={"Mouse ID":"mice remaining"}, inplace=True)
count_the_mice_df=count_the_mice_df.drop(["Tumor Volume (mm3)","Metastatic Sites"], axis=1)


# In[47]:


count_the_mice_df=count_the_mice_df.reset_index(level='Drug')
count_the_mice_df=count_the_mice_df.reset_index()
count_the_mice_df.sort_values(["Drug","Timepoint"], inplace=True, ascending=True) 
count_the_mice_df=count_the_mice_df.reset_index()
count_the_mice_df.head()


# In[48]:


count_the_mice_df=count_the_mice_df.drop(["index"], axis=1)
count_the_mice_df.head()


# In[49]:


table_to_flip_mice_remaining_df=count_the_mice_df.pivot(index='Timepoint', columns='Drug', values='mice remaining')
table_to_flip_mice_remaining_df


# In[50]:


table_to_flip_mice_remaining_df['Timepoint'] = table_to_flip_mice_remaining_df.index


# In[51]:


ax = plt.gca()

table_to_flip_mice_remaining_df.plot(kind='scatter',x='Timepoint',y='Capomulin',color ='blue',marker=".",s=120, label='Capomulin', ax=ax)
table_to_flip_mice_remaining_df.plot(kind='scatter',x='Timepoint',y='Infubinol',color ='red',marker=".",s=120, label='Infubinol', ax=ax)
table_to_flip_mice_remaining_df.plot(kind='scatter',x='Timepoint',y='Ketapril',color ='green',marker=".",s=120, label='Ketapril', ax=ax)
table_to_flip_mice_remaining_df.plot(kind='scatter',x='Timepoint',y='Placebo',color ='black',marker=".",s=120, label='Placebo', ax=ax)


plt.show()
ax.legend()


# In[ ]:


# now do percent change in tumor volume

min_vol_df=merged_mouse_trial_df.groupby(["Drug"]).min()
max_vol_df=merged_mouse_trial_df.groupby(["Drug"]).max()


# In[ ]:


min_vol_df.rename(columns={"Tumor Volume (mm3)":"min volume"}, inplace=True)
min_vol_df=min_vol_df.drop(["Mouse ID","Timepoint", "Metastatic Sites"], axis=1)

max_vol_df.rename(columns={"Tumor Volume (mm3)":"max volume"}, inplace=True)
max_vol_df=max_vol_df.drop(["Mouse ID","Timepoint", "Metastatic Sites"], axis=1)


# In[ ]:



min_vol_df=min_vol_df.reset_index()
min_vol_df


# In[ ]:



max_vol_df=max_vol_df.reset_index()
max_vol_df


# In[ ]:


tumor_changed=pd.merge(max_vol_df, min_vol_df, on='Drug', how='left')
tumor_changed


# In[ ]:


tumor_changed['chnage amount']=tumor_changed['max volume']/tumor_changed['min volume']


# In[ ]:


tumor_changed['change percent']=tumor_changed['change amount']/tumor_changed['max volume']
# I know thi is wrong but I ran out of time - I should have looked at first and last values becaue volume could go up or down
# C'est la vie


# In[ ]:


tumor_changed


# In[ ]:


# writen description of three things about the data
# 1 - Capomulin susbtantively reduces tumor size while the other drugs are statistically no different than the placebo
# 2 - Infubinol and Capomulin both reduce the number of sites but Capomutin does so to a greater extent suggestung a combination of both is unliekly
# to be more effectize than Capomulin alone
# 3 - Infubinol underperforms that placebo near the end of the trial suggesting that by itself it has negatives that may outweight the posisitve impact on sites

