import yaml
from rich.console import Console
import numpy as np

class Guesser:
    '''
        INSTRUCTIONS: This function should return your next guess. 
        Currently it picks a random word from wordlist and returns that.
        You will need to parse the output from Wordle:
        - If your guess contains that character in a different position, Wordle will return a '-' in that position.
        - If your guess does not contain that character at all, Wordle will return a '+' in that position.
        - If you guesses the character placement correctly, Wordle will return the character. 

        You CANNOT just get the word from the Wordle class, obviously :)
    '''
    def __init__(self, manual):
        self.word_list = yaml.load(open('wordlist.yaml'), Loader=yaml.FullLoader)
        self.letter_probs = {'a': [0.07822378834312863, 0.09973683540335704, 0.13361427530984388, 0.06531400150678378, 0.010426232807849422], 'b': [0.044172332248734895, 0.022254154176079215, 0.00932983561430372, 0.004124752191509056, 0.0010527748144730914], 'c': [0.07540769664268558, 0.007580267013681296, 0.01593183622975031, 0.09335365395557076, 0.008563054514062338], 'd': [0.02476941032516033, 0.005658564657573927, 0.03060488554650378, 0.017884060105762562, 0.08103932510684612], 'e': [0.034536351100283656, 0.07432281166591684, 0.13794873917804698, 0.1448482239622777, 0.2361711740196209], 'f': [0.0417328032004659, 0.018824949883365086, 0.009518301919299263, 0.008404696246705586, 0.008736548408580477], 'g': [0.03357339442700658, 0.007609673219578957, 0.030180576573708474, 0.021288825420328252, 0.019535834709898312], 'h': [0.020923132999307488, 0.18162166645768585, 0.020032464995366633, 0.020046474427408534, 0.07427940690908955], 'i': [0.0161420375564963, 0.07292311434908107, 0.14188878992940437, 0.0884896226750715, 0.0014922030927613896], 'j': [0.007586632464356645, 5.659266489315055e-05, 0.004743153004341199, 5.127724155142703e-05, 6.996555186751741e-06], 'k': [0.002996266597892234, 0.0037724272169065236, 0.0022640384696501216, 0.005302447615346849, 0.033679719215509454], 'l': [0.05004162596699969, 0.05807749059179589, 0.028196302381518032, 0.10150006524042887, 0.07023886364540362], 'm': [0.038448301379215254, 0.016508981305427602, 0.015420184568799393, 0.008297876367594634, 0.011827681983759952], 'n': [0.013748998060381892, 0.024594093844337712, 0.03814065969213122, 0.0773523962295662, 0.04566843077968735], 'o': [0.03973053164858823, 0.14699217303640905, 0.09306506509606371, 0.031092179837648257, 0.008528876940436232], 'p': [0.05787514542810564, 0.019966982461752523, 0.016593228317143664, 0.005754443578301863, 0.013975009643249731], 'q': [0.0066129905388348014, 0.0013887726801211583, 5.152206657740201e-06, 0.0003929332855775824, 8.917071501622165e-06], 'r': [0.03599758110698114, 0.10104644255119015, 0.08176271777192862, 0.09274086235611151, 0.1261834658136861], 's': [0.1138876294152568, 0.010755342929433392, 0.025572996787639954, 0.08361088013078923, 0.040311865952487765], 't': [0.12884147671513518, 0.06406273344236244, 0.0509062445881768, 0.05158215751988854, 0.132528688501334], 'u': [0.014550707530995705, 0.03702088986943911, 0.07532345507152566, 0.05558005770460576, 0.0002103319000931744], 'v': [0.015504219398826274, 0.01093708470704882, 0.022702858602573896, 0.01826981729780101, 1.521179494724562e-05], 'w': [0.09856227373985173, 0.007866168238458749, 0.006212522083013322, 0.002541011741813686, 0.008427127659641029], 'x': [8.987254675734994e-05, 0.0037209432342220515, 0.0023681815951437464, 0.00012844064918260894, 0.00278883451421783], 'y': [0.005919901771411889, 0.0024588049386474195, 0.007052163110984859, 0.0008118887511382391, 0.06408479489748085], 'z': [0.00012489884714017086, 0.00024203946123500114, 0.00062137135648064, 0.001236953961236005, 0.00021862874819565995]}
        self._manual = False
        self.console = Console()
        self._tried = []
        self.d = {}

    def restart_game(self):
        self._tried = []

    def entropy(self, word):
        prob = 0
        entropy = 0
        for i,letter in enumerate(word):
            prob = self.letter_probs[letter][i] 
            entropy += prob * np.log2(prob)
        return -entropy
    
    def highest_entropy(self):
        if self._tried == []:
            for word in self.word_list:
                word_entropy = self.entropy(word)
                self.d[word] = word_entropy
        return max(self.d, key=self.d.get)

    def filtered_list(self, result): 
        letters_guess = list(self.guess)
        for i,char in enumerate(result):
            if char == '-':
                for word in list(self.d):
                    if self.guess[i] not in list(word) or word[i] == self.guess[i]:
                        del self.d[word]
            if char == '+':
                for word in list(self.d):
                    if letters_guess.count(self.guess[i]) == 1:
                        if self.guess[i] in word:
                            del self.d[word]
                    else:
                        if self.guess[i] == word[i]:
                            del self.d[word]
            if char.isalpha():
                for word in list(self.d):
                    if word[i] != char:
                        del self.d[word]

    def get_guess(self, result):

        if self._manual=='manual':
            return self.console.input('Your guess:\n')
        else:
            if self._tried == []:
                self.guess = self.highest_entropy()
                self._tried.append(self.guess)
                self.console.print(self.guess)
            else:
                self.filtered_list(result)
                self.guess = self.highest_entropy()
                self._tried.append(self.guess)
                self.console.print(self.guess)
            return self.guess        