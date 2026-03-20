questions = {
    "DSA": [
        {
            "question": "What is the difference between a stack and a queue?",
            "ideal_answer": "A stack follows LIFO (Last In First Out) principle where the last element inserted is the first to be removed. Operations are push and pop. A queue follows FIFO (First In First Out) principle where the first element inserted is the first to be removed. Operations are enqueue and dequeue. Stack example: function call stack. Queue example: printer job scheduling."
        },
        {
            "question": "Explain Binary Search and its time complexity.",
            "ideal_answer": "Binary Search works on a sorted array by repeatedly dividing the search interval in half. We compare the target with the middle element. If target equals middle, we found it. If target is less, we search the left half. If target is greater, we search the right half. Time complexity is O(log n) because we halve the search space each step. Space complexity is O(1) for iterative and O(log n) for recursive."
        },
        {
            "question": "What is a Binary Search Tree and its properties?",
            "ideal_answer": "A Binary Search Tree is a binary tree where each node has at most two children. The left subtree of a node contains only nodes with keys less than the node's key. The right subtree contains only nodes with keys greater than the node's key. Both subtrees must also be BSTs. Average time complexity for search, insert, delete is O(log n). Worst case (skewed tree) is O(n)."
        },
        {
            "question": "What is dynamic programming? Give an example.",
            "ideal_answer": "Dynamic programming is an optimization technique that solves complex problems by breaking them into overlapping subproblems and storing their results to avoid recomputation. It uses memoization (top-down) or tabulation (bottom-up). Key conditions: optimal substructure and overlapping subproblems. Classic examples: Fibonacci sequence, 0/1 Knapsack, Longest Common Subsequence, Shortest Path problems."
        },
        {
            "question": "Explain the difference between BFS and DFS.",
            "ideal_answer": "BFS (Breadth First Search) explores all nodes at current depth before going deeper. It uses a queue and is best for finding shortest path in unweighted graphs. Time complexity O(V+E). DFS (Depth First Search) explores as far as possible along each branch before backtracking. It uses a stack or recursion and is best for detecting cycles, topological sort, maze solving. Time complexity O(V+E)."
        }
    ],
    "OS": [
        {
            "question": "What is a deadlock and what are the four conditions for it?",
            "ideal_answer": "Deadlock is a situation where two or more processes are stuck waiting for each other to release resources, causing all of them to be blocked forever. The four necessary conditions are: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, 4) Circular Wait."
        },
        {
            "question": "What is the difference between a process and a thread?",
            "ideal_answer": "A process is an independent program in execution with its own memory space and resources. A thread is the smallest unit of execution within a process. Multiple threads share the same memory space of their parent process. Threads are lighter, context switching is faster, and creating a thread is cheaper than creating a process."
        },
        {
            "question": "Explain paging in operating systems.",
            "ideal_answer": "Paging is a memory management scheme that eliminates contiguous allocation. Physical memory is divided into frames and logical memory into pages of the same size. The OS maintains a page table mapping pages to frames. Page faults occur when a page is not in memory. Paging eliminates external fragmentation but causes internal fragmentation."
        },
        {
            "question": "What is CPU scheduling and name some scheduling algorithms?",
            "ideal_answer": "CPU scheduling determines which process gets the CPU next. Common algorithms: FCFS (First Come First Serve), SJF (Shortest Job First), Round Robin (fixed time quantum), Priority Scheduling, and Multilevel Queue scheduling."
        },
        {
            "question": "What is virtual memory and why is it used?",
            "ideal_answer": "Virtual memory gives each process the illusion of a large private address space even if physical RAM is limited. It stores parts of a process on disk and loads them into RAM on demand (demand paging). Benefits include running programs larger than RAM, running multiple programs simultaneously, and memory isolation for security."
        }
    ],
    "DBMS": [
        {
            "question": "What is normalization? Explain 1NF, 2NF, 3NF.",
            "ideal_answer": "Normalization reduces redundancy and improves data integrity. 1NF: atomic values, no repeating groups. 2NF: 1NF + no partial dependencies on primary key. 3NF: 2NF + no transitive dependencies between non-key attributes."
        },
        {
            "question": "What is the difference between SQL and NoSQL databases?",
            "ideal_answer": "SQL databases are relational with fixed schemas, use structured tables, support ACID transactions, and scale vertically. NoSQL databases are non-relational with flexible schemas, scale horizontally, and follow BASE model. SQL suits complex queries; NoSQL suits big data and real-time web apps."
        },
        {
            "question": "What are indexes in databases and why are they used?",
            "ideal_answer": "An index is a data structure improving speed of data retrieval at the cost of extra writes and storage. Types include B-tree (range queries), Hash (equality checks), Composite (multiple columns). Indexes slow down INSERT, UPDATE, DELETE operations."
        },
        {
            "question": "What are ACID properties in databases?",
            "ideal_answer": "ACID: Atomicity (all or nothing transaction), Consistency (valid state transitions), Isolation (concurrent transactions appear sequential), Durability (committed transactions survive failures)."
        },
        {
            "question": "What is the difference between INNER JOIN and OUTER JOIN?",
            "ideal_answer": "INNER JOIN returns only matching rows from both tables. OUTER JOIN returns all rows from one or both tables. LEFT JOIN returns all left rows with matched right rows (NULL if no match). RIGHT JOIN is opposite. FULL OUTER JOIN returns all rows from both tables with NULLs where no match."
        }
    ],
    "HR": [
        {
            "question": "Tell me about yourself.",
            "ideal_answer": "Cover: brief background, technical skills and projects, what you are passionate about in tech, and why you are interested in this role. Be concise (90 seconds), confident, and tell a story showing your growth."
        },
        {
            "question": "What is your greatest weakness?",
            "ideal_answer": "Pick a real but non-critical weakness, show self-awareness, and describe concrete steps to improve it. Avoid cliches like 'I am a perfectionist'. Show that you are actively working on it."
        },
        {
            "question": "Describe a challenging project you worked on and how you handled it.",
            "ideal_answer": "Use STAR method: Situation, Task, Action, Result. Be specific about the technical challenge, mention teamwork, show problem-solving skills, and quantify results if possible."
        },
        {
            "question": "Where do you see yourself in 5 years?",
            "ideal_answer": "Show ambition aligned with the company. Mention growing into a senior/lead role, shipping impactful products, mentoring others, and how this role helps build that foundation."
        },
        {
            "question": "Why should we hire you?",
            "ideal_answer": "Connect your unique skills directly to job requirements with specific examples. Mention 2-3 technical strengths, your attitude as a fast learner and team player, and enthusiasm for this specific company."
        }
    ]
}
