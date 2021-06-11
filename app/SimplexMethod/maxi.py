from __future__ import division
from numpy import *


float_formatter = "{:.3f}".format
set_printoptions(formatter={'float_kind':float_formatter})

class Tableau:
    def __init__(self, obj):
        self.obj = [1] + obj
        self.rows = []
        self.cons = []
        self.iter = 0
        self.response_iter=[]
        self.final_response={}
        

    def add_constraint(self, expression, value):
        self.rows.append([0] + expression)
        self.cons.append(value)

    def _columna_pivot(self):
        low = 0
        idx = 0
        for i in range(1, len(self.obj)-1):
            if self.obj[i] < low:
                low = self.obj[i]
                idx = i
        if idx == 0: return -1
        return idx

    def _fila_pivot(self, col):
        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        ratio = []
        for i in range(len(rhs)):
            if lhs[i] == 0:
                ratio.append(99999999 * abs(max(rhs)))
                continue
            ratio.append(rhs[i]/lhs[i])
        return argmin(ratio)
    
    def display(self):
        matriz = matrix([self.obj] + self.rows)
        self.final_response['z']= self.obj[-1];

        return matriz.tolist();
      
    def format_response(self,pivot,tableu):
      response_data = {
        'iter':self.iter,
        'pivot':pivot,
        'tableu':tableu,
      };
      self.iter= self.iter+1;
      return response_data

    def _pivot(self, row, col):
        e = self.rows[row][col]
        self.rows[row] /= e
        for r in range(len(self.rows)):
            if r == row: continue
            self.rows[r] = self.rows[r] - self.rows[r][col]*self.rows[row]
        self.obj = self.obj - self.obj[col]*self.rows[row]

    def _check(self):
        if min(self.obj[1:-1]) >= 0: return 1
        return 0
        
    def solve(self):
        # build full tableau
        for i in range(len(self.rows)):
            self.obj += [0]
            ident = [0 for r in range(len(self.rows))]
            ident[i] = 1
            self.rows[i] += ident + [self.cons[i]]
            self.rows[i] = array(self.rows[i], dtype=float)
        self.obj = array(self.obj + [0], dtype=float)
        # solve
        f_rta= self.format_response([],self.display());
        response_variables=[]
        self.response_iter.append(f_rta);
        while not self._check():
            columna = self._columna_pivot()
            print("columna",columna)
            
            fila = self._fila_pivot(columna)
            print("fila",fila)
            self._pivot(fila,columna)
            
            response_variables.append([columna,fila]);
            print ('\npivot column: %s\npivot row: %s'%(columna+1,fila+2))
            f_rta= self.format_response([columna+1,fila+2],self.display());
            self.response_iter.append(f_rta);

        self.define_final_rtas(response_variables)
        return self.response_iter,self.final_response



    def define_final_rtas(self, response_pairs):
        for pairs in response_pairs:
            col = pairs[0]
            fil = pairs[1]
            if col <= len(self.cons): 
                self.final_response['x'+str(col-1)] = self.rows[fil][-1]
            else:
                self.final_response['s'+str(col-1)] = self.rows[fil][-1]

## EXAMPLE
#t = Tableau([-50,-80])
#t.add_constraint([1, 2], 120)
#t.add_constraint([1, 1], 90)
#print(t.solve())