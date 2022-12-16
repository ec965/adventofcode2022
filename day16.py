import re

inf = 9000000000000000

AdjMatrix = dict[str, list[str]]
StepCosts = dict[str, dict[str, int]]
Rates = dict[str, int]


def find_steps(adj: AdjMatrix, curr: str, end: str, steps: int, seen: set[str]):
    if curr == end:
        return steps

    next_seen = seen.copy()
    next_seen.add(curr)

    next_steps = [inf]
    for next in adj[curr]:
        if not next in next_seen:
            next_steps.append(find_steps(adj, next, end, steps + 1, next_seen))

    return min(next_steps)


def calc_pressure(open_valv_rates: int, pressure: int, time_spent: int):
    return pressure + (open_valv_rates * time_spent)


def explore(
    step_costs: StepCosts,
    rates: Rates,
    loc: str,
    time_left: int,
    open_valv_rates: int,
    pressure: int,
    is_open: set[str],
) -> int:
    if time_left == 0:
        return pressure

    found = [0]
    loc_steps = step_costs[loc]
    for k in loc_steps:
        steps = loc_steps[k]

        time_spent = steps + 1
        next_time = time_left - time_spent

        f = 0

        # don't move, run out the time
        if next_time <= 0 or k in is_open:
            f = calc_pressure(open_valv_rates, pressure, time_left)
        else:
            next_is_open = is_open.copy()
            next_is_open.add(k)

            f = explore(
                step_costs,
                rates,
                k,
                next_time,
                open_valv_rates + rates[k],
                calc_pressure(open_valv_rates, pressure, time_spent),
                next_is_open,
            )

        found.append(f)

    return max(found)


if __name__ == "__main__":
    # we need to assign every node a weight based on valv_val
    # 1. find the # of steps from current loc to next valv
    # 2. calc each valv value and choose highest value
    # 3. decrement time by amount needed to open that valv
    # -> during this process, track pressure released

    # we need to explore every none-zero possibility and then choose the one
    # with the highest pressure release

    input_file = "./inputs/day16.txt"
    rates: Rates = {}
    adj: AdjMatrix = {}
    with open(input_file) as file:
        for line in file.readlines():
            valvs = re.findall("[A-Z]{2}", line)
            valvs.reverse()
            valv = valvs.pop()
            adj[valv] = valvs
            rates[valv] = int(re.findall("\\d+", line).pop())

    step_costs: StepCosts = {}
    for k in adj:
        if rates[k] > 0 or k == "AA":
            step_costs[k] = {}
            for j in adj:
                if rates[j] > 0 and k != j:
                    step_costs[k][j] = find_steps(adj, k, j, 0, set())

    res = explore(step_costs, rates, "AA", 30, 0, 0, set())
    print("part1", res)
