from Parabola import Parabola
from Parabola import parallel_solve_problem
import pypar

problem = Parabola(m=100, n=50, L=10)
my_rank = pypar.rank()
num_procs = pypar.size()
print num_procs
parallel_solve_problem(problem.initialize, problem.func, problem.finalize, my_rank, num_procs, pypar.send, pypar.receive)
pypar.finalize()
