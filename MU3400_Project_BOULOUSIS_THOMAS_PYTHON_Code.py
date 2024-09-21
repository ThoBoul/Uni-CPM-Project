#Copyright © 2022-2023 by Thomas Boulousis

#To run the code, the user needs to have installed mido and midiutil

#Install mido from this link: https://github.com/mido/mido/

#Install midiutil from this link: https://pypi.org/project/MIDIUtil/

import mido
from mido import MidiFile
import midiutil
from midiutil import MIDIFile
import math
import random
#Imports all the necessary modules

def MeanIntervalFinder(List): #finds the mean musical interval of a list which is defined as (Sum_of_all_melodic_intervals/No_of_intervals)
    SumInterval=0 #initialise the max interval
    for i in range (1,len(List)):
        SumInterval+=abs(List[i]-List[i-1]) #adds all the melodic intervals together
    return (SumInterval/len(List)) #returns the mean interval

def IntervalClosenessFunction(Interval,MeanInterval): #finds whether an interval is close to the mean interval
    if min(Interval,abs(MeanInterval-Interval))<=MeanInterval: #if the interval is smaller than the mean interval
        temp=(max(Interval,0.5)/max(min(Interval,abs(MeanInterval-Interval)),0.5))
        return temp*math.log(temp,math.e) #uses this function to determine how small or close to the mean interval an interval is
    else:
        return False #otherwise, it returns False

def FrequencyFinder(List,weight): #finds how many times an element appears in a list and returns a list with this formula [[element1,weight1],[[element2,weight2]...]
    List.sort() #first, it sorts the list
    templist=[] #initialise templist
    templist.append([List[0],(List.count(List[0])*weight)]) #appends the first element of the List as well as how many times it has appeared
    for i in range (1,len(List)):
        if not(List[i]==List[i-1]): #repeats the process for the rest of the elements
            templist.append([List[i],(List.count(List[i])*weight)])
    return templist #returns the list with the above formula

def ListCombination(List1,List2): #combines 2 lists that have the above formula ([[element1,weight1],[element2,weight2],...])
    for i in range (len(List2)): #for every element in List 2
        test=False #initialise test
        for j in range (len(List1)): #if the element exists in List 2, it adds the weight of that List (2) to List 1
            if List2[i][0]==List1[j][0]:
                List1[j][1]+=List2[i][1]
                test=True
        if test==False: #else, it appends it to List 1
            List1.append(List2[i])
    return List1 #returns the new, combines List 1

def QuasiMarkovChain(TheLIST,weight): #the analysis part / TheLIST is the list of notes or rhythms, weight is a modifier (will be explained in more detail below)
    templist=[]
    frequencylist=[]
    weightlist=[]
    for i in range (len(TheLIST)-4):
        templist.append([TheLIST[i],TheLIST[i+1],TheLIST[i+2],TheLIST[i+3],TheLIST[i+4]]) #appends all the combinations of 5 subsequent elements of TheLIST to templist
    for i in range (len(templist)): #iterates through every index of templist and appends it to weightlist using this formula [templist[i]=element,1=no_of_appearances]
        weightlist.append([templist[i],1])
        for j in range (len(templist)):
            if templist[i]==templist[j] and not(i==j): #iterates through every index of templist and adds 1 to weightlist[i][1] every time there is a repetition of it in the list
                weightlist[i][1]+=1     #this way, every small list inside weightlist contains [element, times_it_has_appeared]
    index=0
    while index<len(weightlist): #however, we now have multiple repetitions of the same small list inside weightlist
        index2=0
        while index2<len(weightlist): #so, for every index in weightlist (the length of the list gets smaller, so we cannot use the for ... in loop)
            if weightlist[index][0]==weightlist[index2][0] and not(index==index2): #we iterate through the entire list and delete every repetition
                del weightlist[index2]
            index2+=1
        index+=1
    for i in range (len(weightlist)): #then, the program goes through every times_it_has_appeared and multiplies it with the weight modifier
        weightlist[i][1]*=weight #this way, the program counts as if it has read through the file #WEIGHT times, and thus has a higher (or lower) chance of using the analysis of said file  
                                 #of course, for this to work properly, we need to feed the program at least 2 files
    frequencylist=FrequencyFinder(TheLIST,weight) #finds the frequency of every single note or rhythm as well
    return weightlist,frequencylist #returns weightlist and frequencylist (the number_of_appearances*weight of every single note)

