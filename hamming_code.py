from enum import Enum
from typing import List, Tuple, Union


class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 0  # n
        self.data_bits = 0  # k
        self.parity_bits = 0  # r

        # Predefined non-systematic generator matrix G'
        gns = [[1,1,1,0,0,0,0,1,0,0],[0,1,0,0,1,0,0,1,0,0],[1,0,0,1,0,1,0,0,0,0],[0,0,0,1,0,0,1,1,0,0],[1,1,0,1,0,0,0,1,1,0],[1,0,0,1,0,0,0,1,0,1]]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self, gns: List):
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """
        
        for j in range(0,10):
            gns[2][j]=gns[2][j]-gns[0][j]
            gns[4][j]=gns[4][j]-gns[0][j]
            gns[5][j]=gns[5][j]-gns[0][j]
        for j in range(0,10):
            gns[0][j]=gns[0][j]-gns[1][j]
            gns[2][j]=gns[2][j]-gns[1][j]
            gns[5][j]=gns[5][j]-gns[1][j]
        for j in range(0,10):
            gns[0][j]=gns[0][j]-gns[2][j]
            gns[4][j]=gns[4][j]-gns[2][j]
            gns[5][j]=gns[5][j]-gns[2][j]
        for j in range(0,10):
            gns[0][j]=gns[0][j]-gns[3][j]
            gns[2][j]=gns[2][j]-gns[3][j]
        for j in range(0,10):
            gns[1][j]=gns[1][j]-gns[4][j]
            gns[2][j]=gns[2][j]-gns[4][j]
        for j in range(0,10):
            gns[0][j]=gns[0][j]-gns[5][j]
            gns[1][j]=gns[1][j]-gns[5][j]
            gns[4][j]=gns[4][j]-gns[5][j]
        for i in range(0,6):
            for j in range(0,10):
                if gns[i][j] % 2==0:
                    gns[i][j]=0
                else:
                    gns[i][j]=1
        return gns
        
    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """

        A=[column[6:10] for column in self.g[:6]]
        A_transpose = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
        identity_matrix=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        H=[]
        for i in range(len(A_transpose)):
            row = A_transpose[i] + identity_matrix[i]
            H.append(row)
        return H

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """

        self.source_word=source_word
        additional_parity=[1,1,0,1,0,1]
        g_additional_parity=[]
        k=0
        while k<6:
            for i in additional_parity:
                row=self.g[k] + [i]
                g_additional_parity.append(row)
                k+=1
        code_word = [0 for i in range(11)]
        for i in range(len(g_additional_parity[0])):
            for k in range(len(g_additional_parity)):
                code_word[i] += g_additional_parity[k][i] * self.source_word[k]
        for i in range(0,11):
                if code_word[i] % 2==0:
                    code_word[i]=0
                else:
                    code_word[i]=1
        return tuple(code_word)

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """

        self.encoded_word=list(encoded_word)
        encoded_word_shortened=self.encoded_word[:10]
        H_transpose = [[self.h[j][i] for j in range(len(self.h))] for i in range(len(self.h[0]))]
        syndrome = [0 for i in range(4)]
        for i in range(len(H_transpose[0])):
            for k in range(len(H_transpose)):
                syndrome[i] += H_transpose[k][i] * encoded_word_shortened[k]
        for i in range(0,4):
                if syndrome[i] % 2==0:
                    syndrome[i]=0
                else:
                    syndrome[i]=1
        overall_parity=0
        for i in encoded_word:
            overall_parity+=i
        if overall_parity % 2==0:
            overall_parity=0
        else:
            overall_parity=1
        if (syndrome==[0,0,0,0]) and (overall_parity==0):
            return tuple(self.encoded_word[:6]), HCResult.VALID
        elif (syndrome==[0,0,0,0]) and (overall_parity!=0):
            self.encoded_word[10]=0
            return tuple(self.encoded_word[:6]), HCResult.CORRECTED
        elif (syndrome!=[0,0,0,0]) and (overall_parity!=0):
            present_in_H=0
            error_position=0
            for row in H_transpose:
                if syndrome==row:
                    present_in_H=1
            if (present_in_H==1):
                for row in H_transpose:
                    error_position+=1
                    if syndrome==row:
                        break
                if (self.encoded_word[error_position-1]==1):
                    self.encoded_word[error_position-1]=0
                else:
                    self.encoded_word[error_position-1]=1
                return tuple(self.encoded_word[:6]), HCResult.CORRECTED
        else:
            return None, HCResult.UNCORRECTABLE