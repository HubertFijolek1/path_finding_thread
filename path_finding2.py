import queue
import time 
import threading

def createMaze():
    maze = []
    maze.append(["#","#", "#", "#", "#", "O","#"])
    maze.append(["#"," ", " ", " ", "#", " ","#"])
    maze.append(["#"," ", "#", " ", "#", " ","#"])
    maze.append(["#"," ", "#", " ", " ", " ","#"])
    maze.append(["#"," ", "#", "#", "#", " ","#"])
    maze.append(["#"," ", " ", " ", "#", " ","#"])
    maze.append(["#","#", "#", "#", "#", "X","#"])

    return maze

def createMaze2():
    maze = []
    maze.append(["#","#", "#", "#", "#", "O", "#", "#", "#"])
    maze.append(["#"," ", " ", " ", " ", " ", " ", " ", "#"])
    maze.append(["#"," ", "#", "#", " ", "#", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", " ", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", "#", "#"])
    maze.append(["#"," ", " ", " ", " ", " ", " ", " ", "#"])
    maze.append(["#","#", "#", "#", "#", "X", "#", "#", "#"])
    

    return maze


def printMaze(maze, path=""):
    for x, pos in enumerate(maze[0]):
        if pos == "O":
            start = x

    i = start
    j = 0
    pos = set()
    for move in path:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        pos.add((j, i))
    
    for j, row in enumerate(maze):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("+ ", end="")
            else:
                print(col + " ", end="")
        print()
        


def valid(maze, moves):
    for x, pos in enumerate(maze[0]):
        if pos == "O":
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

        if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif (maze[j][i] == "#"):
            return False

    return True


def findEnd(maze, moves):
    for x, pos in enumerate(maze[0]):
        if pos == "O":
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

    if maze[j][i] == "X":
        print("Found: " + moves)
        time.sleep(1)
        printMaze(maze, moves)
        return True

    return False


# MAIN ALGORITHM
def main2(job_id, num_requests):
    nums = queue.Queue()
    nums.put("")
    add = ""
    maze  = createMaze2()
    start_job = time.time()
    print(f"CPU-bound sub-job {job_id} started.")
    for _ in range(num_requests):
        time.sleep(2)

    while not findEnd(maze, add): 
        add = nums.get()
        #print(add)
        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(maze, put):
                nums.put(put)
    duration = time.time() - start_job
    print(f"CPU-bound sub-job {job_id} finished in {duration:.2f} seconds.")

def run_with_threads(n_jobs, num_requests):
    threads = []
    for id in range(n_jobs):
        # `args` is a tuple specifying the positional arguments for the
        # target function, which will be run in an independent thread.
        thread = threading.Thread(target=main2, args=(id, num_requests))
        threads.append(thread)
        thread.start()

    for thread in threads:
        # With `join`, we wait until the thread terminates, either normally
        # or through an unhandled exception.
        thread.join()

start_one_thread = time.time()
run_with_threads(n_jobs=1, num_requests = 15)
duration = time.time() - start_one_thread
print(f"CPU-bound job finished in {duration:.2f} seconds with a single thread.")

start_five_threads = time.time()
# Run with three threads with a smaller number. The total number of three threads
# adds up to the one of a single thread so the result is comparable.
run_with_threads(n_jobs=5, num_requests=3)
duration = time.time() - start_five_threads
print(f"CPU-bound job finished in {duration:.2f} seconds with five threads.")