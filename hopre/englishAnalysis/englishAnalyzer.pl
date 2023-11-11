/*========================================================================

    The following file has been based off of Prof. Jong Park's
	modification of BB1, written by Patrick Blackburn and Johan Bos.

    File: kellerStorage.pl
    Copyright (C) 2004,2005,2006 Patrick Blackburn & Johan Bos

========================================================================*/

:- module(englishAnalyzer, [infix/0,
                            prefix/0,
							       analyzeSentence/0,
							       analyzeSentence/2]).

:- use_module(readLine, [readLine/1]).

:- use_module(comsemPredicates,[memberList/2,
				                    appendLists/3,
				                    selectFromList/3,
				                    compose/3,
                                infix/0,
                                prefix/0,
				                    printRepresentations/1]).

:- use_module(alphaConversion,[alphabeticVariants/2]).

:- use_module(betaConversion,[betaConvert/2]).

:- [englishGrammar].

:- [englishLexicon].

:- [semLexLambda].

:- [semRulesLambda].


/*========================================================================
   Driver Predicates
========================================================================*/

analyzeSentence:-
   readLine(Sentence),
   setof(Sem,t([sem:Sem],Sentence,[]),Sems),
   printRepresentations(Sems).

analyzeSentence(Sentence,Sems):-
   setof(Sem,t([sem:Sem],Sentence,[]),Sems).


/*========================================================================
   Filter Alphabetic Variants
========================================================================*/

filterAlphabeticVariants(L1,L2):-
   selectFromList(X,L1,L3),
   memberList(Y,L3),
   alphabeticVariants(X,Y), !,
   filterAlphabeticVariants(L3,L2).

filterAlphabeticVariants(L,L).


/*========================================================================
   Info
========================================================================*/

info:-
   format('~n> ------------------------------------------------------------------- <',[]),
   format('~n> englishAnalyser.pl, by Patrick Blackburn and Johan Bos              <',[]),
   format('~n>                                                                     <',[]),
   format('~n> ?- analyzeSentence.          - parse a typed-in sentence            <',[]),
   format('~n> ?- analyzeSentence(S,F).     - parse a sentence and return formulas <',[]),
   format('~n> ?- infix.                    - switches to infix display mode       <',[]),
   format('~n> ?- prefix.                   - switches to prefix display mode      <',[]),
   format('~n> ?- info.                     - show this information                <',[]),
   format('~n> ------------------------------------------------------------------- <',[]),
   format('~n~n',[]).


/*========================================================================
   Display info at start
========================================================================*/

:- info.