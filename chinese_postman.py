import sys
import os

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


class ChinesePostman:
  def __init__(self, graph):
    self.graph = graph
    self.edges_sum = 0
    self.odd_vertices = []
    self.odd_pairs = []
    self.result = 0

  def print(self):
    print('Сума ваг усіх ребер: ', self.edges_sum)
    print('Вершини з непарною степінню: ', self.odd_vertices)
    print('Усі можливі пари вершин за непарною степінню: ', self.odd_pairs)
    print('Вага найкоротшого шляху: ', self.result)

  def search(self):
    self._odd_vertices()
    self._sum_edges()

    if (len(self.odd_vertices) == 0):
      return self.edges_sum

    self._generate_pairs()
    l, pairings_sum = (len(self.odd_pairs) + 1) // 2, []

    def get_pairs(pairs, done = [], final = []):
      if(pairs[0][0][0] not in done):
        done.append(pairs[0][0][0])

        for i in pairs[0]:
          f, val = final[:], done[:]

          if(i[1] not in val): f.append(i)
          else: continue

          if(len(f) == l):
            pairings_sum.append(f)
            return
          else:
            val.append(i[1])
            get_pairs(pairs[1:],val, f)
      else: get_pairs(pairs[1:], done, final)

    get_pairs(self.odd_pairs)
    min_sums = []

    for i in pairings_sum:
        s = 0
        for j in range(len(i)): s += self._dijktra(i[j][0], i[j][1])
        min_sums.append(s)

    self.result = min(min_sums) + self.edges_sum

  def _dijktra(self, source, dest):
    shortest = [0 for i in range(self.graph.number_of_vertices)]
    selected = [source]
    l, inf = len(self.graph.matrix), 10000000
    min_sel = inf

    for i in range(l):
      if (i == source): shortest[source] = 0
      else:
        if(self.graph.matrix[source][i] == 0): shortest[i] = inf
        else:
          shortest[i] = self.graph.matrix[source][i]
          if (shortest[i] < min_sel): min_sel, ind = shortest[i], i

    if (source == dest): return 0
    selected.append(ind)

    while (ind != dest):
      for i in range(l):
        if i not in selected:
          if (self.graph.matrix[ind][i] != 0):
            if ((self.graph.matrix[ind][i] + min_sel) < shortest[i]):
              shortest[i] = self.graph.matrix[ind][i] + min_sel

      temp_min = 1000000

      for j in range(l):
        if j not in selected:
          if (shortest[j] < temp_min): temp_min, ind = shortest[j], j

      min_sel = temp_min
      selected.append(ind)

    return shortest[dest]

  def _generate_pairs(self):
    for i in range(len(self.odd_vertices) - 1):
      self.odd_pairs.append([])
      for j in range(i + 1, len(self.odd_vertices)):
        self.odd_pairs[i].append([self.odd_vertices[i], self.odd_vertices[j]])

  def _odd_vertices(self):
    degrees = [0 for i in range(self.graph.number_of_vertices)]

    for i in range(self.graph.number_of_vertices):
      for j in range(self.graph.number_of_vertices):
        if (self.graph.matrix[i][j] != 0): degrees[i] += 1

    self.odd_vertices = [i for i in range(self.graph.number_of_vertices) if degrees[i] % 2 != 0]

  def _sum_edges(self):
    l = len(self.graph.matrix)

    for i in range(l):
      for j in range(i, l):
        self.edges_sum += self.graph.matrix[i][j]

# __main__
cp = ChinesePostman(Graph('l2_3.txt'))
cp.search()
cp.print()