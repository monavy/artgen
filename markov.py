# http://charlesleifer.com/blog/building-markov-chain-irc-bot-python-and-redis/
# http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/

import random


class Markov():
    def __init__(self):
        self.data = {}
        self.starters = []
        self.chain_length = 2

    def __parse_words(self, words):
        words.append(None)

        for i in range(len(words) - self.chain_length):
            key = tuple(words[i:i+self.chain_length])
            if key in self.data:
                self.data[key].append(words[i + self.chain_length])
            else:
                self.data[key] = []
                self.data[key].append(words[i + self.chain_length])

    def __parse_line(self, line):
        words = line.split()

        if len(words) > self.chain_length:
            key = tuple(words[0:self.chain_length])
            self.starters.append(key)
            self.__parse_words(words)

    def load_from_string(self, string):
        for line in string.split('\n'):
            self.__parse_line(line)

    def load_from_file(self, filename):
        for line in open(filename, 'r'):
            line = line.strip()
            self.__parse_line(line)

    def generate_text(self, pcount):
        # Create pcount paragraphs.
        text = ''
        for i in xrange(pcount):
            text += self.generate_paragraph() + '\n\n'

        return text

    def generate_paragraph(self, m, x):
        scount = random.randint(m, x)
        text = ''
        for i in xrange(scount):
            text += self.generate_sentence() + ' '

        return text

    def generate_sentence(self):
        key = random.choice(self.starters)
        words = []

        # Add the starter to the sentence
        for w in key:
            words.append(w)

        # Get the next word for our sentence
        next = random.choice(self.data[key])

        # Keep adding words until next is None.
        while next is not None:
            words.append(next)
            newkey = list(key[1:])
            newkey.append(next)
            key = tuple(newkey)
            next = random.choice(self.data[key])

        return ' '.join(words)

if __name__ == '__main__':

    text = '''
        The quick brown fox jumped over the spoon.
        The cow jumped over the moon.
        The dish ran away with the spoon.
    '''

    m = Markov()
    m.load_from_string(text)

    print m.starters
    print
    print m.data

    print 'Sentence:'
    print m.generate_sentence()
    print
    print 'Paragraph:'
    print m.generate_paragraph()
    print
    print 'Text:'
    print m.generate_text(2)
