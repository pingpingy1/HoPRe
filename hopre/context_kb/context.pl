:- module(context,[similar/2,
                   dissimilar/2]).

/*========================================================================
   Similar(=contextually relevant) phrases
========================================================================*/

similar([dressing],[salad]).

similar([dressing],[turn,red]).

similar([problems],[math]).

similar([problems],[sad]).

similar([jump],[frog]).

similar([jump],[car]).

similar([windows],[computer]).

similar([windows,open],[cold]).

similar([virus],[computer]).

similar([virus],[doctor]).

similar([peeling],[banana]).

similar([not,feeling,well],[doctor]).

similar([hole],[two,pairs]).

similar([hole-in-one],[golfer]).

similar([byte],[computer]).

similar([bite],[doctor]).


/*========================================================================
   Dissimilar(=contextually incongruent) phrases
========================================================================*/

dissimilar([turn,red],[salad]).

dissimilar([math],[sad]).

dissimilar([frog],[car]).

dissimilar([computer],[cold]).

dissimilar([computer],[doctor]).

dissimilar([banana],[doctor]).

dissimilar([golfer],[two,pairs]).
