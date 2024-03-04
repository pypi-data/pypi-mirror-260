import math

class value:
    
    def __init__(self,data, children=(), op="",label="" ):
        self.data=data
        self.prev = set(children)
        self._backward = lambda :None
        self.op= op
        self.grad = 0.0
        self.label=label
        
        
    def __repr__(self):
        #return  f"value({self.data},{self.prev},{self.op})"
        return  f"{self.data}"
    
    def __add__(self,other):
        other = other if isinstance(other,value) else value(other)
        
        out = value(self.data+other.data,(self,other),"+")
        
        def backward():
            self.grad  +=1 * out.grad 
            other.grad +=1 * out.grad
        out._backward = backward
        
        return out
    
    def __sub__(self, other): 
        return self + (-other)

    def __rsub__(self, other): 
        return other + (-self)
    
    def __radd__(self, other):
        return self + other
    
    def  __rmul__(self, other):
        return self * other
    
    def __mul__(self,other):
        
        other = other if isinstance(other, value) else value(other)   
        
        out = value(self.data * other.data, (self, other), '*')
        
        def backward():
            self.grad  += other.data * out.grad 
            other.grad += self.data  * out.grad
        out._backward = backward
        return out
    
    def __pow__(self,other):
        assert isinstance(other, (int,float)),"only int/float powers"
        out= value(self.data**other,(self,),f'**{other}' )
        
        def backward():
            self.grad += other*self.data**(other-1) * out.grad
        out._backward = backward
        return out
    
    def __truediv__(self, other): # self / other
        return self * (other**-1)

    def __rtruediv__(self, other): # other / self
        return other * self**-1
    
    def __neg__(self): 
        return self * -1
    
    def tanh(self):
        x =self.data
        t =(math.exp(2*x)-1)/(math.exp(2*x)+1)
        out = value(t,(self,),"tanh")
        def backward():
            self.grad  += (1 - t**2)*out.grad
        out._backward = backward
        
        return out
    
    def relu(self):
        x=self.data
        if x<0:
            out = value(0,(self,),"relu")
        else:
            out = value(x,(self,),"relu")
            
        def backward():
            if x<0:
                self.grad  += 0*out.grad
            else:
                self.grad  += 1*out.grad
        out._backward = backward
        
        return out
    
    def backward(self):
        
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v.prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        
        self.grad=1
        for node in reversed(topo):
            node._backward()
        