def MIDIRead(filename):
    mid=MidiFile(filename) #sets up the mido MidiFile
    Notelist=[]
    Rhythmlist=[]
    for msg in mid.tracks[len(mid.tracks)-1]:
        if not(msg.is_meta):
            if msg.type=='note_on': #if the note is on, we get the pitch
                Notelist.append(msg.note)
    for msg in mid.tracks[len(mid.tracks)-1]:
        if not msg.is_meta:
            if msg.type=='note_off': #if the note is off, it means we can get the rhythmic value
                Rhythmlist.append(msg.time/mid.ticks_per_beat)
            elif msg.type=='note_on' and not msg.time==0: #if the note is on but there is some distance between this note and the previous, then we get a rest
                Rhythmlist.append((-1)*msg.time/mid.ticks_per_beat) #this program counts rests as the negative of a rhythmic value (it always uses absolute value later on to determine length)
    return Notelist,Rhythmlist #we return Notelist and Rhythmlist

def ListSimilarity(ListA, ListB): # determines if 2 lists are similar, i.e. they begin and end the same way, have at least n-1 elements in common (where n is their length)and the elements of ListB aren't too far off those of ListA 
    if len(ListA)==len(ListB):#checks whether 2 lists have the same length/ if they do, it continues
        temp=0
        Similar=True #assumes the 2 lists are similar
        average_interval=MeanIntervalFinder(ListA) #finds the mean interval of ListA
        for i in range (len(ListA)): #iterates through every element of ListA
            if ListA[i]==ListB[i]: #if the corresponding elements of ListA and B are equal, then it increases temp by 1
                temp+=1
            else: #else, if said elements aren't the first or last elements of the lists and their difference is smaller or equal to the average interval
                if abs(ListA[i]-ListB[i])<=average_interval and not(i==0 or i==len(ListA)-1):
                    Similar=True #it keeps the similar variable as True, but does not increase temp
                else:
                    Similar=False #in any other case,it changes the similar variable to Falce
        if (temp==len(ListA) or temp==(len(ListA)-1) and Similar==True): #in case temp is equal to n or n-1 (where n is len(ListA)) and Similar=True, then Similar remains true
            Similar=True
        else: #else, similar becomes False
            Similar=False
        return Similar, (1/(1+(len(ListA)-temp))) #The program then returns the Similarity, as well as a number which becomes 1 if they are literally the same, or 1/2 if they only have 1 difference
    else: #if 2 lists don't have the same length, they aren't similar, so it returns False,0
        return False, 0

def NewRhythm_Note(CompositionList,MarkovChainValueFrequency,Valuelist,Valueweights,MeanInterval): #generates new notes/rhythms based on previous notes/rhythms
    #CompositionList: the list of the generated composition thus far
    #MarkovChainValueFrequency: the 1-note/rhythm analysis of the QuasiMarkovChain function
    #Valuelist and Valueweights: 2 lists where each corresponding indexes hold the specific 5-value (pitch or rhythm) as well as its weight respectively
    #MeanInterval: The average interval of a melody as specified by the MeanIntervalFinder function. If it equals -1, it automatically understands we are writing rhythms and not melodies. 
    potentialvalues=[] #Initiates these 2 lists
    valueweights=[]
    for index in MarkovChainValueFrequency:#Splits the MarkovChainValueFrequency list into values and weights accordingly (index[0]=value, index[1]=weight)
        potentialvalues.append(index[0]) 
        valueweights.append(index[1])

    templist=[CompositionList[len(CompositionList)-1],CompositionList[len(CompositionList)-2],CompositionList[len(CompositionList)-3],CompositionList[len(CompositionList)-4]]
    #Makes a temporary list of the 4 previous notes of the composition thus far (!the program makes sure later on to always have at least 4 notes before using this function!) 
    for i in range (len(Valuelist)):#iterates through every index of Valuelist
        templist2=[Valuelist[i][0],Valuelist[i][1],Valuelist[i][2],Valuelist[i][3]] #makes a temporary list with the 4 out of the 5 elements on each given index of Valuelist
        if ListSimilarity(templist,templist2)[0]==True: #compares the above templist (templist2) with the templist containing the 4 previous notes of the composition thus far using the ListSimilarity function
                for i in range (len(potentialvalues)): #if they are similar, it iterates through all indexes of potentialvalues
                    if potentialvalues[i]==Valuelist[i][4]: #and compares it to the 5th element (index 4) the same index of Valuelist
                        valueweights[i]+=Valueweights[i]*ListSimilarity(templist,templist2)[1] #if they are the same, it adds the weight of the corresponding index of Value weights multiplied by the similarity modifier (either 1 or 1/2)
