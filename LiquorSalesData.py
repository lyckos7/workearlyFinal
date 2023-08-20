import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime
import numpy as np

# read data from csv
data = pd.read_csv('finance_liquor_sales.csv')

# get the most popular item per zip code
most_popular_zip_code = data.groupby(['zip_code', 'item_description'])['bottles_sold'].max().reset_index()
most_popular = most_popular_zip_code.loc[most_popular_zip_code.groupby('zip_code')['bottles_sold'].idxmax()]

# get the percentage of sales per store
# sum of all bottles sold
sum_bottles_sold = data['bottles_sold'].sum()
# sum of bottles sold per store
sum_bottles_sold_per_store = data.groupby(['store_number', 'store_name'])['bottles_sold'].sum().reset_index()
# Calculate the percentage of sales for each store
sum_bottles_sold_per_store['percentage'] = (sum_bottles_sold_per_store['bottles_sold'] / sum_bottles_sold)*100
# get the first 10 stores
sorted_by_percentage=sum_bottles_sold_per_store.sort_values(by='percentage', ascending=False).head(10)

# get sales per date
sales_per_date=data.groupby('date')['bottles_sold'].sum().reset_index().dropna()

#create a figure for 3 subplots in a row and change the window's title
fig, axs = plt.subplots(nrows=1, ncols=3, num='WorkEarly final')

# Create the 1st subplot to show the quantity that was sold, of the most popular item per zip code 
colors = cm.gist_ncar(np.linspace(0, 1, len(most_popular['zip_code'])))
for zipcode, c in zip(most_popular['zip_code'], colors):
    axs[0].scatter(zipcode, most_popular[most_popular['zip_code'] == zipcode]['bottles_sold'], color = c)
axs[0].grid(True)
axs[0].set_xlabel('Zip Code')
axs[0].set_ylabel('Bottles Sold')
axs[0].set_title('Most popular Drink per Zip Code')

# Create the 2nd subplot to show the percentages of sales of the first 10 stores 
colors2 = cm.tab20(np.linspace(0, 1, 10))
for name, c in zip(sorted_by_percentage['store_name'], colors2):
    axs[1].bar(name, sorted_by_percentage[sorted_by_percentage['store_name']==name]['percentage'], color = c)
axs[1].tick_params(axis='x', labelsize=5, rotation=90)
axs[1].grid(axis='y')
axs[1].set_xlabel('first 10 stores')
axs[1].set_ylabel('percentage of sales')
axs[1].set_title('Percentage of Sales per Store')

# Create the 3rd subplot to show the botle sales according to dates 
colors3 = cm.cool(np.linspace(0, 1, len(sales_per_date['date'])))
for date, c in zip(sales_per_date['date'], colors3):
    d =datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
    axs[2].plot(d, sales_per_date[sales_per_date['date']==date]['bottles_sold'], marker = 'x', markersize = 8, color = c)  
axs[2].axvline(pd.Timestamp('2020-01-01'),color='r')
axs[2].tick_params(axis='x', labelsize=10, rotation=45)
axs[2].set_xlabel('Dates')
axs[2].set_title('Sales per date')
axs[2].set_ylabel('Bottles Sold')
# set figure width and title
fig.set_figwidth(13)
fig.suptitle('WorkEarly_Final_Assignment')
# To auto adjust the padding of the suplots
plt.tight_layout()
# To show the plot
plt.show()