
# coding: utf-8

# In[5]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "schools_complete.csv"
student_data_to_load = "students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# In[6]:


school_data_complete.head()


# In[7]:


#Calculate the total number of schools
#Calculate the total number of students
#Calculate the total budget
#Calculate the average math score
#Calculate the average reading score
#Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
#Calculate the percentage of students with a passing math score (70 or greater)
#Calculate the percentage of students with a passing reading score (70 or greater)
#Create a dataframe to hold the above results
#Optional: give the displayed data cleaner formatting


# In[8]:


unique_schools=school_data_complete['School ID'].unique()
num_unique_schools=len(unique_schools)
num_unique_schools


# In[9]:


unique_students=school_data_complete['Student ID'].unique()
num_unique_students=len(unique_students)
num_unique_students


# In[10]:


budget_by_school=school_data_complete.groupby(['School ID']).first()
budget_by_school


# In[29]:


budget_column=budget_by_school.drop(columns=['Student ID', 'student_name','gender','grade','school_name','reading_score','math_score','type','size'])

total_budget=budget_column.sum()[0]
total_budget


# In[30]:


math_score_column=school_data_complete.drop(columns=['budget','Student ID', 'student_name','gender','grade','school_name','reading_score','type','size'])
read_score_column=school_data_complete.drop(columns=['budget','Student ID', 'student_name','gender','grade','school_name','math_score','type','size'])
avg_math_score=math_score_column.mean()[0]
avg_read_score=read_score_column.mean()[0]
print("Average Math Score: ",avg_math_score)
print("Average Reading Score: ",avg_read_score)


# In[31]:


school_data_complete['Math and Read Avg'] = (school_data_complete['math_score'] + school_data_complete['reading_score']) / 2


# In[32]:


school_data_complete.head()


# In[33]:


math_and_read_avg_column=school_data_complete.drop(columns=['Student ID', 'student_name','gender','grade','School ID','school_name','reading_score','math_score','type','size', 'budget'])
math_and_read_avg_column.head()
average_math_read_combined=math_and_read_avg_column.mean()[0]
average_math_read_combined


# In[34]:


math_and_read_avg_column.head()


# In[35]:


math_and_read_avg_column_w_stu_id=school_data_complete.drop(columns=['student_name','gender','grade','School ID','school_name','reading_score','math_score','type','size', 'budget'])
math_and_read_pass = math_and_read_avg_column_w_stu_id['Math and Read Avg'] > 69
Math_and_read_pass_sub_set=math_and_read_avg_column_w_stu_id[math_and_read_pass]
Math_and_read_pass_sub_set.head()


# In[36]:


unique_math_and_read_pass_students=Math_and_read_pass_sub_set['Student ID'].unique()
num_unique_M_and_read_pass_students=len(unique_math_and_read_pass_students)
num_unique_M_and_read_pass_students


# In[37]:


school_data_complete.head()


# In[38]:


math_pass = school_data_complete['math_score'] > 69
Math_pass_sub_set=school_data_complete[math_pass]
Math_pass_sub_set.head()


# In[39]:


read_pass = school_data_complete['reading_score'] > 69
Read_pass_sub_set=school_data_complete[read_pass]
Read_pass_sub_set.head()


# In[40]:


math_passers=Math_pass_sub_set['Student ID'].unique()
num_math_passers=len(math_passers)
num_math_passers


# In[41]:


read_passers=Read_pass_sub_set['Student ID'].unique()
num_read_passers=len(read_passers)
num_read_passers


# In[42]:


pcnt_math_passers=num_math_passers/num_unique_students
pcnt_read_passers=num_read_passers/num_unique_students
pcnt_math_and_read_passers=num_unique_M_and_read_pass_students/num_unique_students
print("Percent Reading Passers: ", pcnt_read_passers)
print("Percent Math Passers: ", pcnt_math_passers)
print("Percent Overall Passing Rate: ", pcnt_math_and_read_passers)


# In[44]:


summary_dict = {
    'Total Schools':num_unique_schools,
    'Total Students':num_unique_students,
    'Total Budget':total_budget,
    'Average Math Score':avg_math_score,
    'Average Reading Score': avg_read_score,
    '% Passing Math': pcnt_math_passers,
    '% Passing Reading': pcnt_read_passers,
    '% Overall Passing Rate': pcnt_math_and_read_passers
}

summary_school_and_students_df = pd.DataFrame(summary_dict, index=[0])
summary_school_and_students_df


# In[ ]:


#Create an overview table that summarizes key metrics about each school, including:
#School Name
#School Type
#Total Students
#Total School Budget
#Per Student Budget
#Average Math Score
#Average Reading Score
#% Passing Math
#% Passing Reading
#Overall Passing Rate (Average of the above two)
#Create a dataframe to hold the above results


# In[45]:


school_data_complete.head()


# In[69]:


sch_type=school_data_complete.groupby('school_name').first()
sch_type=sch_type.drop(columns=['gender','student_name','grade','reading_score','math_score','size','budget','Student ID','Math and Read Avg','School ID'])
sch_type.head()