#IMPORTANT: This way, the number of appearances of each value (pitch or rhythm) individually is combined with its appearance as the 5th of every 5-value combination that's similar to the last 4-value combination of the composition thus far
                        if not (MeanInterval==-1 and IntervalClosenessFunction((CompositionList[len(CompositionList)-1]-Valuelist[i][4]),MeanInterval)==False):
                            #In case MeanInterval isn't -1, which means we are dealing with a melody, the weight of the value is also modified by how close to the mean interval it is                            
                            valueweights[i]+=valueweights[i]*IntervalClosenessFunction((CompositionList[len(CompositionList)-1]-Valuelist[i][4]),MeanInterval)
    return potentialvalues,valueweights #the program then returns a list with all the potential next values, as well as a list containing a weight for each corresponding index of potentialvalues

def NewMIDI_Generator(MarkovChainRhythm,MarkovChainNoteValueFrequency,MarkovChainMelody,MarkovChainNoteFrequency,MeanInterval,maxlength,output_filename):
    #The composition-generator function
    #MarkovChainRhythm/MarkovChainMelody: the 5-rhythm/note analysis
    #MarkovChainNoteValueFrequency/MarkovChainFrequency: the individuel rhythm/note analysis
    #MeanInterval: the mean interval
    #maxlength: the user specified length of the new composition
    #output_filename: the user speicified filename    
    MyMIDI = MIDIFile(1) #Generates the new MIDI file
    
    print("Give tempo") #Asks for tempo
    tempo=int(input())
    while tempo<=40 or tempo>=160: #Checks whether tempo is appropriate
        print("Please give an appropriate tempo")
        tempo=int(input())
    MyMIDI.addTempo(0,0, tempo) #Adds the tempo
    
    #Generating rhythm
    Rhythmlist=[] #initiates these 2 lists
    Rhythmweight=[]

    for index in MarkovChainRhythm: #MarkovChainRhythm is a list formed with this formula [[[a,b,c,d,e],weight1],[[b,c,d,e,f],weight2],...]
        Rhythmlist.append(index[0]) #Appends the index[0] of each index of MarkovChainRhythm ([[a,b,c,d,e],[b,c,d,e,f],...])
        Rhythmweight.append(index[1]) #Appends the index[1] of each index of MarkovChainRhythm ([weight1,weight2,..])
                                        #this way, each corresponding index Rhythmlist and Rhythmweight contains the 5-note rhythm and it's appropriate weight accordingly
    Rhythms=random.choices(Rhythmlist,Rhythmweight) #chooses 1 random 5-rhythm sequence from Rhythmlist, using the appropriate Rhythmweights, and appends it to the Rhythms list 
    Rhythms=Rhythms[0]#because the 5-rhythm list will be a list in itself, we need that list to actually become the whole list (i.e. make it so this [[a,b,c,d,e]] becomes this [a,b,c,d,e])

    length=0
    for index in Rhythms:
        length+=abs(index) #calculates the length in beats by adding up all the rhythmic values thus far

    while length<=(4*maxlength): #it then repeats the following process until length is roughly equal to maxlength (in bars) * 4 (to convert it to beats)
        templist=NewRhythm_Note(Rhythms,MarkovChainNoteValueFrequency,Rhythmlist,Rhythmweight,-1) #uses the NewRhythm_Note function to calculate the weights of each rhythm based on the composition thus far (!the mean interval = -1 to specify we are working with rhythms)
        Rhythms.append(random.choices(templist[0],templist[1])) #appends 1 rhythm to the Rhythms list based on the above analysis
        Rhythms[len(Rhythms)-1]=Rhythms[len(Rhythms)-1][0] #similar to above, new rhythm comes inside a list, which needs to be eliminated
        length+=abs(Rhythms[len(Rhythms)-1]) #adds the new rhythmic value to length  
    
    #Generating melody
    Melodylist=[] #similarly to above, it initiates these 2 lists
    Melodyweight=[]

    for index in MarkovChainMelody: #then splits MarkovChainMelody
        Melodylist.append(index[0])
        Melodyweight.append(index[1])

    test=0 #calculates the index of the fourth non-negative rhythmic value (i.e. actual note and not rest)
    index=0
    while test<4: 
        if Rhythms[index]>0:
            test+=1 #1 is added to test every time the index is positive
        index+=1
        
    Melody=random.choices(Melodylist,Melodyweight) #then it adds a 5-note motif from the Melodylist, similarly to what is done with the rhythm
    Melody=Melody[0] #eliminates the list inside the list
    
    for i in range ((index-1),len(Rhythms)): #iterates for every element in Rhythms after the final index-1  
        if Rhythms[i]>0: #in case each index in rhythms is positive 
            templist=NewRhythm_Note(Melody,MarkovChainNoteFrequency,Melodylist,Melodyweight,MeanInterval) #uses the NewRhythm_Note function to find the probability of every note according to the composition thus far
            Melody.append(random.choices(templist[0],templist[1])) #appends a note using the weights from above
            Melody[len(Melody)-1]=Melody[len(Melody)-1][0] #eliminates the melody
            
    index=0 #initiates index (again) and time variables
    time=0
    for rhythm in Rhythms: #iterates through every element in Rhythms, and if it is positive, it adds the corresponding pitch then increases the time variable, otherwise it only increases the time variable (thus calculating the rests)
        if rhythm>0:
            MyMIDI.addNote(0,0,Melody[index],time,rhythm,100)
            index+=1
        time+=abs(rhythm)
        
    with open((output_filename) + '.mid', "wb") as output_file: #exports the output file
        MyMIDI.writeFile(output_file)
    print('Finished!') #notifies the user that the generating process has finished

