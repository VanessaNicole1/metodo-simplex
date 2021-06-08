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

    def _pivot_column(self):
        low = 0
        idx = 0
        for i in range(1, len(self.obj)-1):
            if self.obj[i] < low:
                low = self.obj[i]
                idx = i
        if idx == 0: return -1
        return idx

    def _pivot_row(self, col):
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
        self.final_response['obj']= self.obj[-1];
        count =0;
        for row in self.rows:
            self.final_response['x'+str(count)]=row[-1]
            count=count+1

        return matriz.tolist();
      
    def format_response(self,pivot,tableu):
      response_data = {
        'iter':self.iter,
        'pivot':pivot,
        'tableu':tableu,
        'response':self.final_response
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
        f_rta= self.format_response([-1,-1],self.display());
        self.response_iter.append(f_rta);
        while not self._check():
            c = self._pivot_column()
            r = self._pivot_row(c)
            self._pivot(r,c)
            print ('\npivot column: %s\npivot row: %s'%(c+1,r+2))
            f_rta= self.format_response([c+1,r+2],self.display());
            self.response_iter.append(f_rta);

        return self.response_iter
