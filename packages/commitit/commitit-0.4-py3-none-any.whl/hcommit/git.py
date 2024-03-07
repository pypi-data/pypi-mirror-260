import os


def make_commit(days: int):
    if days < 1:
        return os.system('git push')
    else:
        dates = f'{days} days ago'
        with open('data.txt', 'a') as file:
            file.write(f'{dates}\n')

        # Staging
        os.system('git add data.txt')

        # Commit
        os.system('git commit --date="'+dates+'" -m "first commit"')

        return days * make_commit(days-1)


numberOfDays = input(
    "Enter the number of days from today you want to commit: ")
make_commit(int(numberOfDays))
