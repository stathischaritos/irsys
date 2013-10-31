The goal of this assignment is to get an understanding of all things involved in a real information retrieval system. To this end you are expected to build your own basic IR system and to execute a small-scale experiment using your system. The assignment can be done in teams of up to three people and the system can be build in any programming language you want (as long as we can run it too). The deadline for this assignment is at the end of the course (Sunday Dec. 22 at 23:59), but groups are encouraged to keep me updated on their progress. There is an intermediate deadline on Sunday Nov. 24 at 23:59 for the index test mentioned below (step 2). Groups hand in two things in the end: (1) a short report describing the experiment (pdf, ~3 pages) and (2) the (runnable) code of the IR system. Finally, the files needed for the assignment (document collection, queries, judgements) will be added shortly.

To get to the final retrieval system and the experiments, you will need to go through these steps.

1. Preprocess collection
Your system should be able to preprocess a collection of text documents, so that the output can be stored in an inverted index. The minimally required preprocessing steps are tokenization and normalization, but you can also incorporate other steps like stemming and stopword removal. Before implementing a lot of things of your own, try and search for modules that can help you. For Python, for example, the nltk toolkit offers a lot of text processing functions. The document collection used in this assignment is part of the CSIRO collection (262 documents), but it already partially preprocessed. The original collection consists of HTML documents from the internal CSIRO website (see "CSIRO collection description" for a short collection description), the version we offer here has most HTML removed and contains only the body parts of the HTML files.

2. Index documents
The output of the preprocessing step should be stored in an inverted index. Given the programming language you use, pick an appropriate way of storing the index, so that in a later stage the retrieval models can use this index easily. As a test you are asked to output some basic statistics of the index (total number of tokens, unique tokens, total count of the token "of"). Documents are stored using their documentID, which is the filename minus .txt.

3. Implement retrieval models
Your IR system should support two retrieval models. Which models you add is up to you, but we will look at the complexity of the models in grading the assignment (a Boolean model is easier to implement than language models). Unlike step 1, here you do really need to come up with your own implementation to fully understand the models. Also, since the two models are used to run the experiment, it makes sense to have two models that differ to such a degree that you might actually observe differences in scores. If you have one or two models that use parameters (e.g., BM25 or LMs), you could also consider running an additional experiment in which you explore the impact of parameter settings.

4. Run queries
The IR system should be able to take a query as input and rank the documents according to the implemented retrieval models. To make things run smoothly, it might make most sense to develop the system in such a way that it only needs to index all documents once and you can run all queries and all models in one go. We only require the system to "answer" two queries:
queryID: 6
query: sustainable ecosystems
queryID: 7
query: air guitar textile sensors

4. Generate and evaluate output
Your system should be able to generate the final ranking for a query. This ranking, plus the judgements (which documents are relevant for this query) are used as input for an online evaluation system, which generates the retrieval results for the model that generated the ranking. For evaluation you can use http://thetrecfiles.nonrelevant.net/ which is an online evaluator. You provide it with qrels (judgements) and the ranking your system produced. Each line in the ranking is formatted as follows:

<queryID> Q0 <documentID> <rank> <score> <runID>

Note that "Q0" is an actual string, which is there for legacy reasons. <queryID> should match the queryID in the judgements, while <documentID> is the filename minus .txt. The <score> is used by the evaluator to rank the documents, so make sure the top document has the highest score (it is more important than rank). <runID> could be anything, but you could use it to indicate which model was used to generate the ranking.

5. Report
Write a small report on the experiment you did (which models did you use and which parameter setting did you use?) and the outcomes (which model performs better? which metrics did you use? can you explain the differences?). 