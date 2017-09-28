import random
from copy import deepcopy

# phrase_extraction('resumption of the session', 'wiederaufnahme der sitzungsperiode', [[0,0], [1,1], [1,2], [2,3]])

# resumption of the session
# wiederaufnahme der sitzungsperiode
# 0-0 1-1 1-2 2-3

# alignments = [[0,0], [1,1], [1,2], [2,3]]
def phrase_extraction(sen1, sen2, alignments):
	sen1_words = sen1.split(" ")
	sen2_words = sen2.split(" ")
	#print(sen1)
	#print(sen2)
	#print(alignments)

	smallest_seg = []
	words_with_alignments = [[],[]]
	words_without_alignments = [[],[]]
	#[[12],[]] <- words without alignments
	for a in alignments:
		left = ""
		right = ""
		for a2 in alignments:
			if a[0] == a2[0]:
				right += a2[1] + " "
				#right += sen1_words[int(a2[1])] + " "
			if a[1] == a2[1]:
				left += a2[0] + " "
				#left += sen2_words[int(a2[0])]  + " "
		add_to_array_if_it_doesnt_contain_reps(int(a[0]), words_with_alignments[0])
		add_to_array_if_it_doesnt_contain_reps(int(a[1]), words_with_alignments[1])
		right = right[:-1]
		left = left[:-1]
		if [left, right] not in smallest_seg:
			smallest_seg.append([left,right])

	for language_index,language in enumerate(words_with_alignments):
		pass_numbers = 0
		language.sort()
		for i,word_as_num in enumerate(language):
			i += pass_numbers
			if i!=word_as_num:
				while(word_as_num!=i):
					word_as_num -= 1
					pass_numbers += 1
					words_without_alignments[language_index	].append(word_as_num)
	#print words_with_alignments
	print words_without_alignments


	len_smallest_seg = len(smallest_seg)
	#print smallest_seg
	en_sub_phrases = []
	de_sub_phrases = []
	aligned_sub_phrases = []
	seg_aligned_sub_phrases = []
	
	for i, element in enumerate(smallest_seg):
		en_strings = ''
		de_strings = ''
		for index in range(i, len_smallest_seg):

			aligned_words = smallest_seg[i:index+1]

			en_strings = add_string_if_it_doesnt_contain_reps(smallest_seg[index][1], en_strings)
			de_strings = add_string_if_it_doesnt_contain_reps(smallest_seg[index][0], de_strings)
			possibilities = [[de_strings, en_strings]]
			for l, language in enumerate(words_without_alignments):
				max_l = max([int(poss) for poss in possibilities[0][l].split()])
				min_l = min([int(poss) for poss in possibilities[0][l].split()])
				for word_without_alignment in language:
					if word_without_alignment < max_l and word_without_alignment > min_l:
						possibilities[0][l] = add_string_if_it_doesnt_contain_reps(str(word_without_alignment), possibilities[0][l])
			
			'''for l, language in enumerate(words_without_alignments):
													for word_without_alignment in language:
														max_l = max(possibilities[0][l].split())
														min_l = min(possibilities[0][l].split())
														elif word_without_alignment == max_l+1:
									
														elif word_without_alignment > max(possibilities[0][l])+1:
															break
														elif word_without_alignment == max_l+1:
									
														elif word_without_alignment > max(possibilities[0][l])+1:
															break'''
			# make sure the longest subphrase is 5 words
			if len(possibilities[0][1].split()) <= 5 and len(possibilities[0][0].split()) <= 5:
				en_strings = reorder_string(possibilities[0][1])
				de_strings = reorder_string(possibilities[0][0])
				if check_continuity(en_strings, de_strings):
					aux_en_strings = translate_numbers_to_words(en_strings, sen1_words)
					aux_de_strings = translate_numbers_to_words(de_strings, sen2_words)
					aux_en_strings = aux_en_strings[:-1]
					aux_de_strings = aux_de_strings[:-1]
					if aux_en_strings not in en_sub_phrases: en_sub_phrases.append(aux_en_strings)
					if aux_de_strings not in de_sub_phrases: de_sub_phrases.append(aux_de_strings)
					if aux_en_strings + ' ^ ' + aux_de_strings not in aligned_sub_phrases:
						aligned_sub_phrases.append(aux_en_strings + ' ^ ' + aux_de_strings)
						seg_aligned_sub_phrases.append(translate_numbers_to_words_aligned(aligned_words, sen1_words, sen2_words))
						#print aux_en_strings + ' | ' + aux_de_strings
						#print seg_aligned_sub_phrases[-1]
						#print '---------------------------------------------------'
					#print(aligned_words)
					#print(aux_en_strings)
					#print(aux_de_strings)
					#print('------------------------------')
	# print(en_sub_phrases)
	# print(de_sub_phrases)
	# print(aligned_sub_phrases)

	return en_sub_phrases, de_sub_phrases, aligned_sub_phrases, seg_aligned_sub_phrases

