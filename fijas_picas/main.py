import re
import math
import random


class Agent:
    random.seed(42)

    def __init__(self):
        # Check if the number is a valid number
        self.ALL_NUMBERS = [str(number).zfill(4) for number in range(100, 10000) if len(str(number).zfill(4)) == 4 and
                            len(set(str(number).zfill(4))) == 4]
        self.POTENTIAL_ANSWERS = [(0, 1), (0, 2), (1, 1), (1, 0), (0, 0), (0, 3), (1, 2), (2, 0), (2, 1),
                                  (3, 0), (0, 4), (1, 3), (2, 2), (4, 0)]
        self.last_question = None
        self.history = []
        self.i = 0
        self.current_allowed_numbers = set(self.ALL_NUMBERS)
        self.response = (0, 0)
        self.number_generated = self.number_generator()

    def compute_agent_guess_user_number(self):
        """
        Lunch the game ([S] option) and ask the number of "picas" and "fijas" in the user's number.
        """
        print("R")
        while not self.is_finished():
            n = self.get_question()
            print(n)

            picas_fijas_user = Game.get_picas_fijas_user().split(",")
            picas_fijas_user = f"{picas_fijas_user[1]} {picas_fijas_user[0]}"

            # should be a tuple of two numbers
            answer = tuple([int(i) for i in re.findall(r'[0-9]+', picas_fijas_user)])
            self.put_answer(answer)
            print("A")

        print(self.guessed_number())

    def compute_agent_answer_picas_fijas(self):
        """
        Lunch the game ([#] option) and ask numbers that must be consistent with the machine's number.
        :return: The number of picas and fijas in the machine's number.
        """
        print("R")
        while self.response[0] != 4:
            self.i += 1
            n = Game.get_user_number().zfill(4)
            self.response = self.response_picas_fijas(self.number_generated, n)
            print(f"{self.response[1]},{self.response[0]}")

        print(self.number_generated)

    def is_finished(self):
        """
        Checks if the game is finished.
        :return: A boolean indicating whether the game is finished.
        """
        return self.count_possible_numbers(self.history, self.ALL_NUMBERS) <= 1

    def get_question(self):
        """
        Gets the question to ask the user.
        :return: The question to ask the user.
        """
        assert not self.is_finished()
        self.i += 1
        if self.i == 1:
            self.last_question = "3719"
        else:
            self.last_question = \
                self.get_best_question(self.i, self.history, self.current_allowed_numbers)

        return self.last_question

    def put_answer(self, answer):
        """
        Puts the answer of the user.
        :param answer: The answer of the user.
        """
        assert len(answer) == 2
        self.history.append((self.last_question, answer))

    def get_step(self):
        """
        Gets the step of the game.
        :return: The step of the game.
        """
        if self.is_finished():
            return self.i if self.history[-1][1][0] == 4 else self.i + 1
        else:
            return self.i

    def is_correct(self):
        """
        Checks if the answer is correct.
        :return: A boolean indicating whether the answer is correct.
        """
        return self.count_possible_numbers(self.history, self.ALL_NUMBERS) > 0

    def guessed_number(self):
        """
        Gets the guessed number.
        :return: The guessed number.
        """
        return self.get_unique_possible_number(self.history)

    @staticmethod
    def count_fijas_and_picas(number, question):
        """
        Counts the number of fijas and picas in a number and a question.
        :param number: The number to count the fijas and picas in.
        :param question: The question to count the fijas and picas in.
        :return: The number of fijas and picas in the number and the question.
        """
        number, question, fijas, picas = str(number), str(question), 0, 0

        for i in range(4):
            for j in range(4):
                if number[i] == question[j]:
                    if i == j:
                        fijas += 1
                    else:
                        picas += 1

        return fijas, picas

    def number_is_consistent_with_qa(self, number, question, answer):
        """
        Checks if a number is consistent with a question and answer.
        :param number: The number to check.
        :param question: The question to compare the number to.
        :param answer: The answer to compare the number to.
        :return: A integer indicating whether the number is consistent with the question and answer.
        """
        return self.count_fijas_and_picas(number, question) == answer

    def count_possible_numbers(self, history, allowed_numbers):
        """
        Counts the number of possible numbers that could be generated from a history.
        :param history: The history to count the possible numbers from.
        :param allowed_numbers: The allowed numbers to count the possible numbers from.
        :return: The number of possible numbers that could be generated from the history.
        """
        count = 0
        for number in allowed_numbers:
            count += all(self.number_is_consistent_with_qa(number, question, answer)
                         for question, answer in history)

        return count

    def get_unique_possible_number(self, history):
        """
        Gets a unique number that is possible from a history.
        :param history: The history to get the unique number from.
        :return: The unique number.
        """
        for number in self.ALL_NUMBERS:
            if all(self.number_is_consistent_with_qa(number, question, answer) for question, answer in history):
                return number

    def question_entropy_by_history(self, allowed_numbers):
        """
        Calculates the entropy of a question by a history.
        :param allowed_numbers: The allowed numbers to calculate the entropy of.
        :return: The entropy of the question.
        """
        current_min_entropy = 10 ** 9

        def question_entropy(question):
            """
            Calculates the entropy of a question.
            :param question: The question to calculate the entropy of.
            :return: The entropy of the question.
            """
            nonlocal current_min_entropy
            result = 0
            for answer in self.POTENTIAL_ANSWERS:
                count = self.count_possible_numbers([(question, answer)], allowed_numbers)
                if count > 0:
                    result += - math.log(1 / count) * count
                    if result > current_min_entropy:
                        return result
            current_min_entropy = result

            return result

        return question_entropy

    def get_best_question(self, step, history, current_allowed_numbers):
        """
        Gets the best question to ask the user.
        :param step: The step of the game.
        :param history: The history of the game.
        :param current_allowed_numbers: The allowed numbers to get the best question from.
        :return: The best question to ask the user.
        """
        if step > 1:
            for number in list(current_allowed_numbers):
                if not self.number_is_consistent_with_qa(number, *history[-1]):
                    current_allowed_numbers.remove(number)

        sample = list(current_allowed_numbers)
        random.shuffle(sample)
        sample = sample[:10 ** (step - 1)]

        return min(sample, key=self.question_entropy_by_history(current_allowed_numbers))

    def number_generator(self):
        """
        Generates a number with 4 digits.
        :return: The number generated.
        """
        return random.choice(self.ALL_NUMBERS)

    def response_picas_fijas(self, number_got, number_expected):
        """
        Receive a number and return the number of picas and fijas that it contains.
        :param number_got: A four-digit number.
        :param number_expected: A four-digit number.
        :return: The number of picas and fijas in the number.
        """
        return self.count_fijas_and_picas(number_got, number_expected)


class Game:
    def __init__(self):
        self.agent = Agent()

    def start(self):
        """
        Starts the game, where the user is asked for
        """
        while True:
            answer = input()
            if answer == "S":
                self.__init__()
                self.agent.compute_agent_guess_user_number()
            elif answer == "#":
                self.__init__()
                self.agent.compute_agent_answer_picas_fijas()

    @staticmethod
    def get_picas_fijas_user():
        """
        Gets the number of picas and fijas the user has in their number.
        :return: The number of picas and fijas the user has in their number.
        """
        return input()

    @staticmethod
    def get_user_number():
        """
        Gets the user's number.
        :return: The user's number.
        """
        return input()


game = Game()
game.start()
