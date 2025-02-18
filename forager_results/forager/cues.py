import numpy as np
import scipy
import pandas as pd
import nltk
from functools import lru_cache
from itertools import product as iterprod
import re
from tqdm import tqdm

'''

Generate Cue History for each type of cue (similarity, frequency, phonology). Includes
    additional functions to support the creation of similarity matrices and frequency lists.

    Functions
        (1) create_history_variables: creates similarity, frequency, and phonology list and history
        variables to be used by foraging methods in foraging.py
        (2) create_semantic_matrix: converts a word embedding space into a similarity matrix
        (3) phonology_funcs: class to execute the creation of a phonological similarity matrix
'''


def create_history_variables(fluency_list, subject, corrections_df, labels, sim_matrix, freq_matrix, phon_matrix = None):
    '''
        Args:
            (1) sim_matrix: semantic similarity matrix (NxN np.array)
            (2) phon_matrix: phonological similarity matrix (NxN np.array)
            (3) freq_matrix: frequencies array (Nx1 array)
            (4) labels: the space of words (list of length N)
            (5) fluency_list: items produced by a participant (list of size L)

        Returns: 
            (1) sim_list (list, size: L): semantic similarities between each item in fluency_list 
            (2) sim_history(list, size: L arrays of size N): semantic similarities of each word in fluency_list with all items in labels
            (3) phon_list (list, size: L): phonological similarities between each item in fluency_list 
            (4) phon_history (list, size: L arrays of size N): phonological similarities of each word in fluency_list with all items in labels
            (5) freq_list (list, size: L): frequencies of each item in fluency_list (list of size L)
            (6) freq_history  (list, size: L arrays of size N): frequencies of all words in labels repeated L times


    '''
    if phon_matrix is not None:
        phon_matrix[phon_matrix <= 0] = .0001
    sim_matrix[sim_matrix <= 0] = .0001

    freq_list = []
    freq_history = []

    sim_list = []
    sim_history = []

    phon_list = []
    phon_history = []

    print("fluency_list", fluency_list)

    # check if there are any corrections for this subject, if not then the corrections_df will be empty
    # in that case, proceed with the original fluency_list method
    subject_replacement_df = corrections_df[corrections_df['SID'] == subject]

    if len(subject_replacement_df) == 0:
        print("no corrections made for this subject")
        for i in range(0,len(fluency_list)):
            word = fluency_list[i]
            currentwordindex = labels.index(word)

            freq_list.append(freq_matrix[currentwordindex])
            freq_history.append(freq_matrix)

            if i > 0: # get similarity between this word and preceding word
                prevwordindex = labels.index(fluency_list[i-1])
                sim_list.append(sim_matrix[prevwordindex, currentwordindex] )
                sim_history.append(sim_matrix[prevwordindex,:])
                if phon_matrix is not None:
                    phon_list.append(phon_matrix[prevwordindex, currentwordindex] )
                    phon_history.append(phon_matrix[prevwordindex,:])
            else: # first word
                sim_list.append(0.0001)
                sim_history.append(sim_matrix[currentwordindex,:])
                if phon_matrix is not None:
                    phon_list.append(0.0001)
                    phon_history.append(phon_matrix[currentwordindex,:])

        return sim_list, sim_history, freq_list, freq_history,phon_list, phon_history

    else:
        print("corrections made for this subject")
        original_words = subject_replacement_df['entry'].tolist()
        # remove all special characters and spaces from original words (for wordbreak)
        original_words = [re.sub('[^a-zA-Z]+', '', str(v)) for v in original_words]
        replaced_words = subject_replacement_df['replacement'].tolist()

        print("changing phon_matrix for the following words: ", original_words)

        # get index of replaced words in labels
        replaced_word_indices = [labels.index(word) for word in replaced_words]
        
        # create new labels list with original words
        new_labels = [original_words[replaced_word_indices.index(i)] if i in replaced_word_indices else labels[i] for i in range(len(labels))]
        new_labels = [re.sub('[^a-zA-Z]+', '', str(v)) for v in new_labels]
        # now compute the phonological similarity of each original word to every other word in new_labels
        phon_sim_list = []
        for word in original_words:
            phon_sim = [phonology_funcs.normalized_edit_distance(
                                                phonology_funcs.wordbreak(word)[0],
                                                phonology_funcs.wordbreak(new_labels[i])[0]
                                            ) for i in range(len(new_labels))]
            phon_sim_list.append(phon_sim)
        # convert to numpy array
        phon_sim_list = np.array(phon_sim_list)   
        
        # now we replace specific rows and columns of the phon_matrix only for the replaced_word_indices
        for i in range(len(replaced_word_indices)):
            phon_matrix[replaced_word_indices[i],:] = phon_sim_list[i]
            phon_matrix[:,replaced_word_indices[i]] = phon_sim_list[i]

        # now that the phonological matrix itself has been updated, we can proceed with the rest of the method as before
        phon_matrix[phon_matrix <= 0] = .0001
        print("phonological matrix updated")

        for i in range(0,len(fluency_list)):
            word = fluency_list[i]
            currentwordindex = labels.index(word)

            freq_list.append(freq_matrix[currentwordindex])
            freq_history.append(freq_matrix)

            if i > 0: # get similarity between this word and preceding word
                prevwordindex = labels.index(fluency_list[i-1])
                sim_list.append(sim_matrix[prevwordindex, currentwordindex] )
                sim_history.append(sim_matrix[prevwordindex,:])
                if phon_matrix is not None:
                    phon_list.append(phon_matrix[prevwordindex, currentwordindex] )
                    phon_history.append(phon_matrix[prevwordindex,:])
            else: # first word
                sim_list.append(0.0001)
                sim_history.append(sim_matrix[currentwordindex,:])
                if phon_matrix is not None:
                    phon_list.append(0.0001)
                    phon_history.append(phon_matrix[currentwordindex,:])

        return sim_list, sim_history, freq_list, freq_history,phon_list, phon_history

