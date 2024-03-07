import sys
from time import sleep

from tqdm import tqdm


def gen():
    for i in range(3):
        sleep(0.5)
        yield i


lines = gen()

line_bar = tqdm(leave=True, position=1, file=sys.stdout)

for line in lines:
    line_bar.set_description(f"Line idx: {line}")
    line_bar.update(1)
    instructions = ["a", "b", "c", "d", "e"]
    instruction_bar = tqdm(
        instructions, ncols=100, leave=False, position=1, file=sys.stdout
    )

    line_bar.write(f"Processed line: {line}", file=sys.stdout)
    # print(f"Processing line: {line}", file=sys.stdout, flush=True)

    for instruction in instruction_bar:
        sleep(0.5)

        instruction_bar.set_description(f"Instruction: {instruction}")
        instruction_bar.update(1)
        # line_bar.write(f"instruction: {instruction}", file=sys.stdout)

    instruction_bar.close()
line_bar.write("---")
line_bar.close()
# print("---")

# line_bar.clear()
# line_bar.refresh()
# line_bar.write("---")