# In[67]:


budget_size_math_and_read_score=school_data_complete.groupby('school_name').mean()
avg_math_and_read_score=avg_math_and_read_score.drop(columns=['Student ID','Math and Read Avg','School ID'])
avg_math_and_read_score.head()


# In[70]:


final_sch_descr_table=sch_type.join(avg_math_and_read_score)
final_sch_descr_table


# In[81]:


num_pas_math_by_sch=Math_pass_sub_set.groupby(['school_name']).count()
num_pas_read_by_sch=Read_pass_sub_set.groupby(['school_name']).count()


# In[82]:


num_pas_math_by_sch=num_pas_math_by_sch.drop(columns=['gender','student_name','grade','reading_score','math_score','size','budget','Student ID','Math and Read Avg','School ID'])
num_pas_math_by_sch = num_pas_math_by_sch.rename(columns={'type': 'Num Math Passers'})
num_pas_math_by_sch


# In[83]:


num_pas_read_by_sch=num_pas_read_by_sch.drop(columns=['gender','student_name','grade','reading_score','math_score','size','budget','Student ID','Math and Read Avg','School ID'])
num_pas_read_by_sch = num_pas_read_by_sch.rename(columns={'type': 'Num Read Passers'})
num_pas_read_by_sch


# In[85]:


final_sch_descr_table=final_sch_descr_table.join(num_pas_math_by_sch)
final_sch_descr_table=final_sch_descr_table.join(num_pas_read_by_sch)


# In[86]:


final_sch_descr_table


# In[89]:


final_sch_descr_table['per_math_passers'] = final_sch_descr_table['Num Math Passers'] / final_sch_descr_table['size']
final_sch_descr_table['per_read_passers'] = final_sch_descr_table['Num Read Passers'] / final_sch_descr_table['size']


# In[90]:


final_sch_descr_table


# In[91]:


school_data_complete.head()
#school_data_complete['Math and Read Avg'] = (school_data_complete['math_score'] + school_data_complete['reading_score']) / 2


# In[92]:


math_and_read_pass = school_data_complete['Math and Read Avg'] > 69
Math_and_read_pass_sub_set=school_data_complete[math_and_read_pass]
Math_and_read_pass_sub_set.head()


# In[97]:


math_read_passer_counts=Math_and_read_pass_sub_set.groupby('school_name').count()
math_read_passer_counts=math_read_passer_counts.drop(columns=['type','gender','student_name','grade','reading_score','math_score','size','budget','Math and Read Avg','School ID'])
math_read_passer_counts = math_read_passer_counts.rename(columns={'Student ID': 'Num Read and Math Passers'})
math_read_passer_counts.head()


# In[98]:


final_sch_descr_table=final_sch_descr_table.join(math_read_passer_counts)
final_sch_descr_table


# In[99]:


final_sch_descr_table['per_math_and_read_passers'] = final_sch_descr_table['Num Read and Math Passers'] / final_sch_descr_table['size']
final_sch_descr_table


# In[104]:


final_sch_descr_table = final_sch_descr_table.rename(columns={'type': 'School Type','Size':'Total Students',
                                                              'budget':'Total School Budget',
                                                             'math_score':'Average Math Score',
                                                             'reading_score':'Average Reading Score',
                                                             'per_math_passers':'% Passing Math',
                                                             'per_read_passers':'% Passing Reading',
                                                             'per_math_and_read_passers':'% Overall Passing Rate',
                                                             'size':'Total students'})


# In[105]:


final_sch_descr_table


# In[106]:


final_sch_descr_table=final_sch_descr_table.drop(columns=['Num Math Passers', 'Num Read Passers','Num Read and Math Passers'])


# In[107]:


final_sch_descr_table


# In[110]:


final_sch_descr_table=final_sch_descr_table.sort_values(['% Overall Passing Rate'], ascending=True)


# In[111]:


final_sch_descr_table


# In[112]:


final_sch_descr_table['perf_rank'] = final_sch_descr_table['% Overall Passing Rate'].rank(ascending=0)


# In[113]:


final_sch_descr_table


# In[114]:


# Create variable with TRUE if age is greater than 50
worst_five =final_sch_descr_table['perf_rank'] >10

# Select all cases where nationality is USA and age is greater than 50
sub_set_worst_five=final_sch_descr_table[worst_five]


# In[115]:


sub_set_worst_five


# In[ ]:


#Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
#Create a pandas series for each grade. Hint: use a conditional statement.
#Group each series by school
#Combine the series into a dataframe
#Optional: give the displayed data cleaner formatting


# In[126]:


grade_break_down=school_data_complete.groupby(['school_name','grade']).mean()
grade_break_down


# In[127]:


grade_break_down=grade_break_down.drop(columns=['Student ID', 'math_score','School ID', 'Math and Read Avg','size','budget'])
grade_break_down


# In[ ]:


grade_break_down = grade_break_down.rename(columns={'reading_score': 'School Type'})

