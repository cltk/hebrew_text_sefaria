import os, re
import json
import pdb
import collections

sourceLink = 'http://www.sefaria.org/'
source = 'Sefaria'
works = []

def walkText(text):
	node = { str(i): t for i, t in enumerate(text) }
	node = collections.OrderedDict(sorted(node.items()))
	for child in node:
		if isinstance(node[child], list):
			node[child] = walkText(node[child])
	return node

def main():
	# Build json docs from txt files
	for root, dirs, files in os.walk("."):
		path = root.split('/')
		print((len(path) - 1) * '---', os.path.basename(root))
		for fname in files:
			if fname == 'merged.json':
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


				work['text'] = walkText(data['text'])
				works.append(work)

	for work in works:
		fname = work['source'] + '__' + work['englishTitle'] + '__' + work['language'] + '.json'
		fname = fname.replace(" ", "")
		if not os.path.exists('cltk_json'):
			os.makedirs('cltk_json')
		with open('cltk_json/' + fname, 'w') as f:
			json.dump(work, f)

if __name__ == '__main__':
	main()
