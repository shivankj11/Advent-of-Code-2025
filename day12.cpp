#include <vector>
#include <string>
#include <set>
#include <map>
#include <tuple>
#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdint>
#include <algorithm>
#include <z3++.h>
using namespace std;

struct Orientation {
    vector<pair<int,int>> cells; // (dr, dc)
    int h, w;
};

struct Placement {
    vector<pair<int,int>> cells; // absolute (row, col)
};

vector<string> readLines(const string& path) {
    ifstream f(path);
    vector<string> lines;
    string line;
    while (getline(f, line)) {
        while (!line.empty() && (line.back() == '\r' || line.back() == '\n')) line.pop_back();
        lines.push_back(line);
    }
    return lines;
}

vector<vector<char>> rotate90(const vector<vector<char>>& grid) {
    int h = grid.size(), w = grid[0].size();
    vector<vector<char>> out(w, vector<char>(h));
    for (int r = 0; r < h; r++)
        for (int c = 0; c < w; c++)
            out[w-1-c][r] = grid[r][c];
    return out;
}

vector<vector<char>> fliplr(const vector<vector<char>>& grid) {
    int h = grid.size(), w = grid[0].size();
    vector<vector<char>> out(h, vector<char>(w));
    for (int r = 0; r < h; r++)
        for (int c = 0; c < w; c++)
            out[r][w-1-c] = grid[r][c];
    return out;
}

vector<Orientation> orientations(const vector<vector<char>>& shape) {
    set<vector<pair<int,int>>> seen;
    vector<Orientation> result;
    for (bool flip : {false, true}) {
        vector<vector<char>> arr = flip ? fliplr(shape) : shape;
        for (int rot = 0; rot < 4; rot++) {
            vector<pair<int,int>> cells;
            for (int r = 0; r < (int)arr.size(); r++)
                for (int c = 0; c < (int)arr[0].size(); c++)
                    if (arr[r][c] == '#') cells.push_back({r, c});
            sort(cells.begin(), cells.end());
            if (!seen.count(cells)) {
                seen.insert(cells);
                result.push_back({cells, (int)arr.size(), (int)arr[0].size()});
            }
            arr = rotate90(arr);
        }
    }
    return result;
}

vector<Placement> validPlacements(const Orientation& o, int width, int length) {
    vector<Placement> out;
    if (o.h > length || o.w > width) return out;
    for (int i = 0; i <= length - o.h; i++) {
        for (int j = 0; j <= width - o.w; j++) {
            Placement p;
            for (auto& [dr, dc] : o.cells) p.cells.push_back({i+dr, j+dc});
            out.push_back(p);
        }
    }
    return out;
}

bool canFit(int width, int length, vector<vector<Orientation>>& shapeOrientations, vector<int>& counts) {
    vector<vector<Placement>> placementsByShape(counts.size());
    for (int s = 0; s < (int)counts.size(); s++) {
        if (counts[s] == 0) continue;
        for (auto& o : shapeOrientations[s]) {
            auto vp = validPlacements(o, width, length);
            placementsByShape[s].insert(placementsByShape[s].end(), vp.begin(), vp.end());
        }
        if ((int)placementsByShape[s].size() < counts[s]) return false;
    }

    z3::context ctx;
    z3::solver solver(ctx);
    map<pair<int,int>, vector<z3::expr>> cellVars;

    for (int s = 0; s < (int)counts.size(); s++) {
        if (counts[s] == 0) continue;
        auto& placements = placementsByShape[s];
        z3::expr_vector shapeVars(ctx);
        for (int idx = 0; idx < (int)placements.size(); idx++) {
            z3::expr v = ctx.bool_const(("P_" + to_string(s) + "_" + to_string(idx)).c_str());
            shapeVars.push_back(v);
            for (auto& cell : placements[idx].cells) cellVars[cell].push_back(v);
        }
        vector<int> coeffs(shapeVars.size(), 1);
        solver.add(z3::pbeq(shapeVars, coeffs.data(), counts[s]));
    }

    for (auto& [cell, vars] : cellVars) {
        z3::expr_vector vec(ctx);
        for (auto& v : vars) vec.push_back(v);
        solver.add(z3::atmost(vec, 1));
    }

    return solver.check() == z3::sat;
}

int main(int argc, char** argv) {
    string path = argc > 1 ? argv[1] : "input12.txt";
    vector<string> lines = readLines(path);

    vector<string> first;
    vector<string> second;
    for (auto& line : lines) {
        if (line.find('x') != string::npos) second.push_back(line);
        else first.push_back(line);
    }

    vector<vector<vector<char>>> shapes;
    vector<vector<char>> block;
    auto flushBlock = [&]() {
        if (block.size() > 1) {
            vector<vector<char>> grid(block.begin() + 1, block.end());
            shapes.push_back(grid);
        }
        block.clear();
    };
    for (auto& line : first) {
        if (line.empty()) { flushBlock(); continue; }
        block.push_back(vector<char>(line.begin(), line.end()));
    }
    flushBlock();

    vector<tuple<int,int,vector<int>>> trees;
    for (auto& line : second) {
        int colon = line.find(':');
        string dims = line.substr(0, colon);
        string rest = line.substr(colon + 1);

        int xpos = dims.find('x');
        int width = stoi(dims.substr(0, xpos));
        int length = stoi(dims.substr(xpos + 1));

        vector<int> counts;
        istringstream iss(rest);
        int v;
        while (iss >> v) counts.push_back(v);

        trees.push_back({width, length, counts});
    }

    vector<vector<Orientation>> shapeOrientations;
    for (auto& shape : shapes) shapeOrientations.push_back(orientations(shape));

    int result = 0;
    for (auto& [width, length, counts] : trees) {
        if (canFit(width, length, shapeOrientations, counts)) result++;
    }

    cout << result << endl;
    return 0;
}
