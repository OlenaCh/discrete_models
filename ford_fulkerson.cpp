#include <iostream>
#include <string.h>

using namespace std;

#define N 8
#define INF 9999999

int flow[N][N];
bool visited[N];

int graph[N][N] = {
    { 0, 20, 20, 40, 0,  0,  0,  0 },
    { 0, 0,  10, 0,  10, 0,  0,  0 },
    { 0, 0,  0,  20, 20, 0,  0,  0 },
    { 0, 0,  0,  0,  0,  20, 20, 0 },
    { 0, 0,  0,  0,  0,  0,  0,  30 },
    { 0, 0,  10, 0,  20, 0,  0,  20 },
    { 0, 0,  0,  0,  0,  10, 0,  20 },
    { 0, 0,  0,  0,  0,  0,  0,  0 },
};

int dfs(int s, int t, int minimum) {
    visited[s] = true;

    if (s == t) return minimum;

    for (int i = 0; i < N; i++) {
        int flow_capacity = graph[s][i] - flow[s][i];
        if (!visited[i] && flow_capacity > 0) {
            if (int sent = dfs(i, t, min(minimum, flow_capacity))) {
                flow[s][i] += sent;
                flow[i][s] -= sent;
                return sent;
            }
        }
    }

    return false;
}

int main() {
    memset(flow, 0, sizeof(flow));
    memset(visited, 0, sizeof(visited));

    int s = 0, t = 7, max_flow = 0;

    while (int sent = dfs(s, t, INF)) {
        max_flow += sent;
        memset(visited, 0, sizeof(visited));
    }

    cout << "Максимальний потік " << max_flow << endl;
}
