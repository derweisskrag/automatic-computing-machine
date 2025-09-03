import timeit
from count_to_billion import count_to_billion

# It is highly recommended to use a smaller number of iterations
# for a function that takes a long time to run.
# For example, let's time a single run of your function.
# timeit.timeit(stmt, setup, number)
# stmt: The code statement to be measured.
# setup: The code to run once before the measurement (e.g., imports).
# number: The number of times to run the statement.

# The function you want to benchmark
stmt_to_run = "count_to_billion()"

# A small setup string to import the function
setup_string = "from count_to_billion import count_to_billion"

# Run the benchmark. We'll only run it once since it's a long operation.
# The result will be the total time for the single run.
total_time = timeit.timeit(stmt_to_run, setup=setup_string, number=1)

print(f"The 'count_to_billion' function took {total_time:.2f} seconds to run once.")