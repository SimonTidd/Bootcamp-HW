
# coding: utf-8

# In[44]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# In[2]:


purchase_data.head()


# In[3]:


unique_users=purchase_data['SN'].unique()


# In[4]:


Unique_user_count=len(unique_users)
print(Unique_user_count)


# In[5]:


print("Total Players: ", str(len(unique_users)))


# In[6]:



#Purchasing Analysis (Total)
#Run basic calculations to obtain number of unique items, average price, number of purchases,
#total revenue etc.
#Create a summary data frame to hold the results
#Optional: give the displayed data cleaner formatting
#Display the summary data frame


# In[7]:


unique_items=purchase_data['Item ID'].unique()
total_unique_items=str(len(unique_items))
print("Unique Items: ", total_unique_items)


# In[8]:


purchase_data.describe()


# In[9]:


item_price_list=purchase_data.groupby('Item ID').mean()
item_price_list = item_price_list.drop('Purchase ID', 1)
item_price_list = item_price_list.drop('Age', 1)


# In[10]:


print(item_price_list)


# In[11]:


average_price=item_price_list.mean()[0]
average_price


# In[12]:


number_of_purchases=len(purchase_data)
print("Total Purchases: ", number_of_purchases)


# In[13]:


revenue_column=purchase_data.drop('Age', 1)
revenue_column=revenue_column.drop('Purchase ID',1)
revenue_column=revenue_column.drop('SN',1)
revenue_column=revenue_column.drop('Gender',1)
revenue_column=revenue_column.drop('Item ID',1)
revenue_column=revenue_column.drop('Item Name',1)


# In[14]:


revenue_column


# In[15]:


total_revenue=revenue_column.sum()[0]
total_revenue


# In[16]:


print("Unique Items: ", str(len(unique_items)))
print("Total Purchases: ", number_of_purchases)
print("Average Price: ",average_price)
print("Total Revenue: ",total_revenue)


# In[17]:


purch_dict = {
    'Number of Unique Items':total_unique_items,
    'Average Price':average_price,
    'Number of Purchases':number_of_purchases,
    'Total Revenue':total_revenue}

Purchasing_Analaysis_df = pd.DataFrame(purch_dict, index=[0])
Purchasing_Analaysis_df


# In[18]:


gender_unique=purchase_data.groupby('SN').first()
gender_unique


# In[19]:


gender_counts=gender_unique.groupby(['Gender']).size().reset_index(name='counts')


# In[20]:


gender_counts


# In[21]:


gender_counts = gender_counts.rename(columns={'counts': 'Total Count'})


# In[22]:


gender_counts


# In[23]:


gender_counts['Percentage of Players'] = gender_counts['Total Count'] / Unique_user_count


# In[24]:


gender_counts=gender_counts.set_index('Gender')
gender_counts


# In[25]:


#Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender


# In[26]:


purchase_data.head()


# In[27]:


purch_count_gender=purchase_data.groupby('Gender').count()


# In[32]:


purch_count_gender=purch_count_gender.drop(columns=['SN', 'Age','Item ID','Item Name','Price'])


# In[62]:


purch_count_gender
purch_count_gender = purch_count_gender.rename(columns={'Purchase ID': 'Purchase Count'})
purch_count_gender


# In[38]:


purch_average_gender=purchase_data.groupby('Gender').mean()


# In[40]:


purch_average_gender=purch_average_gender.drop(columns=['Age','Item ID','Purchase ID'])


# In[41]:


purch_average_gender


# In[64]:


purch_average_gender = purch_average_gender.rename(columns={'Price': 'Average Purchase Price'})


# In[45]:


purchase_data


# In[51]:


purch_amnt_gender_and_Indiv=purchase_data.groupby(['Gender', 'SN']).sum()


# In[52]:


purch_amnt_gender_and_Indiv


# In[65]:


Sum_purch_amnt_gender=purch_amnt_gender_and_Indiv.groupby(['Gender']).sum()


