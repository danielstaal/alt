import random

# alignments = [[0,0], [1,1], [1,2], [2,3]]
def phrase_extraction(sen1, sen2, alignments):
	sen1_words = sen1.split(" ")
	sen2_words = sen2.split(" ")

	print(sen1)
	print(sen2)
	print(alignments)

	smallest_seg = []
	for a in alignments:
		left = []
		right = []
		for a2 in alignments:
			if a[0] == a2[0]:
				right.append(sen1_words[int(a2[1])])
			if a[1] == a2[1]:
				left.append(sen2_words[int(a2[0])])
		if [left, right] not in smallest_seg:
			smallest_seg.append([left,right])

	len_smallest_seg = len(smallest_seg)
	# aligned_sub_phrases = 
	en_sub_phrases = []
	de_sub_phrases = []
	de_strings = ''
	en_strings = ''
	for i, element in enumerate(smallest_seg):
		# sub_phrases.append(element)
		for index in range(i+1,len_smallest_seg+1):
			aligned_words = smallest_seg[i:index] 
			# aligned_sub_phrases.append(aligned_sub_phrase)
			en_sub_phrases += [[sub[1] for sub in aligned_words]]
			de_sub_phrases += [[sub[0] for sub in aligned_words]]

	for i, sub in enumerate(en_sub_phrases):
		en_sub_phrases[i] = [val for sublist in sub for val in sublist]
	for i, sub in enumerate(de_sub_phrases):
		de_sub_phrases[i] = [val for sublist in sub for val in sublist]

	aligned_sub_phrases = zip(en_sub_phrases, de_sub_phrases)

	return en_sub_phrases, de_sub_phrases, aligned_sub_phrases

# phrase_extraction('resumption of the session', 'wiederaufnahme der sitzungsperiode', [[0,0], [1,1], [1,2], [2,3]])

# resumption of the session
# wiederaufnahme der sitzungsperiode
# 0-0 1-1 1-2 2-3

def create_dicts():
	en_dic = {}
	de_dic = {}
	en_de_dic = {}

	e = open("en.txt", 'r')
	d = open("de.txt", 'r')
	a = open("aligned.txt", 'r')
	en_txt = e.readlines()
	de_txt = d.readlines()
	alignments = a.readlines()

	i = 0
	for en_sen, de_sen, alignment in zip(en_txt, de_txt, alignments):	

		# alignments = [[0,0], [1,1], [1,2], [2,3]]
		alignment = alignment.split()#.split('-')
		for i, el in enumerate(alignment):
			alignment[i] = el.split('-')

		en_sub_phrases, de_sub_phrases, aligned_sub_phrases = phrase_extraction(en_sen[0:-1], de_sen[0:-1], alignment)
		# if i == 0:
		# 	print(en_sub_phrases)
		# 	print(de_sub_phrases)
		# 	print(aligned_sub_phrases)

		# i += 1
		# if en_sen in en_dic:
		# 	en_dic[en_sen[0:-3]] += 1
		# else:
		# 	en_dic[en_sen[0:-3]] = 1
		# if de_sen in de_dic:
		# 	de_dic[de_sen[0:-3]] += 1
		# else:
		# 	de_dic[de_sen[0:-3]] = 1
		# # keep the space
		# en_de = en_sen[0:-2] + de_sen[0:-3]
		# if en_de in en_de_dic:
		# 	en_de_dic[en_de] += 1
		# else:
		# 	en_de_dic[en_de] = 1

		# print(en_de_dic)
		# print(en_dic['resumption of the process'])


if __name__ == '__main__':
	create_dicts()
