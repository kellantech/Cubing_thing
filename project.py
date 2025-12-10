vmoves = ["U","L","B","R","F","D","U'","L'","B'","R'","F'","D'","U2","L2","B2","R2","F2","D2"]

def _disp_cubestate(cube):
	u_str = f"""{cube.U_corners[1]}{cube.U_edges[1]}{cube.U_corners[2]}\n{cube.U_edges[0]} (U) {cube.U_edges[2]}\n{cube.U_corners[0]}{cube.U_edges[3]}{cube.U_corners[3]}\n"""
	
	s_str = f"{cube.slice[1]}{cube.slice[0]}{cube.slice[3]}{cube.slice[2]}\n"
	
	d_str = f"""{cube.D_corners[0]}{cube.D_edges[3]}{cube.D_corners[3]}\n{cube.D_edges[0]} (D) {cube.D_edges[2]}\n{cube.D_corners[1]}{cube.D_edges[1]}{cube.D_corners[2]}\n"""

	return '--------------\n' + u_str + '\n' + s_str + '\n' + d_str + '--------------'


class edge:
	def __init__(self,F,R,ori):
		self.ident = {F,R}
		self.ori = ori # 0 is good
	def flip(self):
		self.ori = (self.ori + 1) % 2
	def __str__(self):
		return "(" + ''.join(self.ident) + self.ori * "x" + ')' 
	def __repr__(self): return self.__str__()
		

class corner:
	def __init__(self,U,R,F,ori):
		self.ident = {F,R,U}
		self.ori = ori # 0 --> U/D 1--> F/B, 2 --> R/L
	def __str__(self):
		return "(" + ''.join(self.ident) + self.ori * "x" + ')' 
	def flip(self, n=1):
		self.ori = (self.ori + n) % 3


colors = ["U","L","B","R","F","D"]



