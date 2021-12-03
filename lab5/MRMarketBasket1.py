"""
MRMarketBasket1
"""
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRMarketBasket1(MRJob):

    def configure_args(self):
        """
        Additional configuration flag to get the groceries file
    
        :return:
        """
        super(MRMarketBasket1, self).configure_args() 
    
    
    def mapper(self, _, line):
        """
        This is the mapper, it should generate pairs
        of items
        
        :param line: contains a transaction
        """
        # Each line is a string a,b,c
        trans = line.strip().split(',')
        trans = sorted(trans)
        l=[]
        for i in trans:
        	trans.remove(i)
        	for j in trans:
        		yield (i,j), 1
 
                    
    def reducer(self, key, values):
    	yield key, len(list(values))
        

    def steps(self):
        return [MRStep(mapper=self.mapper,
                           reducer=self.reducer)]    


if __name__ == '__main__':
    MRMarketBasket1.run()
