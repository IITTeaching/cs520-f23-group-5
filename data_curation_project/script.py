# implementation of edit distance algorithm by dynamic programing
def edit_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    # Create a matrix to store the edit distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]) + 1

    # Return the edit distance between the two strings
    return dp[m][n]
vizierdb.export_module(edit_distance)

import math
vizierdb.get_module("edit_distance")
default_ds=vizierdb.get_dataset('food_coded')
nulset=set()
nulset.add("nan")
nulset.add("none")
nulset.add("unknown")
clset = set()
for column in default_ds.columns:
    clset.add(column.name)
app_null_list = []
for row in default_ds.rows:
    for cl in clset:
        v = row.get_value(cl)
        if not v:
            continue
        if v in nulset:
            app_null_list.append("rowid: "+row.identifier+"; ed: 0; value: "+v+"; most like word:"+v)
            row[cl] = None
            continue
        try:
            number = float(v)
        except ValueError:
            v = v.strip()
            for nl in nulset:
                ed = edit_distance(nl,v)
                if ed <2:
                    row[cl]=None
                    app_null_list.append("rowid: "+row.identifier+"; ed: "+str(ed)+"; value: "+v+"; most like word:"+nl)
                    break
for n in app_null_list:
    print(n)
vizierdb.update_dataset('food_coded', default_ds)

default_ds=vizierdb.get_dataset('reg_food_coded')
non_numeric_set=set()
non_numeric_set.add('comfort_food')
non_numeric_set.add('comfort_food_reasons')
non_numeric_set.add('diet_current')
non_numeric_set.add('father_profession')
non_numeric_set.add('fav_cuisine')
non_numeric_set.add('food_childhood')
non_numeric_set.add('healthy_meal')
non_numeric_set.add('ideal_diet')
non_numeric_set.add('meals_dinner_friend')
non_numeric_set.add('mother_profession')
non_numeric_set.add('type_sports')
non_numeric_set.add('eating_changes')


clset = set()
for column in default_ds.columns:
    clset.add(column.name)

numeric_set = clset - non_numeric_set
for row in default_ds.rows:
    for cl in numeric_set:
        v=row.get_value(cl)
        if not v:
            continue
        v = v.strip()
        try:
            number = float(v)
        except ValueError:
            print(row.identifier,"->",cl,"->",v)
#vizierdb.update_dataset('food_coded', default_ds)

def extract_longest_number_string(input_string):
    current_number = ""
    longest_number = ""
    for char in input_string:
        if char.isdigit() or char == '.':
            current_number += char
        else:
            if len(current_number) > len(longest_number):
                longest_number = current_number
            current_number = ""
    if len(current_number) > len(longest_number):
        longest_number = current_number
    if longest_number == '.':
        return ""
    return longest_number
vizierdb.export_module(extract_longest_number_string)

import re
default_ds=vizierdb.get_dataset('food_coded')
vizierdb.get_module("extract_longest_number_string")

#define the non numeric columns
non_numeric_set=set()
non_numeric_set.add('comfort_food')
non_numeric_set.add('comfort_food_reasons')
non_numeric_set.add('diet_current')
non_numeric_set.add('father_profession')
non_numeric_set.add('fav_cuisine')
non_numeric_set.add('food_childhood')
non_numeric_set.add('healthy_meal')
non_numeric_set.add('ideal_diet')
non_numeric_set.add('meals_dinner_friend')
non_numeric_set.add('mother_profession')
non_numeric_set.add('type_sports')
non_numeric_set.add('eating_changes')
clset = set()
for column in default_ds.columns:
    clset.add(column.name)
numeric_set = clset - non_numeric_set

str_list=[]
for row in default_ds.rows:
    for cl in numeric_set:
        v = row.get_value(cl)
        if not v:
            continue
        if not re.match('^[0-9]+(\.[0-9]+)?$',v):
            hlstr = extract_longest_number_string(v)
            str_list.append("rowid:"+row.identifier + "," +" column:"+cl + ", value:"+v+"; After extracting:"+hlstr)
            if not hlstr:
                hlstr = None
            row[cl]=hlstr
for n in str_list:
    print(n)
vizierdb.update_dataset('food_coded', default_ds)

default_ds = vizierdb.get_dataset('food_coded')
vizierdb.get_module("extract_longest_number_string")
vizierdb.get_module("edit_distance")
dectect_cl = set()
dectect_cl.add('comfort_food_reasons')
dectect_cl.add('comfort_food_reasons_coded1')

coded_set_dict = {}
coded_set_dict['stress'] = 1
coded_set_dict['boredom'] = 2
coded_set_dict['depression'] = 3
coded_set_dict['sadness'] = 3
coded_set_dict['hunger'] = 4
coded_set_dict['laziness'] = 5
coded_set_dict['cold weather'] = 6
coded_set_dict['happiness'] = 7
coded_set_dict['watching tv'] = 8

for row in default_ds.rows:
	c_f_r = row.get_value('comfort_food_reasons')
	c_f_r_c = row.get_value('comfort_food_reasons_coded1')
	if not c_f_r:
		continue
	vlist = c_f_r.split(",")
	is_predicted = False
	for v in vlist:
		ed = 9999
		predict_v = ""
		for key, value in coded_set_dict.items():
			ed_actual = edit_distance(v, key)
			if ed_actual < ed:
				ed = ed_actual
				predict_v = key
		predict_option = coded_set_dict[predict_v]
		actual_option = c_f_r_c
		print("rowid:" + str(row.identifier) + "; actual - cf reason :" + str(
			c_f_r) + "; actual - cf reason coded :" + str(actual_option) + "; predict reason: " + str(
			predict_v) + "; predict coded:" + str(predict_option))
		if str(actual_option).strip() == str(predict_option).strip():
			is_predicted = True
			break
	print("Predict Hit:" + str(is_predicted) + "; rowid:" + str(row.identifier))


default_ds=vizierdb.get_dataset('food_coded')

fill_set_dict={}
fill_set_dict['comfort_food_reasons_coded1']='9'
fill_set_dict['cook']='5'
fill_set_dict['cuisine']= '6'
fill_set_dict['diet_current_coded']= '4'
fill_set_dict['eating_changes_coded1']= '4'
fill_set_dict['employment']='4'
fill_set_dict['ideal_diet_coded']='8'


for row in default_ds.rows:
    for key,value in fill_set_dict.items():
        value = row[key]
        if not value:
            row[key]=fill_set_dict.get(key)
            print("rowid:"+str(row.identifier)+"; column:"+key+"; cover by:"+fill_set_dict.get(key))
vizierdb.update_dataset('food_coded', default_ds)