import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
import dwavebinarycsp.factories.constraint.gates as gates
import dwave.inspector


csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
#csp.add_constraint(gates.and_gate(['A0', 'B0', 'P0'])) #ignored as ouput is odd so 
#P0 is always 1 and P0 is only the result of A0 AND B0(no other inputs)

#csp.add_constraint(gates.and_gate(['A1', 'B0', 'and1']))
#csp.add_constraint(gates.and_gate(['A0', 'B1', 'and2']))
csp.add_constraint(gates.halfadder_gate(['A1', 'B1', 'P1', 'carry1']))

#csp.add_constraint(gates.and_gate(['A2', 'B0', 'and3']))
csp.add_constraint(gates.and_gate(['A1', 'B1', 'and4']))
csp.add_constraint(gates.halfadder_gate(['a', 'and4', 'ha34', 'carry2']))

#csp.add_constraint(gates.and_gate(['A2', 'B1', 'and5']))
#csp.add_constraint(gates.and_gate(['A0', 'B2', 'and6']))
#csp.add_constraint(gates.and_gate(['A1', 'B2', 'and7']))
#csp.add_constraint(gates.and_gate(['A2', 'B2', 'and8']))

csp.add_constraint(gates.fulladder_gate(['ha34', 'a', 'carry1', 'P2', 'carry3']))
#ha34 refers to output of halfadder with inputs of the 'and3' and 'and4'
csp.add_constraint(gates.fulladder_gate(['B1', 'A1', 'carry2', 'fa57', 'carry4']))
#fa57 refers to output of fulladder with inputs of the 'and5', 'and7' and 'carry2'

csp.add_constraint(gates.halfadder_gate(['carry3', 'fa57', 'P3', 'carry5']))

csp.add_constraint(gates.fulladder_gate(['carry4', 'a', 'carry5', 'P4', 'P5']))

#fix variables so output is the number you want to factorise
#csp.fix_variable('P0', 1)#ignore this as we removed P0 from circuit
csp.fix_variable('P1', 1)
csp.fix_variable('P2', 0)
csp.fix_variable('P3', 0)
csp.fix_variable('P4', 0)
csp.fix_variable('P5', 1)

csp.fix_variable('a', 1)
#'a' represenst most and least significant bit of inputs


bqm = dwavebinarycsp.stitch(csp)

sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(bqm, num_reads = 1000, label = '3 bit multiplier')

print(response)
dwave.inspector.show(response)