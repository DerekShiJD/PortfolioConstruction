import numpy as np

path = "SP500/SP500Companies.txt"

temp_file = open(path, 'r')
all_content = temp_file.read()
temp_file.close()

# List of all companies

all_list = []
temp_word = ''
temp_element = []

for i in all_content:
    if i == '\t':
        temp_element.append(temp_word)
        temp_word = ''
    elif i == '\n':
        temp_element.append(temp_word)
        temp_word = ''
        all_list.append(temp_element)
        temp_element = []
    else:
        temp_word += i

all_array = np.array(all_list)

np.save('SP500/SP500Companies.npy', all_array)

array_shape = np.shape(all_array)

# List of sectors

all_sector = []
all_sector_id = []
all_industry = []
all_industry_id = []

for i in range(array_shape[0]):
    if all_array[i][2] not in all_sector:
        all_sector.append(all_array[i][2])
        temp_industry = [all_array[i][3]]
        all_industry.append(temp_industry)
        temp_sector_id = [i]
        temp_industry_id = [[i]]
        all_sector_id.append(temp_sector_id)
        all_industry_id.append(temp_industry_id)
    else:
        idx = all_sector.index(all_array[i][2])
        all_sector_id[idx].append(i)
        if all_array[i][3] not in all_industry[idx]:
            all_industry[idx].append(all_array[i][3])
            temp_industry_id = [i]
            all_industry_id[idx].append(temp_industry_id)
        else:
            if all_array[i][3] == 'Asset Management & Custody Banks':
                b = 1
            idx_2 = all_industry[idx].index(all_array[i][3])
            all_industry_id[idx][idx_2].append(i)

# Print the count of companies in each sector

sum_all = 0
sum_ind = 0

for i in range(len(all_sector)):
    sum_all += len(all_sector_id[i])
    print(str(len(all_sector_id[i])) + '\t' + all_sector[i])
    for j in range(len(all_industry[i])):
        print('\t' + str(len(all_industry_id[i][j])) + '\t' + all_industry[i][j])
        sum_ind += len(all_industry_id[i][j])
    # print("\tSub-industry:" + str(sum_ind))
    sum_ind = 0

print("Total number: " + str(sum_all))

np.save('SP500/all_sector.npy', all_sector)
np.save('SP500/all_sector_id.npy', all_sector_id)
np.save('SP500/all_industry.npy', all_industry)
np.save('SP500/all_industry_id.npy', all_industry_id)

