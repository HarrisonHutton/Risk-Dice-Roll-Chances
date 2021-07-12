import random
import json

from math import factorial as f


class Calculator:

    def __init__(self):
        self.die = [1, 2, 3, 4, 5, 6]

    # Utility functions to handle storing the json data
    def get_data(self):
        with open('data.json', 'r') as file:
            data = json.load(file)
        return data

    def save_data(self, data):
        with open('data.json', 'w') as file:
            json.dump(data, file)

    def win_rates(self, key):
        data = self.get_data()

        battle_dict = data[key]

        # This will be a dictionary with keys being the type of battle result, and values being the percent frequency
        # that this result occurred.
        percentages = {}

        for battle in battle_dict["battles"]:

            percentages[battle] = battle_dict["battles"][battle] / battle_dict["total"] * 100

        return percentages


    def calculate(self):
        return random.choice(self.die)

    def num_dice_combs(self, dice):
        """
        :param dice: number of dice to be rolled
        :return: the total number of combinations that could be made with the given number of dice
        """
        # Example: 3 dice, 6 faces each:
        # C(n+k-1, k) -> C(6+3-1, 6+3-1-3) = C(8, 5)
        this_many = f(6+dice-1)/(f(dice)*f(6-1))
        return int(this_many)

    def doset(self, retval, map=map, list=list, set=set, tuple=tuple):
        return map(list, set(map(tuple, retval)))

    def clean_combos(self, combo_list):
        for combo in combo_list:
            combo.sort()

        self.doset(combo_list)

        no_duplicates = []
        for combo in combo_list:
            if combo not in no_duplicates:
                no_duplicates.append(combo)

        return no_duplicates

    # Goal: Make this recursive so that it can run with any amount of dice
    def find_combs_3(self):
        """
        :return: list of combinations that could be made with the 3 dice
        """
        combos = []
        for i in range(len(self.die)):
            for j in range(len(self.die)):
                for h in range(len(self.die)):
                    combos.append([self.die[i], self.die[j], self.die[h]])

        return self.clean_combos(combos)

    def find_perms_3(self):
        """
        :return: list of combinations that could be made with the 3 dice
        """
        perms = []
        for i in range(len(self.die)):
            for j in range(len(self.die)):
                for h in range(len(self.die)):
                    perms.append([self.die[i], self.die[j], self.die[h]])

        return perms

    def find_combs_2(self):
        """
        :return: list of combinations that could be made with the 3 dice
        """
        combos = []
        for i in range(len(self.die)):
            for j in range(len(self.die)):
                combos.append([self.die[i], self.die[j]])

        return self.clean_combos(combos)

    def find_perms_2(self):
        """
        :return: list of combinations that could be made with the 3 dice
        """
        perms = []
        for i in range(len(self.die)):
            for j in range(len(self.die)):
                    perms.append([self.die[i], self.die[j]])

        return perms

    def create_frequency_dict(self, combo_list):
        """
        :param combo_list: list (with duplicates) of combinations
        :return: a dictionary that maps each combination to the number of different ways it could occur
        """
        retval = {}

        perms_sorted = combo_list

        for perm in perms_sorted:
            perm.sort()

        for perm in perms_sorted:
            retval[str(perm)] = retval.get(str(perm), 0) + 1

        return retval

    def find_winner(self, attacker_dice: list, defender_dice: list) -> int:
        """
        :param attacker_dice: Combination of a dice roll
        :param defender_dice: Combination of a dice roll
        :return: Dictionary with keys: "attacker" and "defender", both with integer values that
                 that decrement by one when the opponent wins a battle
        """

        # Initialize the score keeper
        score_keeper = {"attacker": 0, "defender": 0}

        print(attacker_dice)
        print(defender_dice)

        attacker_temp_list = attacker_dice
        defender_temp_list = defender_dice

        # Need two different conditions to handle indexing errors
        if len(defender_temp_list) <= len(attacker_temp_list):
            while len(defender_temp_list) > 0:
                # pop the max element in both the attacker list and defender list and compare
                # based on who wins, update score keeper accordingly
                a_index = attacker_temp_list.index(max(attacker_temp_list))
                d_index = defender_temp_list.index(max(defender_temp_list))

                if max(defender_temp_list) >= max(attacker_temp_list):
                    score_keeper["attacker"] -= 1
                else:
                    score_keeper["defender"] -= 1

                attacker_temp_list.pop(a_index)
                defender_temp_list.pop(d_index)

        else:
            while len(attacker_temp_list) > 0:
                # pop the max element in both the attacker list and defender list and compare
                # based on who wins, update score keeper accordingly
                a_index = attacker_temp_list.index(max(attacker_temp_list))
                d_index = defender_temp_list.index(max(defender_temp_list))

                if max(defender_temp_list) >= max(attacker_temp_list):
                    score_keeper["attacker"] -= 1
                else:
                    score_keeper["defender"] -= 1

                attacker_temp_list.pop(a_index)
                defender_temp_list.pop(d_index)

        return score_keeper

    def update_data(self, battle_type: str, win_type: dict):
        """
        :param battle_type: key to access the correct json object
        :param win_type: dictionary representing the type of win
        :return: None; just update the json file
        """

        data = self.get_data()

        data[battle_type]["total"] += 1

        result = str(win_type)

        data[battle_type]["battles"][result] = data[battle_type]["battles"].get(result, 0) + 1

        self.save_data(data)


if __name__ == '__main__':
    print("\n")
    calc = Calculator()
    two_dice_perms = calc.find_perms_2()
    three_dice_perms = calc.find_perms_3()

    expected_number_2 = calc.num_dice_combs(2)
    print(f'The expected number of combinations for 2 dice: {expected_number_2}')
    print(calc.find_combs_2())
    found_number_2 = len(calc.find_combs_2())
    print(f'We found this many: {found_number_2}')

    print("")
    print("------------------------------------------------------")
    print("")

    expected_number_3 = calc.num_dice_combs(3)
    print(f'The expected number of combinations for 3 dice: {expected_number_3}')
    print(calc.find_combs_3())
    found_number_3 = len(calc.find_combs_3())
    print(f"We found this many: {found_number_3}")

    print("")
    print("------------------------------------------------------")
    print("")
    three_dice_perms = calc.find_perms_3()
    print("Frequency of each roll for three dice:")
    print(calc.create_frequency_dict(three_dice_perms))

    print("")
    print("------------------------------------------------------")
    print("")
    two_dice_perms = calc.find_perms_2()
    print("Frequency of each roll for two dice:")
    print(calc.create_frequency_dict(two_dice_perms))
    
    print("")
    print("------------------------------------------------------")
    print("")
    print("Approximate win rate for an attacker rolling with three dice against a defender rolling with two:")
