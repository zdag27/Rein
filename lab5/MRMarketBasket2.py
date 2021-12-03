"""
MRMarketBasket2
"""
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRMarketBasket2(MRJob):

    def configure_args(self):
        """
        Additional configuration flag to get the groceries file
    
        :return:
        """
        super(MRMarketBasket2, self).configure_args() 
    
    
    def mapper(self, _, line):
        """
        This is the mapper, it should generate one item count
        
        :param line: contains a transaction
        """
        # Each line is a string a,b,c
        filee=open('debug.txt','w')
        print(line,file=filee)
        filee.close()
        trans = line.strip().split(',')
        trans=sorted(trans)
        for i in trans:
        	yield i, 1    
                    
    def reducer(self, key, values):
        """
        Input is an item as key and all the countings
        it has assigned
        
        Output should be at least a pair (key, new counting)
        """
        #
        # Compute reducer here
        #        

        yield key, len(list(values))
        

    def steps(self):
        return [MRStep(mapper=self.mapper,
                           reducer=self.reducer)]    


if __name__ == '__main__':
    MRMarketBasket2.run()
