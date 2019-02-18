import csv
import json
from optparse import OptionParser
from encoding_converter import EncodingConverter

# Parse command-line options
parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help="CSV file to be converted")
#parser.add_option("-o", "--output", dest="output", help="Output file", default="../generated/dictionary.json")

(options, args) = parser.parse_args()

EncodingConverter.convert(options.input)

try:
	csvfile = open(options.input, 'rb')
except:
	print "Problem loading the CSV file -- is the filename correct?"

with csvfile:
	reader = csv.reader(csvfile, delimiter=';')

	data = {}	
	i = 0

	for row in reader:
		if i < 1:
			i += 1
			continue

		data[row[2]] = {
			'English': {
				'singular': {
					'article': '',
					'text': row[3]
				},
				'plural': {
					'article': '',
					'text': row[4]
				}
			},
			'Dutch': {
				'singular': {
					'article': row[5],
					'text': row[6]
				},
				'plural': {
					'article': row[7],
					'text': row[8]
				}
			},
			'German': {
				'singular': {
					'article': row[9],
					'text': row[10]
				},
				'plural': {
					'article': row[11],
					'text': row[12]
				}
			},
			'Turkish': {
				'singular': {
					'article': row[13],
					'text': row[14]
				},
				'plural': {
					'article': row[15],
					'text': row[16]
				}
			}
		}

		# Oops, a random exception needed.. should think about how to make this more scalable ;)
		if row[5] != '' or row[7] != '':
			data[row[2]]['English']['singular']['article'] = 'the'
			data[row[2]]['English']['plural']['article'] = 'the'

		i += 1

	with open('../sessions/outputmanager/dictionary.json', 'w') as savefile:
		savefile.write(json.dumps(data, indent=4, sort_keys=True))