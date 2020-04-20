import search_algorithm as dbs
import time

query_topic = input("Input query topic: ")
num_of_results = input("Input desired number of results: ")
query_politicians = input("Input list of politicians: ")
start_time = time.time()
dbs.get_top_n_related(query_topic, num_of_results, query_politicians)
execution_time = time.time() - start_time
print("Excution time: " + str(execution_time))
