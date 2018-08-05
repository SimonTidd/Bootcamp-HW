
# coding: utf-8

# In[ ]:


import os
import pandas as pd


# In[ ]:


election_df=pd.read_csv("election_data.csv")
election_df.head()


# In[ ]:


summary_series=election_df.groupby(by="Candidate").size()
print(summary_series)


# In[ ]:


summary_dataframe = summary_series.to_frame().reset_index()


# In[ ]:


summary_dataframe.columns = ['Candidate', 'Vote Total']
print(summary_dataframe)


# In[ ]:


vote_total=int(summary_dataframe['Vote Total'].sum())
print(vote_total)


# In[ ]:


summary_dataframe[vote_total]=vote_total


# In[ ]:


print(summary_dataframe)


# In[ ]:


summary_dataframe.columns = ['Candidate', 'Vote Total', 'Total Votes Cast']
print(summary_dataframe)


# In[ ]:


summary_dataframe['Percent of Vote'] = summary_dataframe.apply(lambda row: (row['Vote Total'] / row['Total Votes Cast'])/100, axis=1)


# In[ ]:


sorted_dataframe=summary_dataframe.sort_values(by=['Vote Total'],ascending=False)
sorted_dataframe.index = range(len(sorted_dataframe.index))
print(sorted_dataframe)


# In[ ]:


election_winner= sorted_dataframe.iloc[0,0]
print(election_winner)


# In[ ]:


sorted_dataframe.drop('Total Votes Cast', axis=1, inplace=True)


# In[ ]:


print("Election Results")
print("------------------------")
print("Total Votes: "+str(vote_total))
print("------------------------")
print(summary_dataframe)
print("------------------------")
print("Winner: " + election_winner)


# In[ ]:


file = open("output_file_for_python_homework_voting","w")
file.writelines("Election Results"+"\n")
file.writelines("------------------------"+"\n")
file.writelines("Total Votes: "+str(vote_total)+"\n")
file.writelines("------------------------"+"\n")
file.writelines(summary_dataframe)
file.writelines("------------------------"+"\n")
file.writelines("Winner: " + election_winner+"\n")
file.close()


# In[ ]:


# note - the next step would have been to create single text lines of the table rows and printed them with carriage returns
# that would also have allowed me to format the values and drop the row index but I ran pout of stream at 10:30 - appologies ;)

