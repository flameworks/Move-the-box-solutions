class Grid:
    def __init__(self,serial = ''):
        self.l = 7
        self.h = 15
        while serial[:self.l] == '0000000':
            serial = serial[self.l:]
        self.structure = []
        if serial: self.h = len(serial) // self.l
        for idx in range(self.h):
            temp = [0]*self.l
            self.structure.append(temp)
        if serial:
            counter = 0
            for i in range(self.h):
                for j in range(self.l):
                    self.structure[i][j] = int(serial[counter])
                    counter += 1
    def getID(self):
        strr = ''
        for r in self.structure:
            for j in r:
                strr += str(j)
        while strr[:self.l] == '0000000':
            strr = strr[self.l:]
        return strr

    def fill(self,row = None,arr= ''):
        if row == None: row = int(input('Row? (1..10): '))
        if arr == '':
            arr = input('Input for row' + str(row) + ': ')            
            while len(arr) < self.l:
                arr += 'x'
        temp = []
        for c in arr:
            try:
                temp.append(int(c))
            except:
                temp.append(0)
        self.structure[self.h-row] = temp
        
    def printer(self):
        self.gravity()
        print(" R")
        for rowDX in range(len(self.structure)):
            row = self.structure[rowDX]
            if row.count(0) == self.l: continue
            strr = ' ' + str(self.h-rowDX-1) + '|'
            for c in row:
                if c == 0: strr += ' '
                else: strr += str(c)
                strr += ' '
            strr += ' '
            print(strr)
        print('   - - - - - - -  ')
        print('C: 0 1 2 3 4 5 6  ')
        print()

    def gravity(self):
        bol = True
        while bol:
            bol = False
            subBol = True
            while subBol:
                subBol = False
                for i in range(self.h-1):
                    for j in range(self.l):
                        c = self.structure[i][j]
                        if c == 0: continue
                        b = self.structure[i+1][j]
                        if b == 0:
                            self.structure[i][j] = 0
                            self.structure[i+1][j] = c
                            subBol = True
            if self.burst(): bol = True

    def burst(self):
        toZero = []
        for i in range(self.h):
            if self.structure[i].count(0) > 4: continue
            for j in range(self.l-2):
                c = self.structure[i][j]
                if c != 0:
                    for x in range(self.l-j,2,-1):
                        temp = self.structure[i][j:j+x]
                        if temp.count(temp[0]) == len(temp):
                            for p in range(x):
                                toZero.append((i,j+p))
                            break
        for j in range(self.l):
            col = list(map(lambda x: x[j], self.structure))
            for i in range(self.h-2):
                f = col[i]
                if f != 0:
                    for x in range(self.h-i,2,-1):
                        temp2 = col[i:i+x]
                        if temp2.count(temp2[0]) == len(temp2):
                            for p in range(x):
                                toZero.append((i+p,j))
                            break
        for i,j in toZero:
            self.structure[i][j] = 0
        return len(toZero) > 0
    
    def check(self):
        for row in self.structure:
            if row.count(0) != self.l: return False
        return True
    
    def valid(self):
        if self.check(): return True
        d = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        for row in self.structure:
            for c in row: d[c] += 1
        for item in d:
            if 0 < d[item] < 3: return False
        return True

    def guess(self,num,steps):
        jLeft = -1
        jRight = 8
        jTop = 20
        jBot = -1
        for jLeft in range(self.l):
            col = list(map(lambda x: x[jLeft], self.structure))
            if col.count(num) > 0: break
        for jRight in range(self.l-1,-1,-1):
            col = list(map(lambda x: x[jRight], self.structure))
            if col.count(num) > 0: break
        for jBot in range(self.h-1,-1,-1):
            row = self.structure[jBot]
            if row.count(num) > 0: break
        for jTop in range(self.h):
            row = self.structure[jTop]
            if row.count(num) > 0: break
        if (jRight-jLeft+1)*(jBot-jTop+1) != 6: return False
        return True
    
    def move(self,coord,direction): 
        i,j = coord
        if direction == 'R':
            self.structure[i][j], self.structure[i][j+1] = \
                self.structure[i][j+1], self.structure[i][j]
        elif direction == 'D':
            self.structure[i][j], self.structure[i+1][j] = \
                self.structure[i+1][j], self.structure[i][j]
        elif direction == 'L':
            self.structure[i][j], self.structure[i][j-1] = \
                self.structure[i][j-1], self.structure[i][j]
        self.gravity()

    def count(self):
        cnt = 0
        for row in self.structure:
            for c in row:
                if c != 0: cnt += 1
        return cnt

    def validMove(self,coord,direction):
        i,j = coord
        if self.structure[i][j] == 0: return False
        if j == self.l-1 and direction == 'R': return False
        if j == 0 and direction == 'L': return False
        if i == self.h-1 and direction == 'D': return False
        if direction == 'R':
            return self.structure[i][j] != self.structure[i][j+1]
        elif direction == 'D':
            return self.structure[i][j] != self.structure[i+1][j]
        elif direction == 'L':
            return self.structure[i][j-1] == 0      

    def solve(self):
        depthCount = 0
        origID = self.getID()
        workingGrp = [ origID ]
        moveDict = {origID:[]}
        while workingGrp:
            iteration = len(workingGrp)
            for iteration1 in range(iteration):
                gridID = workingGrp.pop(0)
                origTemp = Grid(gridID)
                for i in range(origTemp.h):
                    for j in range(origTemp.l):
                        c = origTemp.structure[i][j]
                        if c == 0: continue
                        for direction in ['L','R','D']:
                            if not origTemp.validMove((i,j),direction): continue            
                            temp = Grid(gridID)
                            temp.move((i,j),direction)
                            tempID = temp.getID()
                            depthCount += 1
                            if temp.valid():
                                if temp.check():
                                    print("Answer format: (Row,Col),Movement")
                                    print("ANSWER:",moveDict[gridID]+[((origTemp.h-1-i,j),direction)])
                                    print("Depth used:",f'{depthCount:,}')
                                    return
                                if tempID not in moveDict:
                                    moveDict[tempID] = \
                                        moveDict[gridID] + [((origTemp.h-1-i,j),direction)]
            workingGrp = list(moveDict.keys())
        if not workingGrp: print("No solution")


import time

r = input('Input number of rows or SerialNum: ')
##r = '00000000000000000000000000000000000000000000012000002440001212000243300123110'
if len(r) > 3:
    a = Grid(r)
else:
    a = Grid()
    for i in range(int(r)):
        a.fill(i+1)
tic = time.perf_counter()
print("\nSerialNum:",'\n'+a.getID(),'\n')
a.printer()
a.solve()
toc = time.perf_counter()
print(f"Solved in {toc - tic:0.5f}s")


