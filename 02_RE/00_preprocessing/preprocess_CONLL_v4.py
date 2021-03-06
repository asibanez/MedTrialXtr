# v2 -> Removes paragrpahs longer than max_seq_len
# v3 -> Adds arm_efficacy_metric and arm_efficacy_results
# v4 -> Fixes bug for adding arm_efficacy_metric and arm_efficacy_results

#%% Imports

import codecs
import pandas as pd

#%% Display options

#pd.set_option('display.max_columns', 2)
#pd.set_option('display.width', 20)

#%% Path definitions

input_path = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\10_Takeda\\05_data\\06_FINAL_21-01\\v3\\v3_annotations.txt'
output_path_1 = 'C:\\Users\\siban\\Dropbox\\CSAIL\\Projects\\10_Takeda\\05_data\\06_FINAL_21-01\\v3\\preprocessed_RE.txt'

#%% Data loading

data = pd.read_csv(input_path, keep_default_na = False)

#%% Global initizalization

tgt_vars_base = ['description',
                 'arm_efficacy_metric-tag','arm_efficacy_metric',
                 'arm_efficacy_results-tag', 'arm_efficacy_results',
                 'arm_description-1-tag', 'arm_description-1', 'arm_dosage-1-tag', 'arm_dosage-1',
                 'arm_description-2-tag', 'arm_description-2', 'arm_dosage-2-tag', 'arm_dosage-2',
                 'arm_description-3-tag', 'arm_description-3', 'arm_dosage-3-tag', 'arm_dosage-3',
                 'arm_description-4-tag', 'arm_description-4', 'arm_dosage-4-tag', 'arm_dosage-4',
                 'arm_description-5-tag', 'arm_description-5', 'arm_dosage-5-tag', 'arm_dosage-5']

#%%
cols_to_remove_1 = ['description', 'arm_efficacy_metric', 'arm_efficacy_results']
cols_to_remove_2 = [x for x in tgt_vars_base if 'tag' in x]
cols_to_remove = cols_to_remove_1 + cols_to_remove_2

tgt_vars = [x for x in tgt_vars_base if x not in cols_to_remove]

max_seq_len = 300

#%% Remove entries with no arm description

filtering = (data['arm_description-1'] == '') & (data['arm_description-2'] == '') &\
    (data['arm_description-3'] == '') & (data['arm_description-4'] == '') &\
        (data['arm_description-5'] == '')

print(f'Shape before removing empty arm descriptors: {data.shape}')
data = data[~filtering]
print(f'Shape after removing empty arm descriptors: {data.shape}')

#%% Remove unwanted columns

data = data[tgt_vars_base]
print(f'Shape after removing unwanted columns: {data.shape}')       

#%% Remove paragraphs shorter than max_seq_len

lens = [len(x.split(' ')) for x in data.description]
filtering = [x <= max_seq_len for x in lens]
data = data[filtering]
print(f'Shape after removing long paragraphs: {data.shape}') 

#%% Capture arm descriptions in different columns

description_new = []
arm_description_tag_new = []
arm_description_new = []
arm_dosage_tag_new = []
arm_dosage_new = []
arm_efficay_metric_tag_new = []
arm_efficay_metric_new = []
arm_efficay_results_tag_new = []
arm_efficay_results_new = []

# Iterate over rows
for _, row in data.iterrows():
    # Iterate over columns
    for idx in range(1,6):
        arm_desc_tag_idx = 'arm_description-' + str(idx) + '-tag'
        arm_desc_idx = 'arm_description-' + str(idx)
        arm_dos_tag_idx = 'arm_dosage-' + str(idx) + '-tag'
        arm_dos_idx = 'arm_dosage-' + str(idx)
        if row[arm_desc_idx] != '':
            description_new.append(row['description'])
            arm_description_tag_new.append(row[arm_desc_tag_idx])
            arm_description_new.append(row[arm_desc_idx])
            arm_dosage_tag_new.append(row[arm_dos_tag_idx])
            arm_dosage_new.append(row[arm_dos_idx])
            arm_efficay_metric_tag_new.append(row['arm_efficacy_metric-tag'])
            arm_efficay_metric_new.append(row['arm_efficacy_metric'])
            arm_efficay_results_tag_new.append(row['arm_efficacy_results-tag'])
            arm_efficay_results_new.append(row['arm_efficacy_results'])

data_new_1 = pd.DataFrame({'description': description_new,
                           'arm_description-tag': arm_description_tag_new,
                           'arm_description': arm_description_new,
                           'arm_dosage-tag': arm_dosage_tag_new,
                           'arm-dosage': arm_dosage_new,
                           'arm_efficacy_metric-tag': arm_efficay_metric_tag_new,
                           'arm_efficacy_metric': arm_efficay_metric_new,
                           'arm_efficacy_results-tag': arm_efficay_results_tag_new,
                           'arm_efficacy_results': arm_efficay_results_new})

