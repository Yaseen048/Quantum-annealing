import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
import dwavebinarycsp.factories.constraint.gates as gates
import dwave.inspector

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(gates.and_gate(['A0', 'B0', 'P0'])) #ignored as ouput is odd so 
#P0 is always 1 and P0 is only the result of A0 AND B0(no other inputs)

csp.add_constraint(gates.and_gate(['A1', 'B0', 'and1']))
csp.add_constraint(gates.and_gate(['A2', 'B0', 'and2']))
csp.add_constraint(gates.and_gate(['A3', 'B0', 'and3']))

csp.add_constraint(gates.and_gate(['A0', 'B1', 'and4']))
csp.add_constraint(gates.and_gate(['A1', 'B1', 'and5']))
csp.add_constraint(gates.and_gate(['A2', 'B1', 'and6']))
csp.add_constraint(gates.and_gate(['A3', 'B1', 'and7']))

csp.add_constraint(gates.fulladder_gate(['and1', 'and4', 'a', 'P1', 'carry1']))
csp.add_constraint(gates.fulladder_gate(['and2', 'and5', 'carry1', 'fa1', 'carry2']))
csp.add_constraint(gates.fulladder_gate(['and3', 'and6', 'carry2', 'fa2', 'carry3']))
csp.add_constraint(gates.fulladder_gate(['and7', 'a', 'carry3', 'fa3', 'carry4']))

csp.add_constraint(gates.and_gate(['A0', 'B2', 'and8']))
csp.add_constraint(gates.and_gate(['A1', 'B2', 'and9']))
csp.add_constraint(gates.and_gate(['A2', 'B2', 'and10']))
csp.add_constraint(gates.and_gate(['A3', 'B2', 'and11']))

csp.add_constraint(gates.fulladder_gate(['fa1', 'and8', 'a', 'P2', 'carry5']))
csp.add_constraint(gates.fulladder_gate(['fa2', 'and9', 'carry5', 'fa4', 'carry6']))
csp.add_constraint(gates.fulladder_gate(['fa3', 'and10', 'carry6', 'fa5', 'carry7']))
csp.add_constraint(gates.fulladder_gate(['carry4', 'and11', 'carry7', 'fa6', 'carry8']))

csp.add_constraint(gates.and_gate(['A0', 'B3', 'and12']))
csp.add_constraint(gates.and_gate(['A1', 'B3', 'and13']))
csp.add_constraint(gates.and_gate(['A2', 'B3', 'and14']))
csp.add_constraint(gates.and_gate(['A3', 'B3', 'and15']))

csp.add_constraint(gates.fulladder_gate(['fa4', 'and12', 'a', 'P3', 'carry9']))
csp.add_constraint(gates.fulladder_gate(['fa5', 'and13', 'carry9', 'P4', 'carry10']))
csp.add_constraint(gates.fulladder_gate(['fa6', 'and14', 'carry10', 'P5', 'carry11']))
csp.add_constraint(gates.fulladder_gate(['carry4', 'and15', 'carry11', 'P6', 'P7']))

#set outputs to binary of number you want to factorise
csp.fix_variable('P0', 1)
csp.fix_variable('P1', 1)
csp.fix_variable('P2', 1)
csp.fix_variable('P3', 1)
csp.fix_variable('P4', 0)
csp.fix_variable('P5', 0)
csp.fix_variable('P6', 0)
csp.fix_variable('P7', 1)

bqm = dwavebinarycsp.stitch(csp)

sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(bqm, num_reads = 1000, annealing_time = 50, label = '4 bit multiplier')

df = response.to_pandas_dataframe()
print(df.head())
dwave.inspector.show(response)