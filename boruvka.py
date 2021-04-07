import sys
import os

class Graph:
  def __init__(self, filename):
    self.number_of_vertices, self.edges = 0, []
    self._build_graph(filename)

  def _add_edge(self, u, row):
    for v in range(self.number_of_vertices):
      w = int(row[v])
      if w != 0: self.edges.append([u, v, w])

  def _build_graph(self, filename):
    try:
      row = -1
      with open(filename, 'r') as matrix:
        for line in matrix.readlines():
          if row == -1: self.number_of_vertices = int(line.rstrip())
          else: self._add_edge(row, line.split())
          row += 1
    except FileNotFoundError:
      print('Помилка зчитування')


class BoruvkaAlgorithm:
  def __init__(self, graph):
    self.graph = graph

  def find(self, array, i):
    if array[i] == i: return i
    return self.find(array, array[i])

  def join_sets(self, parent, rank, x, y):
    xroot, yroot = self.find(parent, x), self.find(parent, y)
    if rank[xroot] < rank[yroot]: parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]: parent[yroot] = xroot
    else : parent[yroot], rank[xroot] = xroot, rank[xroot] + 1

  def search(self):
    parent, rank, cost = [], [], []
    number_of_trees, weight = self.graph.number_of_vertices, 0

    for node in range(self.graph.number_of_vertices):
      parent.append(node)
      rank.append(0)
      cost =[-1] * self.graph.number_of_vertices

    while number_of_trees > 1:
      for i in range(len(self.graph.edges)):
        u, v, w = self.graph.edges[i]
        set1, set2 = self.find(parent, u), self.find(parent, v)

        if set1 != set2:
          if cost[set1] == -1 or cost[set1][2] > w : cost[set1] = [u, v, w]
          if cost[set2] == -1 or cost[set2][2] > w : cost[set2] = [u, v, w]

      for node in range(self.graph.number_of_vertices):
        if cost[node] != -1:
          u, v, w = cost[node]
          set1, set2 = self.find(parent, u), self.find(parent, v)

          if set1 != set2 :
            self.join_sets(parent, rank, set1, set2)
            print ("Ребро %d-%d (вага %d) входить до остового дерева" % (u, v, w))
            number_of_trees, weight = number_of_trees - 1, weight + w

      cost =[-1] * self.graph.number_of_vertices

    print ("Вага остового дерева %d" % weight)


# __main__
BoruvkaAlgorithm(Graph('l1_3.txt')).search()