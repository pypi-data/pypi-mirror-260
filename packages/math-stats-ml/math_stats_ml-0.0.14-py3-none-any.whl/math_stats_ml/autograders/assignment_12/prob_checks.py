from .sol import *

# What are you doing looking in here? Shame on you! You're not going to find the answers!
sol = Solutions()

def prob_check(answers, prob_num):
    solutions = sol.get_solutions(prob_num)
    for answer, solution in zip(answers, solutions):
        if isinstance(answer, type(solution[0])):
            if np.all(answer == solution[0]):
                print("\033[92m-" * 80, '\n')
                print(f"Your `{solution[1]}` is correct!\n")
                print("\033[92m-" * 80)
            else:
                print("\033[91m-" * 80, '\n')
                print(f"Your `{solution[1]}` is incorrect!\n")
                print(f"Your answer:")
                print(answer, '\n')
                print(f"Correct answer:")
                print(solution[0], '\n')
                print("\033[91m-" * 80)
        else:
            print("\033[91m-" * 80, '\n')
            print(print_type_error(solution))
            print("\033[91m-" * 80)