def add_string_if_it_doesnt_contain_reps(substring, strings):
	for sub_number in substring.split():
		if sub_number in strings.split():
			pass
		else:
			strings += sub_number + ' '
	return strings

def add_to_array_if_it_doesnt_contain_reps(sub_number, array):
	if sub_number in array:
		pass
	else:
		array.append(sub_number)
	return array

def translate_numbers_to_words(string, sentence_words):
	aux_string = ""
	for substring in string.split():
		aux_string += sentence_words[int(substring)] + " "
	return aux_string

def translate_numbers_to_words_aligned(aligned_words, sen1_words, sen2_words):
	aux = deepcopy(aligned_words)
	for i in range(len(aligned_words)):
		for j in range(len(aligned_words[i])):
			aux_string = ""
			for substring in aligned_words[i][j].split():
				if j == 0: aux_string += sen2_words[int(substring)] + " "
				elif j == 1: aux_string += sen1_words[int(substring)] + " "
			aux[i][j] = aux_string[:-1]
	return aux

def reorder_string(strings):
	aux_string = [int(i) for i in strings.split()]
	aux_string.sort()
	aux_string = [str(i) for i in aux_string]
	return " ".join(aux_string) + " "

def check_continuity(en_strings, de_strings):
    en_it = (int(x) for x in en_strings.split())
    en_first = next(en_it)
    de_it = (int(x) for x in de_strings.split())
    de_first = next(de_it)
    return all(a == b for a, b in enumerate(en_it, en_first + 1)) and all(a == b for a, b in enumerate(de_it, de_first + 1))

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
	for en_sen, de_sen, alignment in zip(en_txt[1339:1340], de_txt[1339:1340], alignments[1339:1340]):	

	# for en_sen, de_sen, alignment in zip(en_txt[:no_of_sentences], de_txt[:no_of_sentences], alignments[:no_of_sentences]):	
		if j % 100 == 0:
			print(j/len(en_txt))
		j += 1

		# alignments = [[0,0], [1,1], [1,2], [2,3]]
		alignment = alignment.split()#.split('-')
		for i, el in enumerate(alignment):
			alignment[i] = el.split('-')
		en_sub_phrases, de_sub_phrases, aligned_sub_phrases, seg_aligned_sub_phrases = phrase_extraction(en_sen[:-1], de_sen[:-1], alignment)
		
		# if k == 0:
		# 	print(en_sub_phrases)
		# 	print(de_sub_phrases)
		# 	print(aligned_sub_phrases)
		# 	k += 1

		for en in en_sub_phrases:
			if en in en_dic:
				en_dic[en] += 1
			else:
				en_dic[en] = 1
		for de in de_sub_phrases:
			if de in de_dic:
				de_dic[de] += 1
			else:
				de_dic[de] = 1
		for al, alignments in zip(aligned_sub_phrases, seg_aligned_sub_phrases):
			if al in en_de_dic:
				en_de_dic["".join(al)] += 1
			else:
				en_de_dic["".join(al)] = 1
				# Stores alignments of the sub_phrase. Used in lexical_translation_probabilities(). Example:
				# aligns_dic["session of the ^ sitzungsperiode des"] = [['sitzungsperiode', 'session'], ['des', 'of the']]
				aligns_dic["".join(al)] = alignments
		'''for en, de, al, alignments in zip(en_sub_phrases, de_sub_phrases, aligned_sub_phrases, seg_aligned_sub_phrases):
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
				aligns_dic["".join(al)] = alignments'''
			
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
	# trans_prob[en + ' ^ ' + de] = [p_en_given_de, p_de_given_en]
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

		trans_probs[en + ' ^ ' + de] = [p_en_given_de, p_de_given_en]
		# trans_probs[en + ' - ' + de] = [counts, en_count, de_count]

	return trans_probs

