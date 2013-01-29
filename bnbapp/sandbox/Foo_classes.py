class Foo(object):
     def __init__(self, frob, frotz):
          self.frobnicate = frob
          self.frotz = frotz

class Bar(Foo):
	def __init__(self, frob, frizzle):
		Foo.__init__(self, frob, frizzle)
		self.frotz = 34
		self.frazzle = frizzle

class A(object):
	def __init__(self):
		self.name = 'A class'
	
	def routine(self):
		print "A.routine()"

	def render(self, foo, *args, **kwargs):
		foo = 'this is class A'
		print foo  

	def get_name(self):
		return self.name 	  
########################
########################

class A(object) :
    def __init__(self) :
        self.a = 1

    def multiply(self, v) :
    	print 'multiplying...'
        return self.a * v


class B(object) :
    def __init__(self) :
        self.b = 2

    def save(self) :
        print "Saving Object.."
        for a in vars(self) :
            print "Saving " + a

class C(A,B) :
    def __init__(self) :
        A.__init__(self)
        B.__init__(self)

    def multiply_and_save(self, v) :
        super(C,self).multiply(v)
        super(C,self).save()

c = C()
c.multiply_and_save(3)


class Save(object) :
    def __init__(self) :
        self.filename = "save.txt"

    def save(self) :
        fH = open(self.filename, "w")
        for a in vars(self) :
            fH.write( a )
            fH.write( "=" )
            fH.write( str(self.__dict__[a]) )
            fH.write("\n")
        fH.close()


class D(Save) :
    def __init__(self) :
        Save.__init__(self)
        self.name = "D"
        self.value = 3
        self.color = "blue"

    def __del__(self) :
        super(D, self).save()

d = D()
del d