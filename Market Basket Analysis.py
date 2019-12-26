#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import itertools


# In[2]:


#Import Data
orders = pd.read_csv("C:\\Users\\Owner\\Documents\\School\\Masters of Science in Analytics\\Semesters\\Fall Semester\\Data Mining\\Homework\\Homework 1 - Market Basket Analysis\\wide_restaurantData.csv")
orders = orders.rename(columns={"0": "OrderNumber"})
orders = orders.set_index('OrderNumber')


# In[3]:


###Get uniques sets to perfrom market basket analysis and other analytics on
unique_meats = list(set(orders['Meat']))

unique_wines = list(set(orders['Wine']))

unique_meals = list(set(orders['Meat'] + ', ' + orders['Side'] + ', ' + orders['Wine']))

unique_meals = [i.replace(' ','') for i in unique_meals]


# In[4]:


###Counts the number of orders made for each unique order composition

#Makes a column with the meals to be matched to the unique meal set
orders['Complete Meal'] = orders['Meat'] + ', ' + orders['Side'] + ', ' + orders['Wine']
orders['Complete Meal'] = orders['Complete Meal'].str.replace(' ', '')

#Empty vector with length equal to the numer of unique meals
order_count = [0]*len(unique_meals)
index = 0

for meal in unique_meals:
    meal_count = len(orders['Complete Meal'][orders['Complete Meal'] == meal])
    order_count[index] = meal_count
    index += 1

popular_orders = pd.DataFrame([unique_meals, order_count]).transpose()
popular_orders.columns = ['Meal', 'Total Orders']
sorted_popular_orders = popular_orders.sort_values(by='Total Orders', ascending=False)
print('The most ordered meal is', sorted_popular_orders.iloc[0].values[0])


# In[5]:


orders = orders.drop('Complete Meal', axis=1)


# In[8]:


#Define functions to calculate support, confidence, and lift

def support_(data, meat, wine):
    
    df = data
    
    len_df = len(df)
    
    support = len(df[(df['Meat'] == meat) & (orders['Wine'] == wine)]) / len_df

    return support

support = support_(orders, 'Roast Chicken', 'Blackstone Merlot')



def confidence_(data,support, meat, wine):
    
    df = data
    
    len_df = len(df)
    
    p_meat = len(df[(df['Meat'] == meat)]) / len_df
    
    confidence = support / p_meat
    
    return confidence

confidence = confidence_(orders, support, 'Roast Chicken', 'Blackstone Merlot')


    
def lift_(data,support, meat, wine):
    
    df = data
    
    len_df = len(df)
    
    p_meat = len(df[(df['Meat'] == meat)]) / len_df
    
    p_wine = len(df[(df['Wine'] == wine)]) / len_df
    
    lift = support / (p_wine*p_meat)
    
    return lift

lift = lift_(orders,support, 'Roast Chicken', 'Blackstone Merlot')


# In[9]:


### Implement functions to calculate the support confidence and lift for different order pairs

meat_wine_pairs = list(itertools.product(unique_meats, unique_wines))

mb_index = [list(i)[0] + ' ==> ' + list(i)[1] for i in meat_wine_pairs]

mb = []

for pairs in meat_wine_pairs:
    
    pair = list(pairs)
    
    support = support_(orders, pair[0], pair[1])
    
    confidence = confidence_(orders, support, pair[0], pair[1])
    
    lift = lift_(orders, support, pair[0], pair[1])
    
    row = [support, confidence, lift]
    
    mb.append(row)
    
col_names = ['support', 'confidence', 'lift']

final_market_basket = pd.DataFrame(mb, columns=col_names, index=mb_index)


# In[10]:


final_market_basket


# In[11]:


#final_market_basket.to_csv("C:\\Users\\Owner\\Documents\\School\\Masters of Science in Analytics\\Semesters\\Fall Semester\\Data Mining\\Homework\\Homework 1\\market_basket.csv")

