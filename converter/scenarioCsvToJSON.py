import csv
import json
from optparse import OptionParser
import copy
import re

from sceneModel import SceneModel

from encoding_converter import EncodingConverter

def is_number(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def build_object(in_str):
	#print in_str
	location = ''	
	# Parse locations denoted by < and >
	if in_str.find('<') != -1 and in_str.find('>') != 1:
		location = in_str[in_str.find('<')+1:in_str.find('>')].upper()
		obj_id = in_str[:in_str.find('<')]

	else:
		obj_id = in_str

	if obj_id.find('(') != -1:
		if obj_id[obj_id.find('(')+1:obj_id.find(')')] == 'disabled':
			new_object = {
				'object_id': obj_id[:obj_id.find('(')],
				'enabled': False
			}
		else:
			# It's a motion or animation
			print obj_id
			params = obj_id[obj_id.find('(')+1:obj_id.find(')')].split(':')

			print params

			# animation
			if len(params) == 1 or len(params) == 2:
				new_object = {
					'object_id': obj_id[:obj_id.find('(')],
					'animation': params[0].strip(),
					'loop': 'false'
				}

				if len(params) == 2:
					new_object['loop'] = params[1].strip().lower()

			# motion
			else:
				new_object = {
					'object_id': obj_id[:obj_id.find('(')],
					'x': params[0].strip(),
					'y': params[1].strip(),
					'z': params[2].strip(),
					'speed': params[3].strip(),
					'loop': params[4].strip()
				}
	else:
		new_object = {
			'object_id': obj_id
		}

	if location != '':
		new_object['location'] = location

	return new_object



def parse_tablet_objects(in_str):
	out = list()

	amount = 1
	prev_objs = list()
	is_new_obj = True

	if in_str.endswith(' and '):
		in_str = in_str[:-4]

	in_str = in_str.strip()
	in_str = in_str.replace('next to', 'next_to')

	in_brackets = False
	newstr = ''
	for c in in_str:
		if c == '<':
			in_brackets = True
		if c == '>':
			in_brackets = False
		if c == ' ' and in_brackets:
			newstr += '_'
		else:
			newstr += c

	in_str = newstr
	#print in_str

	'''if in_str.find('<') != -1 and in_str.find('>') != 1:
		test2 = in_str[in_str.find('<')+1:in_str.find('>')]
		test2 = test2.upper().replace(' ', '_')
		in_str = in_str.replace(in_str[in_str.find('[')+1:in_str.find(']')], test2)'''

	# We split the string whenever a space occurs to analyze spatial relationships and split multiple objects
	subs = in_str.split(' ')

	index = 0
	while index < len(subs):
		s = subs[index]
		subs2 = s.split(',')

		for s2 in subs2:
			if s2 == '':
				continue

			#print str(is_new_obj) + ' ' + s2
			is_new_obj = True

			if s2 == 'a' or s2 == 'an':
				s2 = 1

			if s2 == 'and':
				is_new_obj = True
				continue

			if is_number(s2):
				amount = int(s2)
				continue

			if s2.lower() == 'between':
				for o in prev_objs:
					o['object_relationship'] = {
						'type': 'BETWEEN',
						'obj_1': build_object(subs[index+1]),
						'obj_2': build_object(subs[index+3]),
					}

				index += 3

			else:
				if not is_new_obj:
					for p in prev_objs:
						p['object_id'] += ' ' + s2
					continue

				prev_objs = list()

				# We found a new object
				new_obj = build_object(s2)
				#print new_obj

				if amount > 1 and new_obj['object_id'][-1] == 's':
					new_obj['object_id'] = new_obj['object_id'][:-1]

				if index+2 < len(subs) and subs[index+1] == 'next_to':
					if index+3 < len(subs) and (subs[index+2] == 'a' or subs[index+2] == 'an' or subs[index+2] == 'the'):
						new_obj['object_relationship'] = {
							'type': 'NEXT_TO',
							'obj': build_object(subs[index+3])
						}
						index += 3
					else:
						new_obj['object_relationship'] = {
							'type': 'NEXT_TO',
							'obj': build_object(subs[index+2])
						}
						index += 2

				if index+2 < len(subs) and subs[index+1] == 'in':
					if index+3 < len(subs) and (subs[index+2] == 'a' or subs[index+2] == 'an'):
						new_obj['object_relationship'] = {
							'type': 'IN',
							'obj_parent': build_object(subs[index+3])
						}
						index += 3
					else:
						new_obj['object_relationship'] = {
							'type': 'IN',
							'obj_parent': build_object(subs[index+2])
						}
						index += 2

				i = 0
				while i < amount:
					prev_objs.append(new_obj)
					out.append(new_obj)

					i += 1

				amount = 1
				is_new_obj = False

		index += 1

		#if s.endswith(',')


	# Split multiple objects (separated by 'and' or comma)
	#subs = in_str.split(' and ')

	'''
	for s in subs:
		subs2 = s.split(',')

		for s2 in subs2:
			print s2.strip()
			out.append({
				'object_id': s2.strip(),
				})

	return out
	'''


	# Filter out some words we don't need
	#in_str = in_str.replace('their ', '').replace('the ', '')

	# Translate words into ones we can parse
	#in_str = in_str.replace(' a ', ' 1 ')
	#print in_str
	return out	

# Parse command-line options
parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help="CSV file to be converted")
parser.add_option("-o", "--output", dest="output", help="Output filename e.g. domain_1_session_1.json")