def lexical_translation_probabilities(en_dic,de_dic,al_dic,aligns_dic,count_ef,we,wf):

	# this contains lexical translation probabilities in both directions in the shape of:
	# lex_trans_prob[en + ' ^ ' + de] = [l_en_given_de, l_de_given_en]
	lex_trans_probs = {}

	for pairs,counts in al_dic.items():
		alignments = aligns_dic[pairs]# e.g.: alignments = [['wiederaufnahme', 'resumption'], ['der', 'of the'], ['sitzungsperiode', 'session']]
		[en,de] = pairs.split(" ^ ")
		l_en_given_de = 1
		l_de_given_en = 1
		#print en + " | " + de
		#print alignments
		for align in alignments:
			en_split = align[1].split()
			de_split = align[0].split()
			len_en_split = len(en_split)
			len_de_split = len(de_split)
			for en_word in en_split:
				aux_ef = 0
				for de_word in de_split:
					aux_ef += float(count_ef.get(en_word + ' ' + de_word, 0))/we[en_word]
				l_en_given_de *= aux_ef/len_de_split
			for de_word in de_split:
				aux_ef = 0
				for en_word in en_split:
					aux_ef += float(count_ef.get(en_word + ' ' + de_word, 0))/wf[de_word]
				l_de_given_en *= aux_ef/len_en_split

		lex_trans_probs[en + ' ^ ' + de] = [l_en_given_de, l_de_given_en]

	return lex_trans_probs

if __name__ == '__main__':

	e = open("en.txt", 'r')
	d = open("de.txt", 'r')
	a = open("aligned.txt", 'r')
	en_txt = e.readlines()
	de_txt = d.readlines()
	alignments = a.readlines()

	en_dic,de_dic,al_dic,aligns_dic,count_ef,we,wf = create_dicts(en_txt,de_txt,alignments, 1)

	trans_probs = translation_probabilities(en_dic,de_dic,al_dic)

	# for i in range(10):
	#  	rn = random.choice(list(trans_probs))
	#  	print(rn)
	#  	print(trans_probs[rn])
	# print(en_dic)
	print('----------------------------------------------')

	lex_trans_probs = lexical_translation_probabilities(en_dic,de_dic,al_dic,aligns_dic,count_ef,we,wf)

	# for i in range(10):
	#  	rn = random.choice(list(lex_trans_probs))
	#  	print(rn)
	#  	print(lex_trans_probs[rn])

	# print(trans_probs["indeed - tatsachlich"])
	# print(lex_trans_probs["indeed - tatsachlich"])

	print(len(lex_trans_probs.keys()))

	
	# write to file
	f = open("results", "w")

	f.write("f ||| e ||| p(f|e) p(e|f) l(f|e) l(e|f) ||| freq(f) freq(e) freq(f, e)\n\n")

	for pairs,counts in trans_probs.items():
		e,d = pairs.split(" ^ ")		
		f.write(d + " ||| " + e + " ||| ")
		f.write(str(counts[1]) + " " + str(counts[0]) + " ")

		lex_trans = lex_trans_probs[pairs]

		f.write(str(lex_trans[1]) + " " + str(lex_trans[0]) + " ||| ")

		f.write(str(de_dic[d]) + " " + str(en_dic[e]) + " " + str(al_dic[pairs]))

		f.write("\n")