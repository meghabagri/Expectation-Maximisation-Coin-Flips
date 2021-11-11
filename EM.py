import requests
import json
import random
import numpy as np


def get_flips():
    # accessing the api to get coin flips in the batch size of 20
    url = "https://24zl01u3ff.execute-api.us-west-1.amazonaws.com/beta"
    response_1 = requests.get(url)
    response_2 = requests.get(url)

    coin_flips_1 = json.loads(response_1.text)['body']

    coin_flips_1_list = [i.strip()
                         for i in coin_flips_1[1:-1].replace('"', "").split(',')]

    coin_flips_2 = json.loads(response_2.text)['body']

    coin_flips_2_list = [i.strip()
                         for i in coin_flips_2[1:-1].replace('"', "").split(',')]

    # combining two api calls and picking randomly 30 coin flips

    combined_flips = [*coin_flips_1_list, *coin_flips_2_list]

    selected_flips = []
    for i in range(30):
        selected_flips.append(random.choice(combined_flips))

    return selected_flips


def bayes_probability(roll, bias):
    # calculating P(X | Z, theta)
    num_heads = roll.count('1')
    total_flips = len(roll)

    return pow(bias, num_heads) * pow(1-bias, total_flips-num_heads)


def estimation(rolls):
    theta_a = random.random()
    theta_b = random.random()

    thetas = [(theta_a, theta_b)]

    for c in range(10):
        heads_a, tails_a, heads_b, tails_b = e_step(rolls, theta_a, theta_b)
        theta_a, theta_b = m_step(heads_a, tails_b, heads_b, tails_b)

    return (theta_a, theta_b)


def e_step(rolls, theta_a, theta_b):
    heads_a, tails_a = 0, 0
    heads_b, tails_b = 0, 0

    for roll in rolls:
        probability_a = bayes_probability(roll, theta_a)
        probability_b = bayes_probability(roll, theta_b)

        p_a = probability_a / (probability_a + probability_b)
        p_b = probability_b / (probability_a + probability_b)

        heads_a += p_a * roll.count('1')
        tails_a += p_a * roll.count('0')
        heads_b += p_b * roll.count('1')
        tails_b += p_b * roll.count('0')

    return heads_a, tails_a, heads_b, tails_b


def m_step(heads_a, tails_a, heads_b, tails_b):
    theta_a = heads_a / (heads_a + tails_a)
    theta_b = heads_b / (heads_b + tails_b)

    return theta_a, theta_b


if __name__ == "__main__":
    rolls = []
    for i in range(5):
        rolls.append(get_flips())

    print(estimation(rolls))
