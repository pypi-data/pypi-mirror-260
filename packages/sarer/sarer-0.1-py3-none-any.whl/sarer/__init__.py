def hot():
    print(
    """
disks = int(input("Enter no of disks : "))
ini = 'X'
fin = 'Z'
through = 'Y'
def hanoi(n, ini, fin, through):
    if n > 0:
        hanoi(n-1, ini, through, fin)
        print('Move the disk from', ini, ' to ', fin)
        hanoi(n-1, through, fin, ini)
hanoi(disks, ini, fin, through)
    """)
def pbc():
    print("""
total: int=int(input('Enter no. of bananas at starting :'))
distance=int(input('Enter distance you want to cover :'))
load_capacity=int(input('Enter max load capacity of your camel :'))
lose=0
start=total
for i in range(distance):
    while start>0:
        start=start-load_capacity

        if start==1:
            lose=lose-1
        lose=lose+2
    lose=lose-1
    start=total-lose
    if start==0:
        break
print("Maximum no of bananas delivered:",start)

""")
def pac():
    print("""
ans=list()
def ab():
  for s in range (0,10):
    for e in range (0,10):
      for n in range (0,10):
        for d in range (0,10):
          for m in range (0,10):
            for o in range (0,10):
              for r in range (0,10):
                for y in range (0,10):
                  if len(set([s,e,n,d,m,o,r,y]))==8:
                    send=s*1000+e*100+n*10+d
                    more=m*1000+o*100+r*10+e
                    money=m*10000+o*1000+n*100+e*10+y
                    if send+more==money:
                      ans.append((send,more,money))
  return ans
ab()
n=len(ans)
print(ans[n-1])
""")
def cg():
    print("""
import networkx as nx
import matplotlib.pyplot as plt
def is_safe(v, graph, color, c):
  for i in range(len(graph)):
    if graph[v][i] == 1 and color[i] == c:
      return False
  return True

def graph_coloring_util(graph, m, color, v):
  if v == len(graph):
    return True
  for c in range(1, m + 1):
    if is_safe(v, graph, color, c):
      color[v] = c
      if graph_coloring_util(graph, m, color, v + 1):
        return True
      color[v] = 0
  return False

def graph_coloring(graph, m):
  color = [0] * len(graph)
  if not graph_coloring_util(graph, m, color, 0):
    print("Solution does not exist")
    return
  print("Solution exists. Following are the assigned colors:")
  for i in range(len(graph)):
    print(f"Vertex {i + 1}: Color {color[i]}")
  edges = []
  for i in range(len(graph)):
    for j in range(i + 1, len(graph[i])):
      if graph[i][j] == 1:
        edges.append((i, j))
        
  G = nx.Graph()
  G.add_edges_from(edges)
  pos = nx.spring_layout(G)
  print(color)
  print(edges)
  node_colors = [f'C{c}' for c in color]
  nx.draw(G, pos, with_labels=True, node_color=node_colors,
          cmap=plt.cm.rainbow, node_size=200)
  plt.rcParams['figure.figsize'] = [10, 10]
  plt.show()
if __name__ == "__main__":
  graph = [
      [0, 1, 1, 0, 0, 0, 0],
      [1, 0, 1, 4, 0, 0, 0],
      [1, 1, 0, 1, 1, 1, 0],
      [0, 1, 1, 0, 1, 0, 0],
      [0, 0, 1, 1, 0, 1, 0],
      [0, 0, 1, 0, 1, 0, 1],
      [0, 0, 0, 0, 0, 1, 0]
  ]
  m = 3
  graph_coloring(graph, m)
""")
def sfb():
    print("""
graph = {
    'A' : ['B','C'],
    'B' : ['D', 'E'],
    'C' : ['F'],
    'D' : [],
    'E' : ['F'],
    'F' : []
}
visited = [] # List to keep track of visited nodes.
queue = [] #Initialize a queue
def bfs(visited, graph, node):
    visited.append(node)
    queue.append(node)
    while queue:
        s = queue.pop(0)
        print (s, end = " ")
        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
                # Driver Code
bfs(visited, graph, 'A')
""")
def sfd():
    print("""
graph = {
    'A' : ['B','C'],
'B' : ['D', 'E'],
'C' : ['F'],
'D' : [],
'E' : ['F'],
'F' : []
}
visited = set() # Set to keep track of visited nodes.
def dfs(visited, graph, node):
  if node not in visited:
    print (node)
    visited.add(node)
    for neighbour in graph[node]:
      dfs(visited, graph, neighbour)
      # Driver Code
dfs(visited, graph, 'A')
""")
def pgw():
    print("""
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
 
def water_jug_problem(capacity_jug1, capacity_jug2, target_amount):
    if target_amount % gcd(capacity_jug1, capacity_jug2) != 0 or target_amount > max(capacity_jug1, capacity_jug2):
        print("No Solution exists")
        return
 
    jug1_current = 0
    jug2_current = 0
 
    while jug1_current != target_amount and jug2_current != target_amount:
        print(f"Jug 1: {jug1_current} Jug 2: {jug2_current}")
 
        if jug1_current == 0:
            jug1_current = capacity_jug1
        elif jug1_current >= 0 and jug2_current < capacity_jug2:
            transfer_amount = min(jug1_current, capacity_jug2 - jug2_current)
            jug1_current -= transfer_amount
            jug2_current += transfer_amount
 
        if jug2_current == capacity_jug2:
            jug2_current = 0
        elif jug2_current >= 0 and jug1_current < capacity_jug1:
            transfer_amount = min(jug2_current, capacity_jug1 - jug1_current)
            jug2_current -= transfer_amount
            jug1_current += transfer_amount
 
    print(f"Jug 1: {jug1_current} Jug 2: {jug2_current}")
    print("Solution found")
 

jug1_capacity = int(input("Enter the capacity of Jug 1: "))
jug2_capacity = int(input("Enter the capacity of Jug 2: "))
target_amount = int(input("Enter the target amount of water: "))
 

water_jug_problem(jug1_capacity, jug2_capacity, target_amount)
""")
def mac():
    print("""
def is_valid(missionaries, cannibals):
    if missionaries < 0 or missionaries > 3:
        return False
    if cannibals < 0 or cannibals > 3:
        return False
    if missionaries != 0 and missionaries < cannibals:
        return False
    if 3 - missionaries < 3 - cannibals and 3 - missionaries != 0:
        return False
    return True
 
def bfs(start_missionaries, start_cannibals):
    visited = set()
    queue = [(start_missionaries, start_cannibals, 'left', 0)]
    print("Starting BFS...")
    print("Initial State:", (start_missionaries, start_cannibals, 'left'))
 
    while queue:
        missionaries, cannibals, boat, depth = queue.pop(0)
        print("Exploring State:", (missionaries, cannibals, boat), "Depth:", depth)
 
        if missionaries == 0 and cannibals == 0:
            print("Goal State reached!")
            return depth
 
        visited.add((missionaries, cannibals, boat))
 
        for m_move, c_move, b_move in [(1, 0, 'right'), (2, 0, 'right'), (0, 1, 'right'), (0, 2, 'right'), (1, 1, 'right')]:
            if boat == 'left':
                new_missionaries = missionaries - m_move
                new_cannibals = cannibals - c_move
                new_boat = 'right'
            else:
                new_missionaries = missionaries + m_move
                new_cannibals = cannibals + c_move
                new_boat = 'left'
 
            if is_valid(new_missionaries, new_cannibals) and (new_missionaries, new_cannibals, new_boat) not in visited:
                print("Adding New state to Queue:", (new_missionaries, new_cannibals, new_boat))
                queue.append((new_missionaries, new_cannibals, new_boat, depth + 1))
 
    return -1
 
if _name_ == "_main_":
    start_missionaries = int(input("Enter the number of missionaries on the starting side: "))
    start_cannibals = int(input("Enter the number of cannibals on the starting side: "))
 
    min_transactions = bfs(start_missionaries, start_cannibals)
    print("Minimum number of Transactions required is:", min_transactions)
""")