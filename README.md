# Uni-CPM-Project
For my project for City St George's, University of London MU3400 Computer Programming for Musicians I attempted to create a Python script capable of analysing, learning from, and then generating new MIDI files.


Thomas Boulousis Student number: 200023242
MU3400 Computer Programming for Musicians Module leader: Dr Erik Nyström
Project Commentary

For my project for MU3400 Computer Programming for Musicians I attempted to create a Python script capable of analysing, learning from, and then generating new MIDI files. I thus incorporated a data structure similar to a Markov Chain, i.e. a set of states whose probability of occurring in the future depends only on the present.1 However, since past musical happenings do affect the future, I decided to treat a set of five adjacent individual states as one state.

A single musical state means a single musical note or rhythm. Using this model of data analysis, the algorithm can determine the rate of appearance of each 5-element state and each single-element state (see QuasiMarkovChain function), as well as the average melodic interval of the file (see MeanIntervalFinder function). To read the contents of a MIDI file, I used the Python module mido.2 A currently significant limitation of this model, one I would like to tackle in the future, lies in its inability to read more than one musical line at a time.
Following the analysis, the program can utilise the above-mentioned data, as well as the math module, to derive the probability of a specific note or rhythm appearing as the fifth element of any given 5-element state. Using the random module, the program can then employ those probabilities to fill-in said fifth element and repeat this process as many times as necessary to generate a new melodic line, which can then be exported as a MIDI file using the MIDIUtil module.3 As a test, I fed the program two MIDI files of the popular Christmas song “Jingle Bells”, one in C major and one in D major, in order to inspect how it would interact with the two key signatures.
Project due date: 12 January 2023


REFERENCES
BJØRNDALEN, Ole Martin (lead programmer) and other contributors (2013). Mido - MIDI Objects for Python. <https://mido.readthedocs.io/en/latest/> (Date last accessed: 4 January 2023).
MIDIUtil. Python Package Index (PyPI) by Python Software Foundation. <https://pypi.org/project/MIDIUtil/> (Released: 4 March 2018, Date last accessed: 4 January 2023).
SERFOZO, Richard (2009). Basics of Applied Stochastic Processes. Springer-Verlag Berlin, Heidelberg.

