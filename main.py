from re import T
import numpy as np

class Qstate:
        # in init:
            # dimension d, amplitudes (up to 2^d of these) as np array with check that it is a valid set of amplitudes, vals as integers (max val is 2^d - 1), check that all vals are actually possible, check that  are of correct lengths assert statement, f"error message {variable} message continues"
        # function to sample from this guy (return the quibit configuration)
        # after: add some functions for gates
        # add a new quibit
        def __init__(self,dimensions, amplitudes, vals):
                assert 0<len(amplitudes) and len(amplitudes) <=2**dimensions, "Amplitudes not of correct length"
                assert max(vals)<=(2**dimensions - 1), "maximum value is too big"
                assert len(amplitudes) == len(vals), "amplitudes and vals are not the same length"
                assert abs(1-(sum(i**2 for i in amplitudes))) < 1e-6
                self.d = dimensions
                self.amps = amplitudes
                self.vals = vals
        def sample(self,samples):
                #idk which thing is the probabilities so im just gonna make a random one and we can fix later
                prob = [i**2 for i in self.amps]
                return (np.random.choice(self.vals,size=samples,p=prob))
        
        def cnot(self, index1, index2):
               assert 0 <= index1 < self.d ,"Index out of bounds"
               assert 0 <= index2 < self.d,"Index out of bounds"
               for x in range(len(self.vals)):
                        bit1= (self.vals[x]&(2**index1))>>index1
                        bit2= (self.vals[x]&(2**index2))>>index2
                        result = (bit1^bit2)<<index2
                        self.vals[x]= (self.vals[x]&(((2**self.d)-1)-2**index2)) + result
                        
                        
        def getVals(self):
                return self.vals
        def getAmps(self):
                return self.amps

        def Hadamard(self, index1):
                amps2 = [0]*len(self.amps)
                assert 0 <= index1 < self.d ,"Index out of bounds"
                length = len(self.vals)
                for x in range(length):
                    bit= (self.vals[x]&(2**index1))>>index1
                    if(bit):
                        prob1 = self.vals[x]
                        prob2 = self.vals[x]-(self.vals[x]&(2**index1))
                        
                        new_amp = self.amps[x] * 1/(2**0.5)
                        try:
                            new_index = self.vals.index(prob2)
                            amps2[new_index] += new_amp
                        except:
                            self.vals.append(prob2)
                            amps2.append(new_amp)
                        amps2[x] -= new_amp

                    else:
                        prob1 = self.vals[x]
                        prob2 = self.vals[x]+((2**index1))
                        new_amp = self.amps[x] * 1/(2**0.5)
                        try:
                            new_index = self.vals.index(prob2)
                            amps2[new_index] += new_amp
                            
                        except:
                            self.vals.append(prob2)
                            amps2.append(new_amp)
                        amps2[x] += new_amp
                            
                self.amps = amps2

                            


        def ccnot(self, index1, index2, index3):
               assert 0 <= index1 < self.d ,"Index out of bounds"
               assert 0 <= index2 < self.d,"Index out of bounds"
               assert 0 <= index3 < self.d,"Index out of bounds"
               for x in range(len(self.vals)):
                    bit1= (self.vals[x]&(2**index1))>>index1
                    bit2= (self.vals[x]&(2**index2))>>index2
                    bit3= (self.vals[x]&(2**index3))>>index3
                    result = ((bit1&bit2)^bit3)<<index3
                    self.vals[x]= (self.vals[x]&(((2**self.d)-1)-2**index3)) + result
class Q_computer():
    def __init__(self,d,q_state):
        self.d = d
        assert q_state == 'Qstate'
        self.qstate= q_state
        self.gates = []
    def setState(self,amplitudes,vals):
          state = Qstate(self.d, amplitudes,list(map(lambda x: int(x,2),vals)))
          self.state = state
    def setGates(self, gates):
          assert(all([(func in {'Hadamard','cnot','ccnot'}) for index, func in gates]))
          self.gates = gates
    def addGates(self, gate_object, gate_index):
          assert 0<=gate_index<=len(self.gates)
          self.gates = self.gates[0:gate_index]+[gate_object]000000000000000000+self.gates[gate_index:]

    def sample(self, samples):
          return self.state.sample(samples)
    def Run_Computer(self):
          for x in range(len(self.gates)):
                index, func = self.gates[x]
                print(index)
                getattr(self.state, func)(*index)
          return self.state.getAmps(),list(map(bin,self.state.getVals()))
    


                
    
                
        

def main():
    computer = Q_computer(d=2, q_state="Qstate")
    computer.setGates(
          [((0,), "Hadamard"), ((0,), "Hadamard")]
          )
    computer.setState(
          [1], ["00"]
    )
    print(computer.Run_Computer())
    print(computer.sample(10))

    computer.addGates(((0, 1), "cnot"), 1)

    computer.setState(
          [1], ["00"]
    )
    print(computer.Run_Computer())
    print(computer.sample(10))





if __name__ == "__main__":
        main()