class cubestate:
	def __init__(self):
		
		self.U_edges = [edge('U',s,0) for s in colors[1:-1]]
		self.D_edges = [edge('D',s,0) for s in colors[1:-1]]
		self.slice = [edge(*list(c),0) for c in ['LF','LB','RB','RF']]
		self.U_corners = [corner('U',*list(s),0) for s in ['LF','LB','RB','RF'] ]  
		self.D_corners = [corner('D',*list(s),0) for s in ['LF','LB','RB','RF'] ]
		
	def __str__(self): return _disp_cubestate(self)
	def __repr__(self): return __str__(self)
	
	
	def parse(self, moves):
		move_map = {"F": self.F, "U": self.U, "D": self.D, "B": self.B, "R": self.R, "L": self.L,
			    "F'":self.Fp, "U'": self.Up, "D'": self.Dp, "B'": self.Bp, "R'": self.Rp, "L'": self.Lp,
			    "F2": self.F2, "U2": self.U2, "D2": self.D2, "B2": self.B2, "R2": self.R2, "L2": self.L2 }
		for m in moves.split(' '):
			if m == '': continue
			if m in move_map.keys(): move_map[m]()
			else: raise ValueError(f"Invalid Move: {m}")

	def eo_repr(self):
		sum = 0
		i = 0
		for e in self.U_edges+self.D_edges+self.slice:
			sum += (2**i) * e.ori
			i+=1
		return sum
	def drm_e(self):
		be = 8
		for u in self.U_edges + self.D_edges:
			if 'U' in u.ident or 'D' in u.ident: be -= 1
		return be
	def drm_c(self):
		bc = 0
		for c in self.U_corners + self.D_corners:
			if c.ori != 0: bc += 1
		return bc
	def drm(self): return (self.drm_e(), self.drm_c())
	def D(self): # :(
		temp = self.D_edges[0]
		self.D_edges = self.D_edges[1:] + [temp]
		
		tempc = self.D_corners[0]
		self.D_corners = self.D_corners[1:] + [tempc]
	def D2(self): self.D(); self.D()
	def Dp(self): self.D(); self.D(); self.D()

	def U(self): # :) 
		temp = self.U_edges[-1]
		self.U_edges = [temp] + self.U_edges[:-1]
	
		tempc = self.U_corners[-1]
		self.U_corners = [tempc] + self.U_corners[:-1]
	def U2(self): self.U(); self.U()
	def Up(self): self.U(); self.U(); self.U()		


	def F(self): 
		# UF Ue[1] --> RF S[3] --> DF De[1] ---> LF S[0]
		# UFL Uc[0] --> UFR Uc[3]--> DFR Dc[3] --> DFL Dc[0]

		UF = self.U_edges[3]
		RF = self.slice[3]
		DF = self.D_edges[3]
		LF = self.slice[0]
		
		UFL = self.U_corners[0]
		UFR = self.U_corners[3]
		DFR = self.D_corners[3]
		DFL = self.D_corners[0]

		UFL.flip(1)
		UFR.flip(2)
		DFL.flip(2)
		DFR.flip(1)


		UF.flip()
		RF.flip()
		DF.flip()
		LF.flip()	
		
		self.U_edges[3] = LF
		self.slice[0] = DF
		self.D_edges[3] = RF
		self.slice[3] = UF

		self.U_corners[0] = DFL
		self.U_corners[3] = UFL
		self.D_corners[3] = UFR
		self.D_corners[0] = DFR
	def F2(self): self.F(); self.F()
	def Fp(self): self.F(); self.F(); self.F()

	def B(self):

		UB = self.U_edges[1]
		RB = self.slice[2]
		DB = self.D_edges[1]
		LB = self.slice[1]
		
		UBL = self.U_corners[1]
		UBR = self.U_corners[2]
		DBR = self.D_corners[2]
		DBL = self.D_corners[1]

		UBL.flip(2)
		UBR.flip(1)
		DBR.flip(2)
		DBL.flip(1)


		UB.flip()
		RB.flip()
		DB.flip()
		LB.flip()	
		
		self.U_edges[1] = RB
		self.slice[1] = UB
		self.D_edges[1] = LB
		self.slice[2] = DB

		self.U_corners[1] = UBR
		self.U_corners[2] = DBR
		self.D_corners[1] = UBL
		self.D_corners[2] = DBL
	def B2(self): self.B(); self.B()
	def Bp(self): self.B(); self.B(); self.B()


	def R(self):	
		# UR --> BR --> DR --> FR
		# UFR --> UBR --> BDR ---> FDR
	
		UR = self.U_edges[2]
		BR = self.slice[2]
		DR = self.D_edges[2]
		FR = self.slice[3]
		
		UFR = self.U_corners[3]
		UBR = self.U_corners[2]
		DBR = self.D_corners[2]
		DFR = self.D_corners[3]

		UFR.flip(1)
		UBR.flip(2)
		DBR.flip(1)
		DFR.flip(2)
		
		self.U_edges[2] = FR
		self.slice[2] = UR
		self.D_edges[2] = BR
		self.slice[3] = DR

		self.U_corners[2] = UFR
		self.U_corners[3] = DFR
		self.D_corners[2] = UBR
		self.D_corners[3] = DBR
	def R2(self): self.R(); self.R()
	def Rp(self): self.R(); self.R(); self.R()

	def L(self):	
		# UL <-- BL <-- DL <-- FL
		# UFR <-- UBR <-- BDR <-- FDR
	
		UL = self.U_edges[0]
		BL = self.slice[1]
		DL = self.D_edges[0]
		FL = self.slice[0]
		
		UFL = self.U_corners[0]
		UBL = self.U_corners[1]
		DBL = self.D_corners[1]
		DFL = self.D_corners[0]

		UFL.flip(2)
		UBL.flip(1)
		DBL.flip(2)
		DFL.flip(1)
		
		self.U_edges[0] = BL
		self.slice[0] = UL
		self.D_edges[0] = FL
		self.slice[1] = DL

		self.U_corners[0] = UBL
		self.U_corners[1] = DBL
		self.D_corners[1] = DFL
		self.D_corners[0] = UFL
	def L2(self): self.L(); self.L()
	def Lp(self): self.L(); self.L(); self.L()