#%% Create separated instances for each arm-description in single entry

description_new = []
arm_description_tag_new = []
arm_dosage_tag_new = []
arm_efficay_metric_tag_new = []
arm_efficay_results_tag_new = []

# Iterate over rows
for _, row in data_new_1.iterrows():
    spans_list = row['arm_description-tag'].split(',')
    spans = [(int(x), int(y)) for x, y in zip(spans_list[::2], spans_list[1::2])]
    for idx, span in enumerate(spans):
        description_new.append(row['description'])
        arm_description_tag_new.append(spans[idx])
        arm_dosage_tag_new.append(row['arm_dosage-tag'])
        arm_efficay_metric_tag_new.append(row['arm_efficacy_metric-tag'])
        arm_efficay_results_tag_new.append(row['arm_efficacy_results-tag'])

data_new_2 = pd.DataFrame({'description': description_new,
                           'arm_description-tag': arm_description_tag_new,
                           'arm_dosage-tag': arm_dosage_tag_new,
                           'arm_efficacy_metric-tag': arm_efficay_metric_tag_new,
                           'arm_efficacy_results-tag': arm_efficay_results_tag_new})

#%% Remove rows with empty dosages

#filtering = data_new_2['arm_dosage-tag'] != ''
#data_new_2 = data_new_2[filtering]

#%% Open output file

with codecs.open(output_path_1, 'w', 'utf-8') as fw:

    lens_list = []    

    # Iterate over rows in dataframe
    for idx, row in data_new_2.iterrows():
        text = row['description']
        text_tokens = text.split(' ')
        lens_list.append(len(text_tokens))
        token_tags = ['O'] * len(text_tokens)
        arm_spans = row['arm_description-tag']
        arm_start, arm_end = arm_spans
        
        # Iterate over spans in arm-dosage
        dosage_spans_list = row['arm_dosage-tag'].split(',')
        dosage_spans = [(int(x), int(y)) for x, y in zip(dosage_spans_list[::2], dosage_spans_list[1::2])]
        
        for dosage_span in dosage_spans:
            dosage_start, dosage_end = dosage_span
            token_tags[dosage_start] = 'B-dosage'
            if dosage_end == dosage_start + 1:
                continue
            for i in range(dosage_start + 1, dosage_end):
                token_tags[i] = 'I-dosage'
                
        # Iterate over spans in arm_efficacy_metric
        arm_efficacy_metric_spans_list = row['arm_efficacy_metric-tag'].split(',')
        arm_efficacy_metric_spans = [(int(x), int(y)) \
                                    for x, y in zip(arm_efficacy_metric_spans_list[::2], arm_efficacy_metric_spans_list[1::2])]
        
        for arm_efficacy_metric_span in arm_efficacy_metric_spans:
            arm_efficacy_metric_start, arm_efficacy_metric_end = arm_efficacy_metric_span
            token_tags[arm_efficacy_metric_start] = 'B-arm_efficacy_metric'
            if arm_efficacy_metric_end == arm_efficacy_metric_start + 1:
                continue
            for i in range(arm_efficacy_metric_start + 1, arm_efficacy_metric_end):
                token_tags[i] = 'I-arm_efficacy_metric'
                
        # Iterate over spans in arm_efficacy_results
        arm_efficacy_results_spans_list = row['arm_efficacy_results-tag'].split(',')
        arm_efficacy_results_spans = [(int(x), int(y)) \
                                    for x, y in zip(arm_efficacy_results_spans_list[::2], arm_efficacy_results_spans_list[1::2])]
        
        for arm_efficacy_results_span in arm_efficacy_results_spans:
            arm_efficacy_results_start, arm_efficacy_results_end = arm_efficacy_results_span
            token_tags[arm_efficacy_results_start] = 'B-arm_efficacy_results'
            if arm_efficacy_results_end == arm_efficacy_results_start + 1:
                continue
            for i in range(arm_efficacy_results_start + 1, arm_efficacy_results_end):
                token_tags[i] = 'I-arm_efficacy_results'
        
        # Insert [P1] & [P2] arm identifiers   
        text_tokens.insert(arm_start, '[P1]')
        token_tags.insert(arm_start, 'O')
        text_tokens.insert(arm_end + 1, '[P2]')
        token_tags.insert(arm_end + 1, 'O')
        
        # Write output file 1
        for token, tag in zip(text_tokens, token_tags):
            fw.write(str(idx) + '\t' + token + '\t' + tag + '\n')
        fw.write('\n')