# In[66]:


Sum_purch_amnt_gender


# In[67]:


Sum_purch_amnt_gender=Sum_purch_amnt_gender.drop(columns=['Age','Item ID','Purchase ID'])


# In[68]:


Sum_purch_amnt_gender


# In[69]:


Sum_purch_amnt_gender = Sum_purch_amnt_gender.rename(columns={'Price': 'Total Purchase Value'})


# In[70]:


Sum_purch_amnt_gender


# In[71]:


final_gender_table=purch_count_gender.join(purch_average_gender)
final_gender_table=final_gender_table.join(Sum_purch_amnt_gender)
final_gender_table


# In[85]:


gender_counts


# In[86]:


final_gender_table['new_counts'] = gender_counts['Total Count']


# In[88]:


final_gender_table


# In[89]:


final_gender_table['Avg Total Purchase per Person'] = final_gender_table['Total Purchase Value'] / final_gender_table['new_counts']


# In[90]:


final_gender_table


# In[91]:


final_gender_table=final_gender_table.drop(columns=['new_counts'])
final_gender_table


# In[130]:


bins = [0,9, 14, 19, 24, 29, 34,39,45]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34","35-39", "40+"]


# In[131]:


purchase_data["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=group_names)


# In[132]:


purchase_data


# In[133]:


age_unique=purchase_data.groupby('SN').first()
age_unique


# In[136]:


age_counts=age_unique.groupby(['Age Group']).size().reset_index(name='counts')


# In[137]:


age_counts = age_counts.rename(columns={'counts': 'Total Count'})


# In[138]:


age_counts


# In[139]:


age_counts['Percentage of Players'] = age_counts['Total Count'] / Unique_user_count


# In[140]:


age_counts=age_counts.set_index('Age Group')
age_counts


# In[109]:


purch_count_age=purchase_data.groupby('Age Group').count()


# In[110]:


purch_count_age


# In[111]:


purch_count_age=purch_count_age.drop(columns=['SN', 'Age','Item ID','Item Name','Price', 'Gender'])


# In[112]:


purch_count_age = purch_count_age.rename(columns={'Purchase ID': 'Purchase Count'})
purch_count_age


# In[113]:


purch_average_age=purchase_data.groupby('Age Group').mean()


# In[115]:


purch_average_age=purch_average_age.drop(columns=['Age','Item ID','Purchase ID'])


# In[116]:


purch_average_age


# In[141]:


purch_average_age = purch_average_age.rename(columns={'Price': 'Average Purchase Price'})


# In[142]:


purch_average_age


# In[143]:


purch_total_age=purchase_data.groupby('Age Group').sum()
purch_total_age


# In[144]:


purch_total_age=purch_total_age.drop(columns=['Age','Item ID','Purchase ID'])


# In[145]:


purch_total_age


# In[146]:


purch_total_age = purch_total_age.rename(columns={'Price': 'Total Purchase Value'})


# In[147]:


purch_total_age


# In[150]:


final_age_table=purch_count_age.join(purch_average_age)
final_age_table=final_age_table.join(purch_total_age)
final_age_table


# In[151]:


final_age_table['new_counts'] = age_counts['Total Count']


# In[152]:


final_age_table


# In[153]:


final_age_table['Avg Total Purchase per Person'] = final_age_table['Total Purchase Value'] / final_age_table['new_counts']


# In[154]:


final_age_table


# In[155]:


purchase_data.head()


# In[156]:


purch_total_indiv=purchase_data.groupby('SN').sum()
purch_total_indiv


# In[157]:


purch_total_indiv=purch_total_indiv.drop(columns=['Age','Item ID','Purchase ID'])
purch_total_indiv.head()


# In[164]:


#purch_total_indiv.sort_values(['col_1','col_2'])
purch_total_indiv=purch_total_indiv.sort_values(['Price'], ascending=False)
purch_total_indiv
purch_total_indiv['Spend_rank'] = purch_total_indiv['Price'].rank(ascending=0)
purch_total_indiv


# In[165]:


purchase_data.head()


# In[167]:


purch_total_indiv.reset_index()


# In[175]:


merge_table = pd.merge(purchase_data, purch_total_indiv, on="SN")
merge_table


# In[177]:


# Create variable with TRUE if age is greater than 50
top_five =merge_table['Spend_rank'] < 6


sub_set=merge_table[top_five]


# In[178]:


sub_set


# In[183]:


top_indiv_count=sub_set.groupby('SN').count()
top_indiv_count


# In[184]:


top_indiv_count=top_indiv_count.drop(columns=['Age','Item ID','Gender', 'Item Name', 'Price_x', 'Price_y', 'Spend_rank','Age Group'])
top_indiv_count.head()


# In[185]:


top_indiv_count = top_indiv_count.rename(columns={'Purchase ID': 'Purchase Count'})
top_indiv_count


# In[190]:


top_indiv_mean_value=sub_set.groupby('SN').mean()
top_indiv_mean_value


# In[191]:


top_indiv_mean_value=top_indiv_mean_value.drop(columns=['Age','Item ID','Purchase ID', 'Price_y', 'Spend_rank'])
top_indiv_mean_value.head()


# In[192]:


top_indiv_mean_value = top_indiv_mean_value.rename(columns={'Price_x': 'Average Purchase Price'})
top_indiv_mean_value


# In[193]:


top_indiv_spend=sub_set.groupby('SN').first()
top_indiv_spend


# In[195]:


top_indiv_spend=top_indiv_spend.drop(columns=['Age','Purchase ID','Gender','Item ID','Item Name','Age Group','Purchase ID', 'Price_x', 'Spend_rank'])
top_indiv_spend.head()


# In[196]:


top_indiv_spend = top_indiv_spend.rename(columns={'Price_y': 'Total Purchase Value'})
top_indiv_spend


# In[197]:


final_top_spend_table=top_indiv_count.join(top_indiv_mean_value)
final_top_spend_table=final_top_spend_table.join(top_indiv_spend)
final_top_spend_table


# In[198]:


final_top_spend_table=final_top_spend_table.sort_values(['Total Purchase Value'], ascending=False)
final_top_spend_table


# In[200]:


popular_subset=purchase_data.drop(columns=['SN','Age','Purchase ID','Gender','Age Group','Purchase ID'])
popular_subset.head()


# In[202]:


popular_subset_total_sold=popular_subset.groupby(['Item ID', 'Item Name']).count()
popular_subset_total_sold


# In[204]:


popular_subset_total_sold = popular_subset_total_sold.rename(columns={'Price': 'Purchase Count'})
popular_subset_total_sold


# In[205]:


popular_subset_item_price=popular_subset.groupby(['Item ID', 'Item Name']).first()
popular_subset_item_price


# In[206]:


popular_subset_item_price = popular_subset_item_price.rename(columns={'Price': 'Item Price'})
popular_subset_item_price


# In[207]:


popular_subset_item_toal=popular_subset.groupby(['Item ID', 'Item Name']).sum()
popular_subset_item_toal


# In[208]:


popular_subset_item_toal = popular_subset_item_toal.rename(columns={'Price': 'Total Purchase Value'})
popular_subset_item_toal


# In[209]:


final_popular_table=popular_subset_total_sold.join(popular_subset_item_price)
final_popular_table=final_popular_table.join(popular_subset_item_toal)

final_popular_table


# In[212]:


final_popular_table=final_popular_table.sort_values(['Purchase Count'], ascending=False)
final_popular_table


# In[213]:


final_popular_table.head()


# In[214]:


final_most_valuable_table=final_popular_table.sort_values(['Total Purchase Value'], ascending=False)
final_most_valuable_table


# In[215]:


final_most_valuable_table.head()

