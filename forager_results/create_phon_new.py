
import pandas as pd 

from forager.embeddings import embeddings
from forager.frequency import get_frequencies
from forager.cues import get_labels_and_frequencies
from forager.cues import phonology_funcs
from forager.cues import create_semantic_matrix
import os 
import numpy as np

class data: 
    '''
        Description: 
            data class contains functions that help with creating the lexical data files.     
    '''
    
    def __init__(self):
        self.path = 'data/lexical_data/'

        # Check whether the specified path exists or not
        isExist = os.path.exists(self.path)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(self.path)
        words = pd.read_csv(self.path + 'forager2082_vocab.csv').vocab.tolist()
        #creating embeddings 
        embeddings(words, self.path)
        print("\nCreated and saved embeddings as USE_embeddings.csv inside " + self.path) 
        
        #get frequencies 
        get_frequencies(self.path + '/USE_embeddings.csv', self.path)
        print("\nCreated and saved word frequencies as USE_frequencies.csv inside " + self.path)  
        
        
        # get semantic matrix 
        create_semantic_matrix(self.path + '/USE_embeddings.csv', self.path)
        print("\nCreated and saved semantic similarity matrix as USE_semantic_matrix.csv inside " + self.path)  
        
        # get phonological matrix 
        #labels, freq_matrix = get_labels_and_frequencies(self.path + '/USE_frequencies.csv')
        # new_labels = pd.read_csv(self.path + 'new_items.csv').vocab.tolist()
        # old_labels = pd.read_csv(self.path + 'forager2075_vocab.csv').vocab.tolist()
        # old_matrix = np.array(pd.read_csv(self.path + 'pmatrix.csv',delimiter=',', header=None))
        # phonology_funcs.update_phonological_matrix(new_labels, old_labels, old_matrix, self.path)
        # print("\nCreated and saved phonological similarity matrix as USE_phon_matrix.csv inside " + self.path) 

#### SAMPLE RUN CODE ####
        
#vocab_list = pd.read_csv('data/lexical_data/vocab.csv').vocab.tolist()
data()