(options, args) = parser.parse_args()

scene_model = SceneModel()
target_word = ''
target_lang = None

EncodingConverter.convert(options.input)

try:
	csvfile = open(options.input, 'rb')
except:
	print "Problem loading the CSV file -- is the filename correct?"

with csvfile:
	reader = csv.reader(csvfile, delimiter=';')

	tmprow1 = next(reader)
	if len(tmprow1) <= 1:
		reader = csv.reader(csvfile, delimiter=',')
		#next(reader)

	# The JSON document will start with 1 root: the Scenario
	# This will be followed by multiple Task objects, which are segments of the script (introduction, modelling of words etc.)
	# Finally, Subtask objects will contain actual output, interactions and scene changes
	data = {
		'description': options.input[options.input.rfind('/')+1:len(options.input)-4],
		'tasks':  list()
	}

	current_task = None
	task_counter = 1
	current_subtask = None
	subtask_counter = 1
	previous_order = -1
	i = 0
	is_2d = False

	# Read each row and try to convert into XML
	for row in reader:
		txt = ''
		txt_nl = ''
		txt_de = ''
		txt_tk = ''

		#print ''.join(row)

		# Skip the header rows
		if i < 1:
			i += 1
			continue

		# Also skip completely empty rows
		if ''.join(row) == '':
			continue

		# Fix some annoying Excel character usage
		#print row[2]
		if ''.join(row).find("\xfc") > -1:
			print ''.join(row)			
			#row[2] = row[2].replace('\x92', "'")

		if row[3].find("\xe9\xe9n") > -1:
			row[3] = row[3].replace("\xe9\xe9n", '1')

		if row[2].find('\xd5') > -1:
			row[2] = row[2].replace('\xd5', "'")

		if row[2].find('\xca') > -1:
			row[2] = row[2].replace('\xca', '')

		if row[2].find('\x92') > -1:
			row[2] = row[2].replace('\x92', "'")

		if row[2].find('\xa0') > -1:
			row[2] = row[2].replace('\xa0', '')

		#if ''.join(row).find('\x93') > -1:
		#	print ''.join(row)

		# Check if we have a target word
		if row[1].find('targetWord') != -1:
			new_target_word = row[1][row[1].find('(')+1:row[1].rfind(')')]

			if new_target_word != target_word:
				parts = new_target_word.split(',')
				target_word = parts[0].strip()

				if len(parts) > 1:
					target_lang = parts[1].strip()

		elif row[1].find('task_') != -1:
			new_target_word = row[1][row[1].find('_')+1:]

			if new_target_word != target_word:
				target_word = new_target_word
				target_lang = ''

		# Work-around for movement detection :o
		if row[2].find('giveResponseOnMove') != -1:
			row[2] = '<wait(5000)>'

		# Column 3 contains the L1 text or title of a particular segment
		# If it contains brackets [], this means we enter a new task
		criterium = None
		if len(row[2]) > 0 and row[2][0] == '[' and row[2][len(row[2])-1] == ']':
			print "=== new task === " + row[2]
			# Reset some values
			target_word = ''
			target_lang = None
			is_test = False

			if row[2].lower().find('test:') != -1:
				is_test = True
			
			# Start the next Task
			current_task = {
				'task_id': str(task_counter),
				'description': row[2][1:len(row[2])-1],
				'subtasks': list(),
				'is_test': is_test
			}

			# Check for Turkish-Dutch experiment what type of task we're dealing with
			if len(row[1]) > 0:
				parts = row[1].split('_')

				if len(parts) > 1:
					if parts[1].lower() == 'nl':
						current_task['lang'] = 'L2'
					elif parts[1].lower() == 'tk':
						current_task['lang'] = 'L1'
					elif parts[1] == '1':
						current_task['order'] = 1
					elif parts[1] == '2':
						current_task['order'] = 2

			data['tasks'].append(current_task)

			task_counter += 1
			subtask_counter = 1

			print len(data['tasks'])
			
		# Detect exit criteria for SubTask
		elif row[2].find('<wait') != -1:
			criterium = {
				'type': 'RESPONSE_DELAY_CRITERIUM',
				'timeout_ms': row[2][row[2].find('(')+1:row[2].rfind(')')]
			}

			current_subtask['exit_criteria'].append(criterium)

		elif row[2].find('giveResponseToSelectObject') != -1:
			# We now have more complex selectors here that depend on the scene.
			# The interactionmanager will need the actual object ID, whereas output needs this original description
			# for proper feedback and requesting an answer.
			desc = row[2][row[2].find('(')+1:row[2].rfind(')')]

			for_criterium = desc
			for_output = {
                "id": desc, 
                "is_plural": False
			}

			if scene_model.is_loaded:
				if desc.find(' with ') != -1:
					if desc.find(',') != 1:
						parts = desc.split(',')
						for_criterium = ""
						for p in parts:
							if p.find(' with ') != -1:
								for_output = scene_model.get_complex_description(p)
								for_criterium += scene_model.get_id(p)
							else:
								for_criterium += ',' + p
					else:
						for_output = scene_model.get_complex_description(desc)
						for_criterium = scene_model.get_id(desc)
				elif desc.find(',') != -1:
					for_output = scene_model.get_multiple_objects(desc)
				else:
					for_output = scene_model.get_object(desc)

			#print for_output
			print for_criterium

			criterium = {
				'type': 'OBJECT_SELECT_CRITERIUM',
				'object_id': for_criterium
			}

			current_subtask['exit_criteria'].append(criterium)

			# Add it for output manager
			existing_found = False
			for output in current_subtask['outputs']:
				if output['type'] == 'TEXT_OUTPUT':
					output['objective'] = for_output
					existing_found = True

			if not existing_found:
				textoutput = {
					'type': 'TEXT_OUTPUT',
					'objective': for_output
				}

				current_subtask['outputs'].append(textoutput)			


		elif row[2].find('giveResponseToTouch') != -1:
			criterium = {
				'type': 'SENSOR_TOUCH_CRITERIUM',
				'sensor': row[2][row[2].find('(')+1:row[2].rfind(')')].lower()
			}

			current_subtask['exit_criteria'].append(criterium)

			for_output = {
				'type': 'sensor_touch',
				'id': row[2][row[2].find('(')+1:row[2].rfind(')')].lower(),
				'is_plural': False
			}

			# Add it for output manager
			existing_found = False
			for output in current_subtask['outputs']:
				if output['type'] == 'TEXT_OUTPUT':
					output['objective'] = for_output
					existing_found = True

			if not existing_found:
				textoutput = {
					'type': 'TEXT_OUTPUT',
					'objective': for_output
				}

				current_subtask['outputs'].append(textoutput)			


		elif row[2].find('giveResponseOnSpeech') != -1:
			criterium = {
				'type': 'VOICE_ACTIVATION_CRITERIUM',
				'target_word': row[2][row[2].find('(')+1:row[2].rfind(')')],
				'timeout_ms': 5000
			}

			current_subtask['exit_criteria'].append(criterium)

			existing_found = False
			for output in current_subtask['outputs']:
				if output['type'] == 'TEXT_OUTPUT':
					output['objective'] = {
						'id': row[2][row[2].find('(')+1:row[2].rfind(')')],
						'is_plural': False
					}
					existing_found = True

			if not existing_found:
				textoutput = {
					'type': 'TEXT_OUTPUT',
					'objective':  {
						'id': row[2][row[2].find('(')+1:row[2].rfind(')')],
						'is_plural': False
					}
				}

				current_subtask['outputs'].append(textoutput)			


		elif row[2].find('giveResponseToMoveObject') != -1:
			paramstr = row[2][row[2].find('(')+1:row[2].rfind(')')]
			params = paramstr.split(',')

			for_output = {
                "id": params[0].strip(), 
                "is_plural": False,
                "rel": {
                	"target": {
                		"id": params[2].strip(),
                		"is_plural": False
                	},
                	"type": params[1].strip()
                }
			}

			criterium = {
				'type': 'OBJECT_MOVE_CRITERIUM',
				'obj_1': params[0].strip()
			}

			if is_2d:
				criterium['type'] = 'OBJECT_MOVE_CRITERIUM_2D'

			if len(params) >= 3:
				criterium['relationship'] = params[1].strip().replace(' ', '_')
				criterium['obj_2'] = params[2].strip()

			current_subtask['exit_criteria'].append(criterium)

			if len(params) > 3:		
				# Add it for output manager
				existing_found = False
				target_loc = {
					'x': float(params[3].strip()),
					'y': float(params[4].strip()),
					'z': float(params[5].strip())
				}
				for_output['target_location'] = target_loc

			for output in current_subtask['outputs']:
				if output['type'] == 'TEXT_OUTPUT':
					output['objective'] = for_output
					existing_found = True

			if not existing_found:
				textoutput = {
					'type': 'TEXT_OUTPUT',
					'objective': for_output
				}

				current_subtask['outputs'].append(textoutput)			

			# Perform it in the scene model
			if scene_model.is_loaded:
				if criterium['relationship'] == 'in':
					scene_model.move_into(criterium['obj_1'], criterium['obj_2'])

				elif criterium['relationship'] == 'on':
					scene_model.move_onto(criterium['obj_1'], criterium['obj_2'])

				elif criterium['relationship'] == 'next_to':
					scene_model.move_next_to(criterium['obj_1'], criterium['obj_2'])

		elif row[2].find('giveResponseToObjectCollide') != -1:
			paramstr = row[2][row[2].find('(')+1:row[2].rfind(')')]
			params = paramstr.split(',')

			#print params
			for_output = {
                "id": params[0].strip(), 
                "is_plural": False,
                "rel": {
                	"target": {
                		"id": params[1].strip(),
                		"is_plural": False
                	},
                	"type": 'collision'
                }
			}			

			criterium = {
				'type': 'OBJECT_COLLISION_CRITERIUM',
				'obj_1': params[0].strip(),
				'obj_2': params[1].strip()
			}

		
			current_subtask['exit_criteria'].append(criterium)
			for_output['disappear'] = True

			if len(params) > 2:
				# Add it for output manager
				existing_found = False
				target_loc = {
					'x': float(params[2].strip()),
					'y': float(params[3].strip()),
					'z': float(params[4].strip())
				}
				for_output['target_location'] = target_loc

			if len(params) > 5:
				if params[5].lower().strip() == 'false':
					for_output['disappear'] = False
				else:
					for_output['disappear'] = True

			for output in current_subtask['outputs']:
				if output['type'] == 'TEXT_OUTPUT':
					output['objective'] = for_output
					existing_found = True

			if not existing_found:
				textoutput = {
					'type': 'TEXT_OUTPUT',
					'objective': for_output
				}

				current_subtask['outputs'].append(textoutput)			

		# No exit criteria found, it must be an output.
		# If the current order field (row[0]) is different from the previous one,
		# we should start a new Subtask
		elif len(row[2]) > 0 or len(row[6]) > 0 or len(row[3]) > 0 or len(row[4]) > 0 or len(row[5]) > 0:	
			txt = row[2]
			txt_nl = row[3]
			txt_de = row[4]
			txt_tk = row[5]

		if len(row[6]) > 0:
			if len(txt) > 0 and txt[len(txt)-1] != ' ':
			  txt += ' '
			txt += '{' + row[6] + '}'

			if len(txt_nl) > 0 and txt_nl[len(txt_nl)-1] != ' ':
			  txt_nl += ' '
			txt_nl += '{' + row[6] + '}'

			if len(txt_de) > 0 and txt_de[len(txt_de)-1] != ' ':
			  txt_de += ' '
			txt_de += '{' + row[6] + '}'

			if len(txt_tk) > 0 and txt_tk[len(txt_tk)-1] != ' ':
			  txt_tk += ' '
			txt_tk += '{' + row[6] + '}'


		if len(row[9]) > 0 or len(row[8]) > 0 or len(row[7]) > 0 or txt != '' or txt_nl != '' or txt_de != '' or txt_tk != '':
			try:
				this_order = int(row[0])

				if this_order != previous_order:
					# If the previous subtask had no exit criteria, it should be an OutputFinishCriterium
					if current_subtask != None and len(current_subtask['exit_criteria']) == 0:
						criterium = {
							'type': 'OUTPUT_FINISH_CRITERIUM'
						}

						current_subtask['exit_criteria'].append(criterium)
						#criterium = ET.SubElement(current_subtask.find('ExitCriteria'), 'OutputFinishCriterium')

					current_subtask = {
						'subtask_id': str(subtask_counter),
						'outputs': list(),
						'exit_criteria': list()
					}

					if target_word != '':
						current_subtask['target_word'] = {
							'target_word': target_word
						}

						if target_lang == None:
							if len(row[6]) > 0:
								target_lang = 'L1'
							else:
								target_lang = 'L2'

						current_subtask['target_word']['lang'] = target_lang


					current_task['subtasks'].append(current_subtask)

					subtask_counter += 1
					previous_order = this_order
			except:
				pass
			
			# If text output already exists, we should append to that instead of adding another.
			existing_found = False
			for output in current_subtask['outputs']:
				if output['type'] == 'TEXT_OUTPUT':
					output['text']['English'] += ' ' + txt
					output['text']['Dutch'] += ' ' + txt_nl
					output['text']['German'] += ' ' + txt_de
					output['text']['Turkish'] += ' ' + txt_tk
					existing_found = True

			if not existing_found:
				textoutput = {
					'type': 'TEXT_OUTPUT',
					'text': {
						'English': txt,
						'Dutch': txt_nl,
						'German': txt_de,
						'Turkish': txt_tk
					}
				}

				current_subtask['outputs'].append(textoutput)			

		# Tablet output
		# These are a bit tricky, as some of them (displaying things) should be sent to the tablet directly,
		# while others (sounds) should be listed as outputs 

		# row[7] is a scene change
		if len(row[7]) > 0:
			if 'tablet_display_actions' in current_subtask:
				current_subtask['tablet_display_actions']['scene'] = row[7]
			else:				
				current_subtask['tablet_display_actions'] = {
					'scene': row[7]
				}

			if row[7].lower().strip() == 'town' or row[7].lower().strip() == 'recap':
				is_2d = True

			else:
				is_2d = False
				scene_model.load_scene(row[7])

		# row[8] is a change in the displayed scene
		if len(row[8]) > 0:	
			to_add = ''
			to_remove = ''
			to_enable = ''
			to_highlight = ''
			to_move = ''
			to_animate = ''

			items = list()
 			items += [m.start() for m in re.finditer(r'\bdisplay\b', row[8])]
 			items += [m.start() for m in re.finditer(r'\bremove\b', row[8])]
 			items += [m.start() for m in re.finditer(r'\benable\b', row[8])]
 			items += [m.start() for m in re.finditer(r'\bhighlight\b', row[8])]
 			items += [m.start() for m in re.finditer(r'\bmove\b', row[8])]
 			items += [m.start() for m in re.finditer(r'\banimate\b', row[8])]

 			items = sorted(items)

 			for idx, it in enumerate(items):
 				# If there is a next item, get the area in between
 				if (idx+1) < len(items):
 					scene_str = row[8][it:items[idx+1]]#.lower()
 				# Else get everything until the end
 				else:
 					scene_str = row[8][it:]#.lower()

 				print "===-- " + scene_str

 				if scene_str.startswith('display'):
 					to_add = scene_str[8:]
 				elif scene_str.startswith('remove'):
 					to_remove = scene_str[7:]
 				elif scene_str.startswith('enable'):
 					to_enable = scene_str[7:]
 				elif scene_str.startswith('highlight'):
 					to_highlight = scene_str[10:]
 				elif scene_str.startswith('move'):
 					to_move = scene_str[5:]
 				elif scene_str.startswith('animate'):
 					to_animate = scene_str[8:]

			# Split objects where needed
			if to_add != '':
				parsed = parse_tablet_objects(to_add)

				if 'tablet_display_actions' in current_subtask:
					current_subtask['tablet_display_actions']['objects_added'] = parsed
				else:
					current_subtask['tablet_display_actions'] = {
						'objects_added': parsed
					}

				if scene_model.is_loaded:
					for p in parsed:
						scene_model.show_object(p['object_id'])



			if to_remove != '':
				if to_remove.startswith('highlights'):
					if 'tablet_display_actions' in current_subtask:
						current_subtask['tablet_display_actions']['remove_highlights'] = []
					else:
						current_subtask['tablet_display_actions'] = {
							'remove_highlights': []
						}

				else:
					parsed = parse_tablet_objects(to_remove)

					if 'tablet_display_actions' in current_subtask:
						current_subtask['tablet_display_actions']['objects_removed'] = parsed
					else:
						current_subtask['tablet_display_actions'] = {
							'objects_removed': parsed
						}

					if scene_model.is_loaded:
						for p in parsed:
							scene_model.hide_object(p['object_id'])

			if to_enable != '':
				if 'tablet_display_actions' in current_subtask:
					current_subtask['tablet_display_actions']['objects_enabled'] = parse_tablet_objects(to_enable)
				else:
					current_subtask['tablet_display_actions'] = {
						'objects_enabled': parse_tablet_objects(to_enable)
					}				

			if to_highlight != '':
				if 'tablet_display_actions' in current_subtask:
					current_subtask['tablet_display_actions']['objects_highlighted'] = parse_tablet_objects(to_highlight)
				else:
					current_subtask['tablet_display_actions'] = {
						'objects_highlighted': parse_tablet_objects(to_highlight)
					}		

			if to_move != '':
				if 'tablet_display_actions' in current_subtask:
					current_subtask['tablet_display_actions']['objects_move'] = parse_tablet_objects(to_move)
				else:
					current_subtask['tablet_display_actions'] = {
						'objects_move': parse_tablet_objects(to_move)
					}

			if to_animate != '':
				if 'tablet_display_actions' in current_subtask:
					current_subtask['tablet_display_actions']['objects_animated'] = parse_tablet_objects(to_animate)
				else:
					current_subtask['tablet_display_actions'] = {
						'objects_animated': parse_tablet_objects(to_animate)
					}
		i += 1

		# row[9] has tablet speech, this also should go to the outputmanager
		if len(row[9]) > 0:			
			'''current_subtask = {
				'subtask_id': str(subtask_counter),
				'outputs': list(),
				'exit_criteria': list()
			}

			current_task['subtasks'].append(current_subtask)

			subtask_counter += 1'''
			
			current_subtask['outputs'].append({
				'type': 'TABLET_SPEECH_OUTPUT',
				'text': row[9]
			})

	# If we didn't have a criterium at the end, we need one last OUTPUT_FINISHED
	if current_subtask != None and len(current_subtask['exit_criteria']) == 0:
		criterium = {
			'type': 'OUTPUT_FINISH_CRITERIUM'
		}

		current_subtask['exit_criteria'].append(criterium)

	# Done going through the CSV file, time to save our generated JSON
	with open('../generated/full_scenario.json', 'w') as savefile:
		savefile.write(json.dumps(data, indent=4, sort_keys=True))

	# Generate the files for interactionmanager and outputmanager	
	outputmanager_data = {}
	interactionmanager_data = copy.deepcopy(data)

	for d in interactionmanager_data['tasks']:
		taskid = d['task_id']

		for s in d['subtasks']:
			subtaskid = s['subtask_id']

			if len(s['outputs']) == 0:
				s['has_output'] = False
			else:
				s['has_output'] = True
				outputmanager_data[taskid.zfill(3) + ':' + subtaskid.zfill(3)] = s['outputs']
				del s['outputs']


	#print json.dumps(interactionmanager_data, indent=4, sort_keys=True)
	#print json.dumps(outputmanager_data, indent=4, sort_keys=True)
	if options.output.rfind('.json') == -1:
		options.output += '.json'

	with open('../sessions/interactionmanager/' + options.output, 'w') as savefile:
		savefile.write(json.dumps(interactionmanager_data, indent=4, sort_keys=True))

	with open('../sessions/outputmanager/' + options.output, 'w') as savefile:
		savefile.write(json.dumps(outputmanager_data, indent=4, sort_keys=True))


	# @TODO: generate different files for all the modules (e.g. OutputManager only has Output tags with no flow, interaction manager only knows there is output but not exactly what)
