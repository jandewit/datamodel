import json
import os.path

class SceneModel:
	def __init__(self):
		self.is_loaded = False
		
	def _copy_properties(self, json_obj, target_obj):
		target_obj['id'] = json_obj['id'].split('_', 1)[1].split('?')[0]
		target_obj['is_visible'] = json_obj['visible']
		target_obj['is_static'] = json_obj['id'][0] == 's'
		target_obj['position'] = json_obj['position']

		# Defaults
		target_obj['can_contain'] = False
		target_obj['relations'] = list()

		# Flat planes can contain objects
		if 'type' in json_obj and ((json_obj['type'] == 'plane' and json_obj['rotation']['x'] == 90 and json_obj['scaling']['z'] == 1) or (json_obj['type'] == 'cylinder' and json_obj['scaling']['y'] <= 1)) and json_obj['position']['y'] <= 1:
			del target_obj['position']

			#if json_obj['type'] == 'cylinder':
			#	width = json_obj['size']['diameter'] / 2
			#	height = json_obj['size']['diameter'] / 2
			#else:
			#	width = json_obj['size']['width'] / 2
			#	height = json_obj['size']['height'] / 2
			multiplier = 50
			if json_obj['type'] == 'cylinder':
				multiplier = 5

			width = json_obj['scaling']['x'] * multiplier
			if json_obj['rotation']['x'] == 90:
				height = json_obj['scaling']['y'] * multiplier
			else:
				height = json_obj['scaling']['z'] * multiplier

			target_obj['is_ground'] = True
			print "ground " + json_obj['id']
			target_obj['bounding_box'] = {}
			target_obj['bounding_box']['left'] = json_obj['position']['x'] - width
			target_obj['bounding_box']['right'] = json_obj['position']['x'] + width
			target_obj['bounding_box']['top'] = json_obj['position']['z'] + height
			target_obj['bounding_box']['bottom'] = json_obj['position']['z'] - height

		else:
			target_obj['is_ground'] = False

		# Type of object
		tmp = json_obj['id'].split('_')
		target_obj['types'] = []
		target_obj['types'].append(tmp[1])

		return target_obj


	def load_scene(self, scene_name):
		try:
			with open(os.path.join(os.path.dirname(__file__), '../tablet_scenes/' + scene_name + '.json')) as infile:
				scene_json = json.load(infile)

			self.scene = {}
			self.scene['objects'] = {}

			total_objs = scene_json['loadable_objects'] + scene_json['creatable_objects']

			for lo in total_objs:
				obj = {}

				# Check whether this is part of a bigger object
				if lo['id'].find('?') != -1:
					obj = self._copy_properties(lo, obj)

					if obj['id'] not in self.scene['objects']:
						# If it's part of a Box3D, it can contain other objects so we need a bounding box
						if lo['id'].find('box3d') != None:
							obj['can_contain'] = True
							del obj['position']

							# We can only estimate the size of the bounding box because the scale doesn't say much
							obj['bounding_box'] = {}
							obj['bounding_box']['left'] = lo['position']['x']
							obj['bounding_box']['right'] = lo['position']['x']
							obj['bounding_box']['top'] = lo['position']['z']
							obj['bounding_box']['bottom'] = lo['position']['z']

						self.scene['objects'][obj['id']] = obj

					else:
						existing_obj = self.scene['objects'][obj['id']]
						if lo['position']['x'] > existing_obj['bounding_box']['right']:
							existing_obj['bounding_box']['right'] = lo['position']['x']
						elif lo['position']['x'] < existing_obj['bounding_box']['left']:
							existing_obj['bounding_box']['left'] = lo['position']['x']

						if lo['position']['z'] > existing_obj['bounding_box']['top']:
							existing_obj['bounding_box']['top'] = lo['position']['z']
						elif lo['position']['z'] < existing_obj['bounding_box']['bottom']:
							existing_obj['bounding_box']['bottom'] = lo['position']['z']

		
				else:
					# Simply copy some of its properties as defined in JSON (the ones we may need)
					obj = self._copy_properties(lo, obj)
					self.scene['objects'][obj['id']] = obj


			# Prefill existing relations (for now only 'contains' and 'on', other unique identifiers might be needed later for multiple objects of same type, referring expressions)
			for o in self.scene['objects']:
				so = self.scene['objects'][o]

				if so['can_contain']:
					for o2 in self.scene['objects']:
						so2 = self.scene['objects'][o2]

						if 'position' in so2:
							if so2['position']['x'] > so['bounding_box']['left'] and so2['position']['x'] < so['bounding_box']['right'] and so2['position']['z'] < so['bounding_box']['top'] and so2['position']['z'] > so['bounding_box']['bottom']:
								#print "Found object within another object: " + so2['id'] + ' inside ' + so['id']
								so['relations'].append({
									'type': 'contains',
									'id': so2['id'],
									'object_types': so2['types']
								})

								so2['relations'].append({
									'type': 'in',
									'id': so['id'],
									'object_types': so['types']
								})

				if so['is_ground']:
					for o2 in self.scene['objects']:
						so2 = self.scene['objects'][o2]

						if not so2['is_ground'] and 'position' in so2:
							if so2['position']['x'] > so['bounding_box']['left'] and so2['position']['x'] < so['bounding_box']['right'] and so2['position']['z'] < so['bounding_box']['top'] and so2['position']['z'] > so['bounding_box']['bottom']:						
								so['relations'].append({
									'type': 'below',
									'id': so2['id'],
									'object_types': so2['types']
								})

								so2['relations'].append({
									'type': 'on',
									'id': so['id'],
									'object_types': so['types']	
								})					

			#print json.dumps(self.scene, indent=4, sort_keys=True)
			self.is_loaded = True
		except Exception as ex:
			print "exception: " + ex.message
			self.scene = None

	def _remove_existing_child_relations(self, obj_id):
		obj = self.scene['objects'][obj_id]

		for j in xrange(len(obj['relations']) - 1, -1, -1):
			r = obj['relations'][j]

			if r['type'] == 'on':
				# Find matching parent
				for i in xrange(len(self.scene['objects'][r['id']]['relations']) - 1, -1, -1):
					r2 = self.scene['objects'][r['id']]['relations'][i]

					if r2['type'] == 'below' and r2['id'] == obj_id:
						del self.scene['objects'][r['id']]['relations'][i]

			elif r['type'] == 'in':
				# Find matching parent
				for i in xrange(len(self.scene['objects'][r['id']]['relations']) - 1, -1, -1):
					r2 = self.scene['objects'][r['id']]['relations'][i]

					if r2['type'] == 'contains' and r2['id'] == obj_id:
						del self.scene['objects'][r['id']]['relations'][i]

			elif r['type'] == 'next_to':
				# Find matching parent
				for i in xrange(len(self.scene['objects'][r['id']]['relations']) - 1, -1, -1):
					r2 = self.scene['objects'][r['id']]['relations'][i]

					if r2['type'] == 'having_next_to' and r2['id'] == obj_id:
						del self.scene['objects'][r['id']]['relations'][i]

			del obj['relations'][j]

	def _add_relation(self, obj, target, rel_obj, rel_target):
		to_add = obj

		# Check if the object itself actually exists. If not, find the first one of the type that is not yet added.
		if not obj in self.scene['objects']:
			for o in self.scene['objects']:				
				so = self.scene['objects'][o]

				if obj in so['types'] and not so['is_static']:
					already_there = False

					for r in so['relations']:
						if r['type'] == rel_obj and r['id'] == target:
							already_there = True
							print "already there"

					if not already_there:
						print "hai " + so['id']						
						to_add = so['id']
						so['is_static'] = True
						'Found one, adding.. ' + to_add
						break


		self._remove_existing_child_relations(to_add)

		self.scene['objects'][target]['relations'].append({
				'type': rel_target,
				'id': to_add,
				'object_types': self.scene['objects'][to_add]['types']
			})

		self.scene['objects'][to_add]['relations'].append({
				'type': rel_obj,
				'id': target,
				'object_types': self.scene['objects'][target]['types']
			})


	def move_into(self, obj, container):
		print container
		if self.scene['objects'][container]['is_ground']:
			self.move_onto(obj, container)
		else:
			print "Moving " + obj + " into " + container
			self._add_relation(obj, container, 'in', 'contains')

		#print json.dumps(self.scene, indent=4, sort_keys=True)		
		#raw_input('...')	


	def move_onto(self, obj, surface):
		print "Moving " + obj + " onto " + surface
		self._add_relation(obj, surface, 'on', 'below')

		#print json.dumps(self.scene, indent=4, sort_keys=True)		
		#raw_input('...')	

	def move_next_to(self, obj, target):
		print "Moving " + obj + " next to " + target
		self._add_relation(obj, target, 'next_to', 'having_next_to')

		#print json.dumps(self.scene, indent=4, sort_keys=True)		
		#raw_input('...')	

	# @TODO: move out of, away from stuff

	def show_object(self, obj):
		print "Showing object: " + obj
		if self.scene != None and obj in self.scene['objects']:
			self.scene['objects'][obj]['is_visible'] = True

	def hide_object(self, obj):
		print "Hiding object: " + obj
		if self.scene != None and obj in self.scene['objects']:
			self.scene['objects'][obj]['is_visible'] = False		

	def _is_parent(self, r):
		return r['type'] == 'contains' or r['type'] == 'having_next_to' or r['type'] == 'below'

	def _get_with(self, area_type, object_type):
		print "getting " + area_type + " with " + object_type
		found_area = False
		found_object_type = False

		found = list()
		
		found_number = 0
		found_id = None

		for o in self.scene['objects']:
			so = self.scene['objects'][o]

			if so['is_visible'] and area_type in so['types']:
				found_area = True
				num_r = 0

				for r in so['relations']:
					if self.scene['objects'][r['id']]['is_visible'] and object_type in r['object_types']:
						found_object_type = True
						num_r += 1

				found.append({
					'id': so['id'],
					'number': num_r,
					'types': so['types']
					})

		if not found_area:
			print "Couldn't find area type " + area_type

			for o in self.scene['objects']:
				so = self.scene['objects'][o]

				if so['is_visible']:
					num_r = 0

					for r in so['relations']:
						if self.scene['objects'][r['id']]['is_visible'] and object_type in r['object_types']:
							found_object_type = True
							num_r += 1

					found.append({
						'id': so['id'],
						'number': num_r,
						'types': so['types']
						})

		elif not found_object_type:
			print "Couldn't find object type " + object_type
			for o in self.scene['objects']:
				so = self.scene['objects'][o]

				if so['is_visible'] and area_type in so['types']:
					num_r = 0

					for r in so['relations']:
						if self.scene['objects'][r['id']]['is_visible'] and self._is_parent(r):
							num_r += 1

					found.append({
						'id': so['id'],
						'number': num_r,
						'types': so['types']
						})


		# If we cannot find either, we assume all containers/surfaces are area and all contained items are included
		elif not found_area and not found_object_type:
			for o in self.scene['objects']:
				so = self.scene['objects'][o]

				if so['is_visible']:
					num_r = 0

					for r in so['relations']:
						if self.scene['objects'][r['id']]['is_visible'] and self._is_parent(r):
							num_r += 1

					found.append({
						'id': so['id'],
						'number': num_r,
						'types': so['types']
						})


		return found

	# For now, 'with' counts as all types of spatial relations.. see if that works in all cases :)
	def get_with_most(self, area_type, object_type, opts = None):
		found = self._get_with(area_type, object_type)
		found_number = 0
		found_id = None

		for f in found:
			if (opts == None or self._check_match_options(opts, f)) and f['number'] > found_number:
				found_number = f['number']
				found_id = f['id']

		if found_id == None:
			print "Could not find " + area_type + " with " + object_type
		else:
			print "Most " + object_type + " found in " + found_id

		return found_id


	def get_with_least(self, area_type, object_type, opts = None):
		found = self._get_with(area_type, object_type)
		found_number = 1000
		found_id = None

		for f in found:
			if (opts == None or self._check_match_options(opts, f)) and f['number'] < found_number:
				found_number = f['number']
				found_id = f['id']

		if found_id == None:
			print "Could not find " + area_type + " with " + object_type
		else:
			print "Least " + object_type + " found in " + found_id

		return found_id

	def get_with_exactly(self, area_type, object_type, amount, opts = None):
		found = self._get_with(area_type, object_type)

		for f in found:
			if (opts == None or self._check_match_options(opts, f)) and int(f['number']) == int(amount):
				return f['id']

		return None

	# @TODO: highest object, biggest object, lowest object etc?

	def _check_match_options(self, opts, obj):
		if obj['id'] in opts:
			return True

		for t in obj['types']:
			if t in opts:
				print "=== MATCH: " + t
				return True


		return False

	def _is_plural(self, obj_id):
		if self.scene == None:
			return False # Town map..

		if obj_id in self.scene['objects']:
			return False
		else:
			return True		

	def get_object(self, target_str):
		return {
			'id': target_str,
			'is_plural': self._is_plural(target_str)
		}

	def get_multiple_objects(self, target_str):
		parts = target_str.split(',')
		print "=== multiple "

		p1 = parts[0].strip()
		p2 = parts[1].strip()

		obj1 = {
			'id': p1
		}
		obj2 = {
			'id': p2
		}

		# Only 1 object?
		if p1 in self.scene['objects']:			
			obj1['is_plural'] = False
			found = self.scene['objects'][p1]

		else:
			for p in self.scene['objects']:
				if p.find(p1) != -1:
					obj1['is_plural'] = True
					found = self.scene['objects'][p]
					break

		for r in found['relations']:
			if r['id'] == p2 or r['id'].find(p2) != -1:
				if r['id'] == p2:
					obj2['is_plural'] = False
				else:
					obj2['is_plural'] = True

				rel = {}

				if r['type'] == 'contains' or r['type'] == 'in':
					rel['type'] = 'in'
				elif r['type'] == 'having_next_to' or r['type'] == 'next_to':
					rel['type'] = 'next_to'
				elif r['type'] == 'below' or r['type'] == 'on':
					rel['type'] = 'on'
				
				if self._is_parent(r):
					rel['target'] = obj1
					obj2['rel'] = rel
					return obj2
				else:
					rel['target'] = obj2
					obj1['rel'] = rel
					return obj1

		# No relation found, probably or
		if p2 in self.scene['objects']:			
			obj2['is_plural'] = False					

		else:
			for p in self.scene['objects']:
				if p.find(p2) != -1:
					obj2['is_plural'] = True
					break

		# For now we don't want to use the "or" relationship in request_answer, leaving it out..
		#obj1['rel'] = {
		#	'target': obj2,
		#	'type': 'or'
		#}

		return obj1

	def get_complex_description(self, target_str):
		command = target_str.split(' with ')

		command = target_str.split(' with ')
		rest = command[1].split(' ')

		opts = None

		opt = command[1].split(':')

		if len(opt) > 1:
			opts = opt[1].strip().split(' or ')
			rest = opt[0].split(' ')

		rest0 = rest[0]
		if rest[0].isdigit():
			rest[0] = rest[0].replace(rest[0], self._int2words(rest[0]))

		obj = {
			'id': command[0],
			'is_plural': False,
			'rel': {
				'type': ' '.join(rest[:-1]),
				'target': {
					'id': self._find_and_remove_plural(rest[-1]),
					'is_plural': True
				}
			}
		}

		if rest0.isdigit() and int(rest0) <= 1:
			obj['rel']['target']['is_plural'] = False

		if opts != None:
			obj['opts'] = list()

			# Figure out what kind of spatial relations we have with these options
			for opt in opts:
				matching_obj = self._get_obj(opt)

				if matching_obj != None:
					for r in matching_obj['relations']:
						if r['type'] == 'having_next_to' or r['type'] == 'contains' or r['type'] == 'below':
							obj['opts'].append({
								'type': r['type'],
								'id': opt
								})			
							
							break

		return obj

	def _get_obj(self, obj_id):
		# Can be ID or type
		if obj_id in self.scene['objects']:
			return self.scene['objects'][obj_id]

		for o in self.scene['objects']:
			if obj_id in self.scene['objects'][o]['types']:
				return self.scene['objects'][o]

		return None


	def _find_and_remove_plural(self, obj_type):
		# Remove plural if needed
		if obj_type[-1] == 's':
			return obj_type[:-1]

		return obj_type

	def get_id(self, target_str):
		command = target_str.split(' with ')
		rest = command[1].split(' ')

		opts = None

		opt = command[1].split(':')

		if len(opt) > 1:
			opts = opt[1].strip().split(' or ')
			rest = opt[0].split(' ')

		# Figure out what to look for
		for r in rest:			
			if r == 'most' or r == 'more':
				return self.get_with_most(command[0], self._find_and_remove_plural(rest[-1]), opts)
			elif r == 'least' or r == 'less':
				return self.get_with_least(command[0], self._find_and_remove_plural(rest[-1]), opts)
			elif r.isdigit():
				if int(r) > 1:
					return self.get_with_exactly(command[0], self._find_and_remove_plural(rest[-1]), r, opts)
				else:
					return self.get_with_exactly(command[0], rest[-1], r, opts)
				# @TODO: between 2 objects compare		

		return None

	def _int2words(self, num):	
		"""Given an int32 number, print it in English.

		Parameters
		----------
		num : int

		Returns
		-------
		words : str
		"""
		num = int(num)
		assert (0 <= num)
		d = {
			0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
			6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
			11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
			15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
			19: 'nineteen', 20: 'twenty',
			30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty',
			70: 'seventy', 80: 'eighty', 90: 'ninety'
		}

		h = [100, 'hundred', 'hundred and']
		k = [h[0] * 10, 'thousand', 'thousand,']
		m = [k[0] * 1000, 'million', 'million,']
		b = [m[0] * 1000, 'billion', 'billion,']
		t = [b[0] * 1000, 'trillion', 'trillion,']
		
		if num < 20:
			return d[num]
		if num < 100:
			div_, mod_ = divmod(num, 10)
			return d[num] if mod_ == 0 else d[div_ * 10] + '-' + d[mod_]
		else:
			if num < k[0]:
				divisor, word1, word2 = h
			elif num < m[0]:
				divisor, word1, word2 = k
			elif num < b[0]:
				divisor, word1, word2 = m
			elif num < t[0]:
				divisor, word1, word2 = b
			else:
				divisor, word1, word2 = t
			
			div_, mod_ = divmod(num, divisor)
			if mod_ == 0:
				return '{} {}'.format(int2words(div_), word1)
			else:
				return '{} {} {}'.format(int2words(div_), word2, int2words(mod_))	