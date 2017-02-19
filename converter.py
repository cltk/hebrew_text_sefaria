import os, re
import json
import pdb
import collections
from django.utils.text import slugify

sourceLink = 'http://www.sefaria.org/'
source = 'Sefaria'
works = []

def jaggedListToDict(text):
	textNodes = []
	for t in text:
		if not isinstance(t, int) and len(t):
			textNodes.append(t)
	node = { str(i): t for i, t in enumerate(textNodes) }
	node = collections.OrderedDict(sorted(node.items(), key=lambda k: int(k[0])))
	for child in node:
		if isinstance(node[child], list):
			if len(node[child]) == 1:
				node[child] = node[child][0]
			else:
				node[child] = jaggedListToDict(node[child])

	return node

def main():
	if not os.path.exists('cltk_json'):
		os.makedirs('cltk_json')

	# Build json docs from txt files
	for root, dirs, files in os.walk("."):
		path = root.split('/')
		print((len(path) - 1) * '---', os.path.basename(root))
		for fname in files:
			if fname == 'merged.json' and 'Other' not in path:
				with open(os.path.join(root, fname)) as f:
					data = json.load(f)
				work = {
					'originalTitle': data['heTitle'],
					'englishTitle': data['title'],
					'author': 'Not available',
					'source': source,
					'sourceLink': sourceLink,
					'language': '',
					'text': {},
				}
				if data['language'] == 'he':
					work['language'] = 'hebrew'
				elif data['language'] == 'en':
					work['language'] = 'english'
				else:
					print('language not identified--review manually', root, fname)


				work['text'] = jaggedListToDict(data['text'])
				works.append(work)

	for work in works:
		fname = slugify(work['source']) + '__' + slugify(work['englishTitle'][0:140]) + '__' + slugify(work['language']) + '.json'
		fname = fname.replace(" ", "")
		with open('cltk_json/' + fname, 'w') as f:
			json.dump(work, f)

if __name__ == '__main__':
	main()
