'''
Epidemic modelling

YOUR NAME
Doniyorbek Ibrokhimov
Functions for running a simple epidemiological simulation
'''

import random
import click

# This seed should be used for debugging purposes only!  Do not refer
# to it in your code.
TEST_SEED = 20170217

def count_infected(city):
    infected_counter = 0
    for i in city:
        if i[0] == "I":
            infected_counter += 1

    return infected_counter


def has_an_infected_neighbor(city, position):
    assert city[position] == "S"
    if position == 0 and len(city) == 1 and city[position].find("I") != 0:
        statement = False

    elif position == 0:
        if city[position + 1].find("I") == 0:
            statement = True
        else:
            statement = False

    elif position == len(city) - 1:
        if city[position - 1].find("I") == 0:
            statement = True
        else:
            statement = False

    elif city[position + 1].find("I") == 0 or city[position - 1].find("I") == 0:
        statement = True
    else:
        statement = False

    return statement


def advance_person_at_position(city, position, days_contagious):
    if city[position] == "V":
        return "V"

    if city[position].startswith("I"):
        if int(city[position][1:]) + 1 == days_contagious:
            return "R"

        elif int(city[position][1:]) + 1 < days_contagious:
            return f"I{int(city[position][1:]) + 1}"

    elif city[position].startswith("S") and not has_an_infected_neighbor(city, position):
        return "S"
    elif city[position].startswith("S") and has_an_infected_neighbor(city, position):
        return "I0"
    elif city[position].startswith("R"):
        return "R"
    elif int(city[position][1:]) + 1 < days_contagious:
        return f"I{int(city[position][1:]) + 1}"
    else:
        return "R"


def simulate_one_day(starting_city, days_contagious)

    return [advance_person_at_position(starting_city,position, days_contagious) for position, _  in  enumerate(starting_city, start=0)]

def run_simulation(starting_city, days_contagious,
                   random_seed=None, vaccine_effectiveness=0.0):

    random.seed(random_seed)
    starting_city = vaccinate_city(starting_city, vaccine_effectiveness)
    num = 0
    while 0 != count_infected(city=starting_city):
        starting_city = simulate_one_day(starting_city=starting_city, days_contagious=days_contagious)
        num += 1

    return (starting_city, num)


def vaccinate_city(starting_city, vaccine_effectiveness):

    new_city = starting_city[:]
    for index, person in enumerate(starting_city):

        if person == "S":
            if vaccine_effectiveness >= random.random():
                new_city[index] = "V"

    return new_city

def calc_avg_days_to_zero_infections(
        starting_city, days_contagious,
        random_seed, vaccine_effectiveness,
        num_trials):

    assert num_trials > 0
    total = 0
    for i in range(num_trials):
        total += run_simulation(starting_city, days_contagious, random_seed, vaccine_effectiveness)[1]
        if i >= 1:
            random_seed += 1
    answer = total / num_trials

    return answer


################ Do not change the code below this line #######################


@click.command()
@click.argument("city", type=str)
@click.option("--days-contagious", default=2, type=int)
@click.option("--random_seed", default=None, type=int)
@click.option("--vaccine-effectiveness", default=0.0, type=float)
@click.option("--num-trials", default=1, type=int)
@click.option("--task-type", default="single",
              type=click.Choice(['single', 'average']))
def cmd(city, days_contagious, random_seed, vaccine_effectiveness,
        num_trials, task_type):
    '''
    Process the command-line arguments and do the work.
    '''

    # Convert the city string into a city list.
    city = [p.strip() for p in city.split(",")]
    emsg = ("Error: people in the city must be susceptible ('S'),"
            " recovered ('R'), or infected ('Ix', where *x* is an integer")
    for p in city:
        if p[0] == "I":
            try:
                _ = int(p[1])
            except ValueError:
                print(emsg)
                return -1
        elif p not in {"S", "R"}:
            print(emsg)
            return -1

    if task_type == "single":
        print("Running one simulation...")
        final_city, num_days_simulated = run_simulation(
            city, days_contagious, random_seed, vaccine_effectiveness)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    else:
        print("Running multiple trials...")
        avg_days = calc_avg_days_to_zero_infections(
            city, days_contagious, random_seed, vaccine_effectiveness,
            num_trials)
        msg = ("Over {} trial(s), on average, it took {:3.1f} days for the "
               "number of infections to reach zero")
        print(msg.format(num_trials, avg_days))

    return 0


if __name__ == "__main__":
    cmd()  # pylint: disable=no-value-for-parameter
