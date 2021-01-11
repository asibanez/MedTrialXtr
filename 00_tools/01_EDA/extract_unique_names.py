import pandas as pd
from tqdm import tqdm

#%%
data = pd.read_csv('extracted_names_all', keep_default_na = False, na_values=['NaN'])
print('Data shape = ', data.shape)
output_file = 'name_list.txt'
names = []

#%%
for index_1 in tqdm(range(data.shape[0])):
    print('index 1 = ', index_1)
    text = data['description'][index_1]
    #spans = data['name_spans'][index_1].strip('[').strip(']').split(', ')    
    spans = data['spans'][index_1].split(', ')    
    if spans != ['']:
        for index_2 in range(0, len(spans), 2):
            b_span = int(spans[index_2])
            e_span = int(spans[index_2+1])
            name = text[b_span:e_span]
            if name != '':
                names.append(name)

#%% 
unique_names = set(names)
unique_names_list = sorted(list(unique_names))

#%%
with open(output_file, 'w', encoding = 'utf-8') as f:
    for item in tqdm(unique_names_list):
        f.write(item + '\n')
        
#%%
