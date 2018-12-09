saved_response = ['movie tickets', 'question']

movie_responses = {
	'cinema': ['genesis deluxe', 'film house'],
	'location': [['Psalm', 'leisure', 'maryland'], ['Ikeja', 'Ojota', 'Ketu']]
}
j = 0

questions = ['select cinema', 'select location']

while j < 2:
	to_ask = questions[j]
	for msg, reply in movie_responses.items():		
		if msg in to_ask:
			print(reply)
	j += 1


question = None
found = False
b = 0
answers = []
# print(responses[saved_response[0]])
# print(saved_response[0] + saved_response[1])
# print(responses[saved_response[0]saved_response[1]])

# while b < len(saved_response):
# 	if saved_response[b] in responses:		
# 		f_rep = saved_response[b]		
# 		b += 1
# 		print(f_rep)		
# 		print(responses[f_rep].values())
# 	b+=1

# for b in saved_response:
# 	# reply = message['text'].lower()		
# 	print(responses[b])
# 	for i in responses[b]:

	# for response in responses:

	# 	if reply in response:
	# 		# print(responses[response]['question'])
	# 		question = responses[response]['question']
	# 		for answer in responses[response]['answer']:
	# 			answers.append(answer)
	# 	elif reply in saved_response[b]:
	# 		question = responses[saved_response[b]]['question']
	# 		for answer in responses[saved_response[b]]['answer']:				
	# 			answers.append(answer)
	# b += 1
print(question, answers)
