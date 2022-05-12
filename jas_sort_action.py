import pcbnew, re, os, math

class JasSort(pcbnew.ActionPlugin):
	groups = []
	_refnrs = {}	# ref : nr

	def defaults(self):
		if not "__file__" in locals() and not "__file__" in globals():
			return
		self.name = "JasSort"
		self.category = "Sorting"
		self.description = "Generates new component referenced grouped by type, footprint, and value. And sorts them left to right. Note that you need to run 'Tools > Update Schematic from PCB' when done."
		self.show_toolbar_button = True
		self.icon_file_name = os.path.join(os.path.dirname(__file__), 'JasSort.png') # Optional, defaults to ""

	def Run(self):
		self.groups = []
		footprints = pcbnew.GetBoard().GetFootprints()
		for footprint in footprints:
			self.add(footprint)
		self.sort()
		self.write()
		#self.print()
		pcbnew.Refresh()

	def add(self, footprint):
		# Get ref like C or R with no number
		start = re.search("[\?0-9]", footprint.GetReference())
		ref = "UNKNOWN"
		if start:
			ref = footprint.GetReference()[0:start.start()]
		else:
			ref = "UNKNOWN"
		# Get footprint name
		ident = footprint.GetFPID().GetUniStringLibItemName()
		# Get value
		value = footprint.GetValue()
		group = self.getGroup(ref, ident, value)
		if not group:
			group = FpGroup(ref, ident, value)
			self.groups.append(group)
		group.add(footprint)
	
	def print(self):
		for group in self.groups:
			print(group.ident, group.value, ":", len(group.footprints))

	# Get the furthest top and furthest left components, returns xy tuple
	def getTopLeft(self):
		x = -1
		y = -1
		for group in self.groups:
			xy = group.getTopLeft()
			if x == -1 or xy[0] < x:
				x = xy[0]
			if y == -1 or xy[1] < y:
				y = xy[1]
		return (x, y)

	def sort(self):
		# First sort groups based on the top-left most component
		tl = self.getTopLeft()
		self.groups = sorted(self.groups, key = lambda x: (x.getTopLeftDist(tl)))
		for group in self.groups:
			group.sort()

	# Gets a group by ref, ident, and value
	def getGroup(self, ref, ident, value):
		for group in self.groups:
			if group.ref == ref and group.ident == ident and group.value == value:
				return group

	# Writes changes to board
	def write(self):
		self._refnrs = {}
		for group in self.groups:
			ref = group.ref		# Get reference label like Q or R or C
			# Create new index if it doesn't exist
			if not ref in self._refnrs:
				self._refnrs[ref] = 1
			start = self._refnrs[ref]
			group.write(start)
			self._refnrs[ref] += len(group.footprints)

class FpGroup:
	def __init__(self, ref, ident, value):
		self.ref = ref
		self.ident = ident		# Footprint ex R_0603_1608Metric
		self.value = value		# Value ex 100k
		self.footprints = []	# Items to be sorted

	# Gets the coordinates for the topmost and leftmost component(s)
	def getTopLeft(self):
		x = -1
		y = -1
		for footprint in self.footprints:
			xy = footprint.GetPosition();
			if x == -1 or xy[0] < x:
				x = xy[0]
			if y == -1 or xy[1] < y:
				y = xy[1]
		return (x,y)
	
	# Gets the shortest distance to top left, assuming top left is reference (xy tuple)
	def getTopLeftDist(self, reference):
		out = -1
		for footprint in self.footprints:
			pos = footprint.GetPosition()
			dist = math.sqrt(
				((pos[0]-reference[0])**2) + 
				((pos[1]-reference[1])**2)
			)
			if out == -1 or dist < out:
				out = dist
		#print(self.ref, self.value, round(out/10000))
		return out


	def add(self, footprint):
		self.footprints.append(footprint)

	# Sorts from left to right. Could sort better later
	def sort(self):
		self.footprints = sorted(self.footprints, key = lambda x: (x.GetPosition()[0], x.GetPosition()[1]))

	# Writes footprints
	def write(self, start):
		for footprint in self.footprints:
			ref = self.ref+str(start)
			footprint.SetReference(ref)
			start += 1
	
sorter = ""
# This is run directly, not through import
if __name__ == "__main__":
	JasSort().Run()