MarkovChainMelody=[]#initiates these 5 lists
MarkovChainRhythm=[]
MarkovChainNoteFrequency=[]
MarkovChainNoteValueFrequency=[]
Filename=[]
#A possible future expansion might include the ability to import already filled MarkovChainMelody/Rhythm/NoteFrequency/NoteValueFrequency lists in order to expand on previously analysed data

test=''#initiates test
while not(test.capitalize()=='Stop'):#as long as the user hasn't told it to stop, the program continues to ask for filenames, which are appended to the Filename list
    print ("Give me a filename")
    filename=str(input())
    print ("Give a weight") 
    weight=int(input())
    Filename.append([filename,weight]) #filename is stored as index[0] of each index of Filename, and weight as index[1]
    print ("Tell me if I should stop")
    test=str(input())

MeanInterval=[]#initiates the MeanInterval list, which will initially contain all the mean intervals of all the files, of which the mean interval of all of them will be found and stored in it
for filename in Filename: #iterates through every index in Filename 
    templist=MIDIRead(filename[0])#the MIDIRead function to read the file, getting a list that has the notes in index 0 and the rhythms in index 1

    if len(templist[0])>4: #only if the melody is longer than 4 notes, it does the rest
        TempMarkovChainMelody=QuasiMarkovChain(templist[0],filename[1]) #uses the QuasiMarkovChain (filename[1]=weight)
    
        TempMarkovChainRhythm=QuasiMarkovChain(templist[1],filename[1]) #for both melody and rhythm
        
        MarkovChainMelody=ListCombination(MarkovChainMelody,TempMarkovChainMelody[0]) #it then combines the previous iteration of MarkovChainMelody (in case it's the first iteration, the list is empty) with the new temporary MarkovChainMelody 
        MarkovChainRhythm=ListCombination(MarkovChainRhythm,TempMarkovChainRhythm[0]) #same for rhythm
    
        MarkovChainNoteFrequency=ListCombination(MarkovChainNoteFrequency,TempMarkovChainMelody[1])#same for the 1-note combinations
        MarkovChainNoteValueFrequency=ListCombination(MarkovChainNoteValueFrequency,TempMarkovChainRhythm[1])

        MeanInterval.append(MeanIntervalFinder(templist[0]))#it then finds the average interval of the list of notes and appends it to the MeanInterval list

MeanInterval=MeanIntervalFinder(MeanInterval)#it then finds the MeanInterval from all the average intervals in MeanInterval

print("Give maxlength in bars") #asks for the max length in bars
maxlength=int(input())
print("Give output_filename") #asks for an output filename
output_filename=str(input())
#uses the NewMIDI_Generator to generate a new MIDI file
NewMIDI_Generator(MarkovChainRhythm,MarkovChainNoteValueFrequency,MarkovChainMelody,MarkovChainNoteFrequency,MeanInterval,maxlength,output_filename)

#the NewMIDI_Generator function is easy to use again on the same python shell to generate more melodies
