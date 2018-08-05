
# coding: utf-8

# In[21]:



import os
import csv


# In[22]:


csvpath = os.path.join("election_data.csv")


# In[23]:


# read in file
with open(csvpath, newline="") as csvfile:
    budget_data = csv.reader(csvfile, delimiter=",")
    file_as_list=list(election_data)


# In[4]:


# set accumulator variables
net_profit_or_loss=float(file_as_list[1][1])
prior_month_value=float(file_as_list[1][1])
current_month_value=0
month_to_month_change=0
greatest_pos_change=0
greatest_neg_change=0
greatest_month_of_pos_change=file_as_list[1][0]
greatest_month_of_neg_change=file_as_list[1][0]
accumulator_for_average_change=0
print(current_month_value)
print(greatest_month_of_pos_change)


# In[5]:


number_of_records=len(file_as_list)-1


# In[7]:


for i in range(number_of_records):
        current_month_value=float(file_as_list[i+1][1])
        net_profit_or_loss=net_profit_or_loss + current_month_value
        month_to_month_change=current_month_value - prior_month_value
        accumulator_for_average_change=accumulator_for_average_change+month_to_month_change
        prior_month_value=current_month_value
        if month_to_month_change > greatest_pos_change:
            greatest_pos_change = month_to_month_change
            greatest_month_of_pos_change=file_as_list[i+1][0]
        if month_to_month_change < greatest_neg_change:
            greatest_neg_change = month_to_month_change
            greatest_month_of_neg_change=file_as_list[i+1][0]


# In[8]:


average_month_to_month_change=accumulator_for_average_change/number_of_records
begin_to_end_change=float((file_as_list[number_of_records][1]))-float((file_as_list[1][1]))
print("Total Months: " + str(number_of_records))
print("Total Profit or Loss: $" + str(round(net_profit_or_loss)))
print("Average Month-to-Month Change: $" + str(round(average_month_to_month_change,0)))
print("Greatest Increase in Profits: " + str(greatest_month_of_pos_change) + " ($" + str(greatest_pos_change)+")")
print("Greatest Decrease in Profits: " + str(greatest_month_of_neg_change) + " ($" + str(greatest_neg_change)+")")


# In[20]:


file = open("output_file_for_python_homework_budget","w")
file.writelines("Total Months: " + str(number_of_records)+"\n")
file.writelines("Total Profit or Loss: $" + str(round(net_profit_or_loss))+"\n")
file.writelines("Average Month-to-Month Change: $" + str(round(average_month_to_month_change,0))+"\n")
file.writelines("Greatest Increase in Profits: " + str(greatest_month_of_pos_change) + " ($" + str(greatest_pos_change)+")"+"\n")
file.writelines("Greatest Decrease in Profits: " + str(greatest_month_of_neg_change) + " ($" + str(greatest_neg_change)+")"+"\n")
file.close()

