# python program/estimate_params.py ../hw2b-files/network-grid10x10-t10.txt ../hw2b-files/training-grid10x10-t10.txt cpd-grid10x10-t10.txt
# rm queryResult.txt

./program/bayes_query_sp ../hw2b-files/network-grid10x10-t10.txt ../hw2b-files/cpd-grid10x10-t10.txt ../hw2b-files/cliquetree-grid10x10-t10.txt modified-queries-grid10x10-t10.txt

# pypy program/bayes_query_sp.py hw2b-files/network-grid10x10-t10.txt hw2b-files/cpd-grid10x10-t10.txt program/cliquetree-grid10x10-t10.txt hw2b-files/queries-grid10x10-t10.txt

# pypy program/bayes_query_sp.py hw2b-files/network-grid10x10-t100.txt hw2b-files/cpd-grid10x10-t100.txt program/cliquetree-grid10x10-t100.txt hw2b-files/queries-grid10x10-t100.txt

# pypy program/bayes_query_sp.py hw2b-files/network-grid10x10-t1000.txt hw2b-files/cpd-grid10x10-t1000.txt program/cliquetree-grid10x10-t1000.txt hw2b-files/queries-grid10x10-t1000.txt

# pypy program/bayes_query_sp.py hw2b-files/network-grid15x15-t100.txt hw2b-files/cpd-grid15x15-t100.txt program/cliquetree-grid15x15-t100.txt hw2b-files/queries-grid15x15-t100.txt


# ../hw2b-files/network-grid10x10-t1000.txt cpd-grid10x10-t1000.txt cliquetree-grid10x10-t1000.txt ../hw2b-example_queries_results/queries-grid10x10-t1000.txt