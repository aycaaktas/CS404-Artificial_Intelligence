% Load grid size and grid data from included data file
include "hashi_instance_hard.dzn";
int: n = 7;

% Define sets based on grid dimensions
set of int: ROWS = 1..n;
set of int: COLS = 1..n;

function int: string2int(string: num) =
  if num == "1" then 1
  elseif num == "2" then 2
  elseif num == "3" then 3
  elseif num == "4" then 4
  elseif num == "5" then 5
  elseif num == "6" then 6
  elseif num == "7" then 7
  else 8 
  endif;

function array[1..n, 1..n] of int: convert_to_int(array[1..n, 1..n] of string: grid) =
  array2d(1..n, 1..n, [ if grid[i, j] = "." then 0 else string2int(grid[i, j]) endif | i in 1..n, j in 1..n ]);
  
array[1..n, 1..n] of string: grid_string;

% Convert the grid to integers
array[1..n, 1..n] of int: grid = convert_to_int(grid_string);


% Extract island positions and required number of bridges

% Number of islands
int: num_islands = sum([grid[r,c] > 0 | r in ROWS, c in COLS]);
% Finding islands and their details
array[1..num_islands] of tuple(int, int, int): islands = array1d([(r, c, grid[r,c]) | r in ROWS, c in COLS where grid[r,c] > 0 ]);

% Variables for bridges between islands
array[1..num_islands, 1..num_islands] of var 0..2: bridges;

% CONSTRAINTS

%----------------------------------

% Bridges between two distinct islands
constraint forall(i in 1..num_islands)(
    bridges[i, i] = 0
);


% Bridges must be orthogonal
predicate orthogonal(int: i, int: j) =
  (islands[i].1 != islands[j].1 /\ islands[i].2 != islands[j].2) -> bridges[i, j] = 0;

constraint forall(i in 1..num_islands) (
    forall(j in 1..num_islands) (
      orthogonal(i, j)
    )
);

% The number of bridges connected to each island must match the number on that island
constraint forall(i in 1..num_islands)(
    sum([bridges[i,j] | j in 1..num_islands]) = islands[i].3
);

% Symmetry constraint due to the nature of adjacency matrix
constraint forall(i in 1..num_islands) (
    forall(j in 1..num_islands) (
      bridges[i, j] = bridges[j, i]
    )
);

% A bridge must not cross an island
constraint forall(i, j in 1..num_islands where i < j) (
    let {
        int: x1 = islands[i].1;
        int: y1 = islands[i].2;
        int: x2 = islands[j].1;
        int: y2 = islands[j].2;
    } in
    if x1 == x2 then %if two islands on same row
        forall(h in 1..num_islands where h != i /\ h != j) (
            if (islands[h].1 = x1 /\ islands[h].2 > min(y1, y2) /\ islands[h].2 < max(y1, y2)) then
                bridges[i, j] = 0
            else
                true
            endif
        )
    elseif y1 == y2 then
        forall(h in 1..num_islands where h != i /\ h != j) (
            if (islands[h].2 = y1 /\ islands[h].1 > min(x1, x2) /\ islands[h].1 < max(x1, x2)) then
                bridges[i, j] = 0
            else
                true
            endif
        )
    else
        true
    endif
);

% A bridge must not cross another bridge
constraint forall(a, b, c, d in 1..num_islands where a < b /\ c < d) (
    let {
        int: xa = islands[a].1;
        int: ya = islands[a].2;
        int: xb = islands[b].1;
        int: yb = islands[b].2;
        int: xc = islands[c].1;
        int: yc = islands[c].2;
        int: xd = islands[d].1;
        int: yd = islands[d].2;
    } in
    if xa = xb /\ yc = yd then
        if (min(ya, yb) < yc /\ yc < max(ya, yb)) /\ (min(xc, xd) < xa /\ xa < max(xc, xd)) then
            bridges[a, b] = 0 \/ bridges[c, d] = 0
        else
            true
        endif
    elseif ya = yb /\ xc = xd then
        if (min(xa, xb) < xc /\ xc < max(xa, xb)) /\ (min(yc, yd) < ya /\ ya < max(yc, yd)) then
            bridges[a, b] = 0 \/ bridges[c, d] = 0
        else
            true
        endif
    else
        true
    endif
);

% All islands must be connected in the end --> see the Python file for the check

%----------------------------------

% Solve for a solution
solve satisfy;

output[show(bridges), show(islands)]