import re


def bio_to_xml(utterance, bio_annotation):
	utterance_tokens = utterance.split()
	bio_annotation_tokens = bio_annotation.split()
	if len(utterance_tokens) != len(bio_annotation_tokens):
		return utterance
	opened_tag = False
	result = []
	for i in range(len(utterance_tokens)):
		tag = re.search('([bi])-([^@]+)@([^@]+)', bio_annotation_tokens[i])
		out_token = utterance_tokens[i]
		if tag:
			mode, sn, si = tag.group(1), tag.group(2), tag.group(3)
			if mode == 'b':
				if opened_tag is True:
					result[i-1] = "{}</{}@{}>".format(result[i-1], last_tag[0], last_tag[1])
				opened_tag = True
				out_token = "<{}@{}>{}".format(sn, si, out_token)
			last_tag = (sn, si)
		else:
			if opened_tag is True:
				result[i-1] = "{}</{}@{}>".format(result[i-1], last_tag[0], last_tag[1])
				opened_tag = False

		result.append(out_token)
	if opened_tag is True:
			result[-1] = "{}</{}@{}>".format(result[-1], last_tag[0], last_tag[1])
	
	return ' '.join(result)