class EOTable:
	def __init__(self):
		self.table = {0: 0}
	def store_table(self, fname = 'ptable_eo.txt'):
		with open(fname, 'w') as file:
			file.write(str(self.table))
	def load_table(self, fname='ptable_eo.txt'):
		with open(fname,'r') as file:
			self.table = eval(file.read())
	def gen(self,max_mc=5):
		print(f"Generating EOs (Depth={max_mc})")
		i=0
		for m in ["F","B"]: 
			self._gen(m,max_mc)
			i+=1
			print(f"{i}/4")
	def get_table(self):
		return self.table
	def _gen(self, movs='', max_mc = 5):
		mlen = len(movs.split(' '))
		if mlen > max_mc: return 
		
		state = cubestate()
		state.parse(movs)
		eo = state.eo_repr()
		
		if not (eo in self.table.keys()):
			self.table[eo] = mlen
			
			
			
		elif (eo in self.table.keys() and mlen < self.table[eo]): 
			self.table[eo] = mlen
			
	
		for move in vmoves:
			
			if  move[0] == movs.split(' ')[-1][0]:
				continue
			self._gen(movs + ' ' + move, max_mc)
			


class EOSolver:
	def __init__(self, scram, EO, max_len=5, max_eos=30):
		self.scram = scram
		self.table = EO.get_table()
		self.solved_states = []
		self.max_len = max_len
		self.max_eos = max_eos
	
	def solve(self, cs=''):
		if len(self.solved_states) > self.max_eos: return
		state = cubestate()
		state.parse(self.scram + ' ' + cs)
		if state.eo_repr() == 0:
			if len(cs) == 0 or cs.split(' ')[-1][0] in ['F','B']:
				self.solved_states.append(cs)

		if len(cs.split(' ')) > self.max_len: return
		
		eo_dist = self.table[state.eo_repr()]
		
		for move in vmoves:
			
			if  not(cs.split(' ') == ['']) and move[0] == cs.split(' ')[-1][0]: continue


			nstate = cubestate()
			nstate.parse(self.scram + ' ' + cs + ' ' + move)
			eor = nstate.eo_repr()
			if eor not in self.table.keys(): print(f"Warning! Unknown EO state {eor}"); return
			
			neo_dist = self.table[eor]
			
			
			if neo_dist <= eo_dist:
				self.solve(cs + ' ' + move)

class DRSolver:
	targets = {(2,4), (1,4), (1,3)}
	def __init__(self, scram):
		self.scram = scram
		self.rzps = []
	def solve_rzp(self):
		ar_rl = ["R", "L", "R'", "L'", ""]
		ar_ud = ["U","U'","D","D'",""]

		for m1 in ar_rl
			for m2 in ar_ud:
				for m3 in ar_rl:   # yess i know its bad
					state = cubestate()  
					crzp =  ' '.join((m1,m2,m3))
					state.parse(self.scram + crzp)
					if state.drm in targets: self.rzps.append(crzp)
					


EOtable = EOTable()
EOtable.load_table('ptable_eo6.txt')


#eos = EOSolver("R' U' F L' U' L2 F2 L2 D F2 D' F2 R2 D U2 B' U2 R' B2 L F L' D R' U' F", EOtable,5)
#eos.solve()

cube = cubestate()
cube.parse("R' U' F L' U' L2 F2 L2 D F2 D' F2 R2 D U2 B' U2 R' B2 L F L' D R' U' F U F L' D B")
#cube.parse("B")
print(cube.drm_c())

#print(eos.solved_states)
#print(len(eos.solved_states))





input("-------")