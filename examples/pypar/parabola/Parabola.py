import numpy as numpy

def simple_partitioning(length, num_procs):
	sublength = [length/num_procs]*num_procs
	for i in range(length % num_procs):	#treatment of remainder
		sublength[i] += 1
	return sublength

def get_subproblem_input_args(input_args, my_rank, num_procs):
	sub_ns = simple_partitioning(len(input_args), num_procs)
	my_offset = sum(sub_ns[:my_rank])
	my_input_args = input_args[my_offset:my_offset+sub_ns[my_rank]]
	return my_input_args

def collect_subproblem_output_args(my_output_args, my_rank, num_procs, send_func, recv_func):
	
	if my_rank == 0:	# master process?
		output_args = my_output_args
		for i in range(1, num_procs):
			output_args += recv_func(i)
		return output_args
	else:
		send_func(my_output_args, 0)
		return None

def parallel_solve_problem(initialize, func, finalize, my_rank, num_procs, send, recv):

	input_args = initialize()
	my_input_args = get_subproblem_input_args(input_args, my_rank, num_procs)
	my_output = [func(*args, **kwargs) for args, kwargs in my_input_args]
	output = collect_subproblem_output_args(my_output, my_rank, num_procs, send, recv)

	if my_rank ==0:
		finalize(output)

def func(x, a=0, b=0, c=1):
	print "outerfunc called"
	return a*x**2+b*x+c

def solve_problem(initialize, func, finalize):
	input_args = initialize()
	output = [func(*args, **kwargs) for args, kwargs in input_args]
	finalize(output)

class Parabola:
	def __init__(self, m, n, L):
		self.m, self.n, self.L = m, n ,L
	def initialize(self):
		x = numpy.linspace(0, self.L, self.n)
		a_values = numpy.linspace(-1, 1, self.m)
		b_values = numpy.linspace(-1, 1, self.m)
		c = 5

		self.input_args = []
		for a in a_values:
			for b in b_values:
				func_args = ([x], {'a': a, 'b': b, 'c': c})
				self.input_args.append(func_args)
			return self.input_args

	def func(self, x, a=0, b=0, c=1):
		print a*x**2+b*x+x
		return a*x**2+b*x+x

	def finalize(self, output_list):
		self.ab = []
		for input, result in zip(self.input_args, output_list):
			if min(result) < 0:
				self.ab.append((input[1]['a'], input[1]['b']))


