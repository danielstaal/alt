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

	# print(smallest_seg)

	# we do not want subphrases longer than 5
	# TODO does not work yet
	#print(smallest_seg)
	range_up_to_five = len(smallest_seg)

	en_sub_phrases = []
	de_sub_phrases = []
	aligned_sub_phrases = []
	seg_aligned_sub_phrases = []
	
	for i, element in enumerate(smallest_seg):
		if range_up_to_five - i > 5:
			range_up_to_five = i + 5

		for index in range(i+1,range_up_to_five+1):
			de_strings = ''
			en_strings = ''
			# TODO make sure the longest subphrase is 5 words
			aligned_words = smallest_seg[i:index] 
			
			for sub in aligned_words:
				en_strings += sub[1] + " "
				de_strings += sub[0] + " "
			en_strings = en_strings[:-1]
			de_strings = de_strings[:-1]
			en_sub_phrases.append(en_strings)
			de_sub_phrases.append(de_strings)
			aligned_sub_phrases.append(en_strings + ' ^ ' + de_strings)
			seg_aligned_sub_phrases.append(aligned_words)
			#print(aligned_words)
			#print(en_strings)
			#print(de_strings)
			#print('------------------------------')

	return en_sub_phrases, de_sub_phrases, aligned_sub_phrases, seg_aligned_sub_phrases


def create_dicts(en_txt,de_txt,alignments, no_of_sentences=50000):
	en_dic = {}
	de_dic = {}
	en_de_dic = {}
	aligns_dic = {}
	# KMO dictionaries
	count_ef = {}# count of appeareances of single words aligned to other language words
	we = {}# appearance of single words (english)
	wf = {}# appearance of single words (deutsch)

	j = 0
	k = 0
	for en_sen, de_sen, alignment in zip(en_txt[:no_of_sentences], de_txt[:no_of_sentences], alignments[:no_of_sentences]):	
		if j % 100 == 0:
			print(j/len(en_txt))
		j += 1

		# alignments = [[0,0], [1,1], [1,2], [2,3]]
		alignment = alignment.split()#.split('-')
		for i, el in enumerate(alignment):
			alignment[i] = el.split('-')
		en_sub_phrases, de_sub_phrases, aligned_sub_phrases, seg_aligned_sub_phrases = phrase_extraction(en_sen[0:-1], de_sen[0:-1], alignment)
		
		# if k == 0:
		# 	print(en_sub_phrases)
		# 	print(de_sub_phrases)
		# 	print(aligned_sub_phrases)
		# 	k += 1

		for en, de, al, alignments in zip(en_sub_phrases, de_sub_phrases, aligned_sub_phrases, seg_aligned_sub_phrases):
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
				# Stores alignments of the sub_phrase. Used in lexical_translation_probabilities(). Example:
				# aligns_dic["session of the ^ sitzungsperiode des"] = [['sitzungsperiode', 'session'], ['des', 'of the']]
				aligns_dic["".join(al)] = alignments
			
	# print(len(en_dic))
	# print(len(de_dic))
	# print(len(en_de_dic))

	# words counting not working atm (PHRASE -> SUB_PHRASES -> COUNTS APPEAREANCES IN SUB_PHRASES ATM)
	for pairs,counts in en_de_dic.items():
		[en,de] = pairs.split(" ^ ")
		en_split = en.split()
		de_split = de.split()
		for en_word in en_split:
			for de_word in de_split:
				ende = en_word + ' ' + de_word
				count_ef[ende] = count_ef.get(ende, 0) + 1
		for en_word in en_split:
			we[en_word] = we.get(en_word, 0) + 1
		for de_word in de_split:
			wf[de_word] = wf.get(de_word, 0) + 1

	return en_dic,de_dic,en_de_dic,aligns_dic,count_ef,we,wf

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
		# trans_probs[en + ' - ' + de] = [counts, en_count, de_count]

	return trans_probs

def lexical_translation_probabilities(en_dic,de_dic,al_dic,aligns_dic,count_ef,we,wf):

	# this contains lexical translation probabilities in both directions in the shape of:
	# lex_trans_prob[en + ' - ' + de] = [l_en_given_de, l_de_given_en]
	lex_trans_probs = {}

	for pairs,counts in al_dic.items():
		alignments = aligns_dic[pairs]# e.g.: alignments = [['wiederaufnahme', 'resumption'], ['der', 'of the'], ['sitzungsperiode', 'session']]
		[en,de] = pairs.split(" ^ ")
		l_en_given_de = 1
		l_de_given_en = 1
		for align in alignments:
			en_split = align[1].split()
			de_split = align[0].split()
			len_en_split = len(en_split)
			len_de_split = len(de_split)

			for en_word in en_split:
				aux_ef = 0
				for de_word in de_split:
					aux_ef += float(count_ef[en_word + ' ' + de_word])/we[en_word]
				l_en_given_de *= aux_ef/len_de_split

			for de_word in de_split:
				aux_ef = 0
				for en_word in en_split:
					aux_ef += float(count_ef[en_word + ' ' + de_word])/wf[de_word]
				l_de_given_en *= aux_ef/len_en_split

		lex_trans_probs[en + ' - ' + de] = [l_en_given_de, l_de_given_en]

	return lex_trans_probs

if __name__ == '__main__':

	e = open("en.txt", 'r')
	d = open("de.txt", 'r')
	a = open("aligned.txt", 'r')
	en_txt = e.readlines()
	de_txt = d.readlines()
	alignments = a.readlines()

	en_dic,de_dic,al_dic,aligns_dic,count_ef,we,wf = create_dicts(en_txt,de_txt,alignments, 5000)

	trans_probs = translation_probabilities(en_dic,de_dic,al_dic)

	for i in range(10):
		rn = random.choice(list(trans_probs))
		print(rn)
		print(trans_probs[rn])
	# print(en_dic)
	print('----------------------------------------------')

	lex_trans_probs = lexical_translation_probabilities(en_dic,de_dic,al_dic,aligns_dic,count_ef,we,wf)

	for i in range(10):
		rn = random.choice(list(lex_trans_probs))
		print(rn)
		print(lex_trans_probs[rn])