def get_labels_and_frequencies(path_to_frequencies):
    '''
        Description:
            Returns search space of words and their log-frequencies
        Args:
            (1) path_to_frequencies (str): path to a .csv file containing N words (the full search space) and its log-frequencies (Nx2 array)
        Returns: 
            (1) labels (list, size: N): the space of words
            (2) freq_matrix (np.array, Nx1): a np.array of the frequencies of each word in labels
    '''

    freq_matrix = pd.read_csv(path_to_frequencies, header = None)
    labels = list(freq_matrix[0])
    freq_matrix = np.array(freq_matrix[1])

    return labels, freq_matrix

def create_semantic_matrix(path_to_embeddings, path_for_lexical_data):
    '''
        Description:
            Takes in N word embeddings and returns a semantic similarity matrix (NxN np.array)
        Args:
            (1) path_to_embeddings (str): path to a .csv file containing N word embeddings of size D each (DxN array)
        Returns: 
            (1) semantic_matrix: semantic similarity matrix (NxN np.array)
    '''
    embeddings = pd.read_csv(path_to_embeddings, encoding="unicode-escape").transpose().values
    N = len(embeddings)
    
    semantic_matrix = 1-scipy.spatial.distance.cdist(embeddings, embeddings, 'cosine').reshape(-1)
    semantic_matrix = semantic_matrix.reshape((N,N))
    # convert to dataframe without header or index
    semantic_matrix_df = pd.DataFrame(semantic_matrix)
    semantic_matrix_df.to_csv(path_for_lexical_data + '/USE_semantic_matrix.csv', header=False, index=False)
    return semantic_matrix

