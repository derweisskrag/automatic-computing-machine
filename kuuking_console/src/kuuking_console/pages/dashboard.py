def dashboard(todo_queue, tasks, migrated=0):
    if migrated == 0:
        print("[BURMESE PRINTS 🐍]: Inspecting DEFAULT CLUSTER...\n")
        todo_queue.print_queue()

        print("\n[BURMESE PRINTS 🐍]: Inspecting DAILY CLUSTERS...\n")
        print(f"\t Cluster 1: {'  |  '.join(map(str, tasks.get(1, [])))}\n")
        print(f"\t Cluster 2: {'  |  '.join(map(str, tasks.get(2, [])))}\n")
        print(f"\t Cluster 3: {'  |  '.join(map(str, tasks.get(3, [])))}\n")
        print(f"\t Cluster 4: {tasks.get(4)}\n")
    else:
        print("\n[BURMESE PRINTS 🐍]: Inspecting DEFAULT RUST CLUSTER... 🦀\n")
        print("\tEmpty now")