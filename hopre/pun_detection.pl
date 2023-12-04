:-use_module(library(lists)).

replace(Lin,Phrase1,Phrase2,Lout):-
   append([Front,Phrase1,Back],Lin),
   append([Front,Phrase2,Back],Lout).

allTexts([]).
allTexts([Sentence|Rest]):-
   lambda:t(_,Sentence,[]),
   allTexts(Rest).

homonymPun(Sentences):-
   allTexts(Sentences),
   append(Sentences,AllWords),
   append([_,HomonymPhrase,_],AllWords),
   append([_,Context1,_],AllWords),
   similar(HomonymPhrase,Context1),
   append([_,Context2,_],AllWords),
   similar(HomonymPhrase,Context2),
   dissimilar(Context1,Context2).