class phonology_funcs:
    '''
        Description: 
            This class contains functions to generate phonemes from a list of words and create a phonological similarity matrix.
            Code has been adapted from the following link: https://stackoverflow.com/questions/33666557/get-phonemes-from-any-word-in-python-nltk-or-other-modules
        Functions:
            (1) load_arpabet(): loads and returns the arpabet dictionary from the NLTK CMU dictionary
            (2) wordbreak(s, arpabet): takes in a word (str) and an arpabet dictionary and returns a list of phonemes
            (3) normalized_edit_distance(w1, w2): takes in two strings (w1, w2) and returns the normalized edit distance between them
            (3) create_phonological_matrix: takes in a list of labels (size N) and returns a phonological similarity matrix (NxN np.array)
    '''
    @lru_cache()
    def wordbreak(s):
        '''
            Description:
                Takes in a word (str) and an arpabet dictionary and returns a list of phonemes
            Args:
                (1) s (str): string to be broken into phonemes
            Returns:
                (1) phonemes (list, size: variable): list of phonemes in s 
        '''
        try:
            arpabet = nltk.corpus.cmudict.dict()
        except LookupError:
            nltk.download('cmudict')
            arpabet = nltk.corpus.cmudict.dict()
                
        s = s.lower()
        if s in arpabet:
            return arpabet[s]
        middle = len(s)/2
        partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
        for i in partition:
            pre, suf = (s[:i], s[i:])
            if pre in arpabet and phonology_funcs.wordbreak(suf) is not None:
                return [x+y for x,y in iterprod(arpabet[pre], phonology_funcs.wordbreak(suf))]
        return None

    def normalized_edit_distance(w1, w2):
        '''
            Description: 
                Takes in two strings (w1, w2) and returns the normalized edit distance between them
            Args:
                (1) w1 (str): first word
                (2) w2 (str): second word
            Returns:
                (1) normalized_edit_distance (float): normalized edit distance between w1 and w2
        '''
        return round(1-nltk.edit_distance(w1,w2)/(max(len(w1), len(w2))),4)

    def create_phonological_matrix(labels, path_for_lexical_data):
        '''
            Description:
                Takes in a list of labels (size N) and returns a phonological similarity matrix (NxN np.array)
            Args:
                (1) labels: a list of words matching the size of your search space (list of length N)
            Returns: 
                (1) phonological_matrix: phonological similarity matrix (NxN np.array)
        '''
        labels = [re.sub('[^a-zA-Z]+', '', str(v)) for v in labels]
        sim = np.zeros((len(labels), len(labels)))
        for i in tqdm(range(len(labels))):
            for j in range(i):
                sim[i, j] = phonology_funcs.normalized_edit_distance(phonology_funcs.wordbreak(labels[i])[0], phonology_funcs.wordbreak(labels[j])[0])
        sim = sim + sim.T
        np.fill_diagonal(sim, 1)
        # convert to dataframe without header or index
        phon_matrix_df = pd.DataFrame(sim)
        phon_matrix_df.to_csv(path_for_lexical_data + '/USE_phon_matrix.csv', header=False, index=False)
        return sim

    def update_phonological_matrix(new_labels, old_labels, old_matrix, path_for_lexical_data):
        '''
        '''
        new_labels = [re.sub('[^a-zA-Z]+', '', str(v)) for v in new_labels]
        old_labels = [re.sub('[^a-zA-Z]+', '', str(v)) for v in old_labels]

        # print("new_labels=",new_labels)
        # print("old_labels=",old_labels)

        n = len(new_labels)
        N1= old_matrix.shape[1]
        N2= old_matrix.shape[0]

        

        N = N1

        # print("n = ", n)
        # print("N1 = ", N1)
        # print("N2 = ", N2)
        assert N1 == N2

        finalN =  n + N
        # Compute similarities for new items with existing items: nxN 
        new_old_similarities = np.zeros((n, N))
        
        for i, new_item in enumerate(new_labels):
            print("old-new sims for new_item=",new_item)
            for j, existing_item in enumerate(old_labels):
                #print("existing_item=",existing_item)
                new_old_similarities[i, j] = phonology_funcs.normalized_edit_distance(phonology_funcs.wordbreak(new_item)[0], phonology_funcs.wordbreak(existing_item)[0])

        ## also compute similarities of new labels to themselves, nxn
        new_new_similarities = np.zeros((n, n))
        for i, new_item1 in enumerate(new_labels):
            print("new-new sims for new_item=",new_item)
            for j, new_item2 in enumerate(new_labels):
                new_new_similarities[i, j] = phonology_funcs.normalized_edit_distance(phonology_funcs.wordbreak(new_item1)[0], phonology_funcs.wordbreak(new_item2)[0])

        # extended matrix, we first stack the n x N matrix with the nxn matrix to form n x (N+n) matrix

        extended_similarity_matrix = np.hstack((new_old_similarities, new_new_similarities))

        zeros_padding = np.zeros((N, n))

        old_matrix_padded = np.hstack((old_matrix, zeros_padding))

        # Append new similarities to the existing matrix

        final_matrix = np.vstack((old_matrix_padded, extended_similarity_matrix))

        # change the last n columns and rows with the transpose

        final_matrix[:N, N:] = new_old_similarities.T

        print("shape of final matrix is:", final_matrix.shape)    

        assert final_matrix.shape[0] == finalN

        phon_matrix_df = pd.DataFrame(final_matrix)
        phon_matrix_df.to_csv(path_for_lexical_data + '/new_algo_phon_matrix.csv', header=False, index=False)

### SAMPLE RUN CODE ###
#create_semantic_matrix('../data/lexical_data/USE_embeddings.csv')