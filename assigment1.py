import random

# phrase_extraction('resumption of the session', 'wiederaufnahme der sitzungsperiode', [[0,0], [1,1], [1,2], [2,3]])

# resumption of the session
# wiederaufnahme der sitzungsperiode
# 0-0 1-1 1-2 2-3

# alignments = [[0,0], [1,1], [1,2], [2,3]]
def phrase_extraction(sen1, sen2, alignments):
	sen1_words = sen1.split(" ")
	sen2_words = sen2.split(" ")
	# print(sen1)
	# print(sen2)
	# print(alignments)

	smallest_seg = []
	for a in alignments:
		left = ""
		right = ""
		for a2 in alignments:
			if a[0] == a2[0]:
				right += sen1_words[int(a2[1])] + " "
			if a[1] == a2[1]:
				left += sen2_words[int(a2[0])]  + " "
		right = right[:-1]
		left = left[:-1]
		if [left, right] not in smallest_seg:
			smallest_seg.append([left,right])

	# we do not want subphrases longer than 5
	# TODO does not work yet
	range_up_to_five = len(smallest_seg)

	en_sub_phrases = []
	de_sub_phrases = []
	aligned_sub_phrases = []
	
	for i, element in enumerate(smallest_seg):
		if i - range_up_to_five > 5:
			range_up_to_five = i + 5

		for index in range(i+1,range_up_to_five+1):
			de_strings = ''
			en_strings = ''
			# TODO make sure the longest subphrase is 5 words
			aligned_words = smallest_seg[i:index] 
			
			for sub in aligned_words:
				en_strings += sub[1]  + " "
				de_strings += sub[0]  + " "
			en_strings = en_strings[:-1]
			de_strings = de_strings[:-1]
			en_sub_phrases.append(en_strings)
			de_sub_phrases.append(de_strings)
			aligned_sub_phrases.append(en_strings + ' ^ ' + de_strings)

	return en_sub_phrases, de_sub_phrases, aligned_sub_phrases



def create_dicts(en_txt,de_txt,alignments):
	en_dic = {}
	de_dic = {}
	en_de_dic = {}

	j = 0
	k = 0
	for en_sen, de_sen, alignment in zip(en_txt[:100], de_txt[:100], alignments[:100]):	
		if j % 100 == 0:
			print(j/len(en_txt))
		j += 1

		# alignments = [[0,0], [1,1], [1,2], [2,3]]
		alignment = alignment.split()#.split('-')
		for i, el in enumerate(alignment):
			alignment[i] = el.split('-')
		en_sub_phrases, de_sub_phrases, aligned_sub_phrases = phrase_extraction(en_sen[0:-1], de_sen[0:-1], alignment)
		
		# if k == 0:
		# 	print(en_sub_phrases)
		# 	print(de_sub_phrases)
		# 	print(aligned_sub_phrases)
		# 	k += 1

		for en, de, al in zip(en_sub_phrases, de_sub_phrases, aligned_sub_phrases):
			if en in en_dic:
				en_dic[en] += 1
			else:
				en_dic[en] = 1
			if de in de_dic:
				de_dic[de] += 1
			else:
				de_dic[de] = 1
			if al in en_de_dic:
				en_de_dic["".join(al)] += 1
			else:
				en_de_dic["".join(al)] = 1
			
	# print(len(en_dic))
	# print(len(de_dic))
	# print(len(en_de_dic))

	return en_dic,de_dic,en_de_dic

def translation_probabilities(en_dic,de_dic,al_dic):

	# this contains translation probabilities in both directions in the shape of:
	# trans_prob[en + ' - ' + de] = [p_en_given_de, p_de_given_en]
	trans_probs = {}

	# print(al_dic)
	# print(random.choice(al_dic.items()))

	for pairs,counts in al_dic.items():
		# print(pairs)
		[en,de] = pairs.split(" ^ ")
		en_count = en_dic[en]
		de_count = de_dic[de]
		p_de_given_en = float(counts)/en_count
		p_en_given_de = float(counts)/de_count

		trans_probs[en + ' - ' + de] = [p_en_given_de, p_de_given_en]

	return trans_probs

if __name__ == '__main__':

	e = open("en.txt", 'r')
	d = open("de.txt", 'r')
	a = open("aligned.txt", 'r')
	en_txt = e.readlines()
	de_txt = d.readlines()
	alignments = a.readlines()

	en_dic,de_dic,al_dic = create_dicts(en_txt,de_txt,alignments)

	trans_probs = translation_probabilities(en_dic,de_dic,al_dic)

	rn = random.choice(list(trans_probs))
	print(rn)
	print(trans_probs[rn])
	# print(trans_probs)

