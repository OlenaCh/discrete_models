import math
import os
import sys

class Graph:
  def __init__(self, filename):
    self.number_of_vertices, self.matrix = 0, []
    self._build_graph(filename)

  def _build_graph(self, filename):
    try:
      row = -1
      with open(filename, 'r') as data:
        for line in data.readlines():
          if row == -1: self.number_of_vertices = int(line.rstrip())
          else:
            vals = []
            for val in line.split(): vals.append(int(val))
            self.matrix.append(vals)
          row += 1
    except FileNotFoundError:
      print('Помилка зчитування')


class TSP:
  def __init__(self, graph):
    self.graph = graph
    self.maxsize = float('inf')
    self.final_res = self.maxsize
    self.final_path = [None] * (self.graph.number_of_vertices + 1)

  def print(self):
    print("Мінімальна вага: ", self.final_res)
    print("Шлях: ", end = ' ')
    for i in range(self.graph.number_of_vertices + 1):
      print(self.final_path[i], end = ' ')
    print()

  def search(self):
    curr_bound = 0
    curr_path = [-1] * (self.graph.number_of_vertices + 1)
    visited = [False] * self.graph.number_of_vertices

    for i in range(self.graph.number_of_vertices):
      curr_bound += self._first_min(i) + self._second_min(i)
    curr_bound = math.ceil(curr_bound / 2)

    visited[0], curr_path[0] = True, 0
    self._search_helper(curr_bound, 0, 1, curr_path, visited)

  def _search_helper(self, curr_bound, curr_weight, level, curr_path, visited):
    if level == self.graph.number_of_vertices:
      if self.graph.matrix[curr_path[level - 1]][curr_path[0]] != 0:
        curr_res = curr_weight + self.graph.matrix[curr_path[level - 1]][curr_path[0]]
        if curr_res < self.final_res:
          self._copy_to_final_path(curr_path)
          self.final_res = curr_res
      return

    for i in range(self.graph.number_of_vertices):
      if self.graph.matrix[curr_path[level - 1]][i] != 0 and visited[i] == False:
        temp = curr_bound
        curr_weight += self.graph.matrix[curr_path[level - 1]][i]

        if level == 1:
          curr_bound -= ((self._first_min(curr_path[level - 1]) + self._first_min(i)) / 2)
        else:
          curr_bound -= ((self._second_min(curr_path[level - 1]) + self._first_min(i)) / 2)

        if curr_bound + curr_weight < self.final_res:
          curr_path[level], visited[i] = i, True
          self._search_helper(curr_bound, curr_weight, level + 1, curr_path, visited)

        curr_weight -= self.graph.matrix[curr_path[level - 1]][i]
        curr_bound = temp

        visited = [False] * len(visited)
        for j in range(level):
          if curr_path[j] != -1: visited[curr_path[j]] = True

  def _first_min(self, i):
    min = self.maxsize
    for k in range(self.graph.number_of_vertices):
      if self.graph.matrix[i][k] < min and i != k:
        min = self.graph.matrix[i][k]
    return min

  def _second_min(self, i):
    first, second = self.maxsize, self.maxsize
    for j in range(self.graph.number_of_vertices):
      if i == j: continue
      if self.graph.matrix[i][j] <= first:
        second, first = first, self.graph.matrix[i][j]
      elif(self.graph.matrix[i][j] <= second and self.graph.matrix[i][j] != first):
        second = self.graph.matrix[i][j]
    return second

  def _copy_to_final_path(self, curr_path):
    self.final_path[:self.graph.number_of_vertices + 1] = curr_path[:]
    self.final_path[self.graph.number_of_vertices] = curr_path[0]


# Driver code
tsp = TSP(Graph('l3_3.txt'))
tsp.search()
tsp.print()
