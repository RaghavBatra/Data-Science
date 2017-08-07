def fix_extra_a(str1, set_of_values):
	'''
	if [str1] has an "extra" a, and its correct spelling has been encountered, "fix" [str1]
	'''
    try:
        set_of_values.add(str1)
    
        if str1[-1] == "a" and (str1[:-1] in set_of_values):
            return str1[:-1]
    except:
        pass
    return str1