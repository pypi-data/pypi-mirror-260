import logging
import os
import pathlib
import select
import sys
import time
import yaml

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

from pyfiglet import Figlet
from termcolor import colored

from . import constants


console = Console()


# If DEFAULT_RICH is set to True, then will use the Rich library to display menus and other information.
DEFAULT_RICH = True

# This is the number of seconds to wait before starting a set
DEFAULT_SECONDS_BEFORE_START_EXERCISE = 10

DEFAULT_INTERTSET_BREAK_SECONDS = 60


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)


class Tracker:

    def __init__(self, **kwargs):
        self.config_file = kwargs.get("config_file", constants.DEFAULT_CONFIG_FILE)
        self.outdir = kwargs.get("outdir", DEFAULT_OUTDIR)
        self.outfile = kwargs.get("outfile", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        logging.info(f"Will load contents of the workout file '{self.config_file}'")
        self.config = yaml.safe_load(Path(self.config_file).read_text())

        self._load_functions()

        self.current_option_number = 0
        self.selection_lookup = {}


        self._workout_session_start_time = None
        self._workout_session_end_time = None
        self._workout_session_elapsed_time = None
        self._workout_session_exercises_completed = 0
        self._workout_session_exercises_not_completed = 0

        self.seconds_before_start_exercise = self.config.get("seconds_before_start_exercise", DEFAULT_SECONDS_BEFORE_START_EXERCISE)
        self.interset_break_seconds = self.config.get("interset_break_seconds", DEFAULT_INTERTSET_BREAK_SECONDS)

        self.previous_leftside_weight = None
        self.previous_rightside_weight = None
        self.previous_leftside_reps = None
        self.previous_rightside_reps = None

        self.previous_weight = None
        self.previous_reps = None

    def _reinit_weight_and_reps(self) -> None:
        self.previous_leftside_weight = None
        self.previous_rightside_weight = None
        self.previous_leftside_reps = None
        self.previous_rightside_reps = None

        self.previous_weight = None
        self.previous_reps = None

    def _load_functions(self) -> None:
        self.config["functions"] = {}
        self.config["functions"]["Main Menu"] = self._display_main_menu
        self.config["functions"]["Select Workout"] = self._display_select_workout_menu
        self.config["functions"]["Review Previous Workout"] = self._display_review_previous_workout_menu
        logging.info("Loaded functions lookup")

    def run(self) -> None:
        self._display_main_menu()

    def _print_banner(self, message: str) -> None:
        print("\n=====================================")
        print(f"    {message}")
        print("=====================================")


    def _display_menu_banner(self, menu_name: str) -> None:
        self._print_banner(f"Menu: {menu_name}")

    def _display_main_menu(self, rich: bool = DEFAULT_RICH) -> None:
        if rich:
            self._display_main_menu_rich("Main Menu")
        else:
            self._display_menu_banner("Main")
            self._display_menu("Main Menu")
        self._prompt_user("Main Menu")


    def _display_main_menu_rich(self, menu_name: str) -> None:

        if menu_name == "Quit":
            self._quit()

        if menu_name not in self.config["menus"]:
            raise Exception(f"Could not find menu '{menu_name}'")

        start = self.current_option_number + 1

        table = Table(
            show_header=True,
            header_style='bold #2070b2',
            title='[bold]Main Menu[/]'
        )

        table.add_column('Number', justify='center')
        table.add_column('Option')

        for i, option in enumerate(self.config["menus"][menu_name]["options"], start=start):
            table.add_row(f"{i}", option)
            self.current_option_number = i
            self.selection_lookup[i] = option

        console.print(table)


    def _display_select_workout_menu(self) -> None:
        self._display_available_workouts()

    def _display_available_workouts(self) -> None:

        if "workouts" not in self.config:
            raise Exception("Could not find 'workouts' in the lookup")

        if DEFAULT_RICH:
            i = 0
            selection_lookup = {}

            table = Table(
                show_header=True,
                header_style='bold #2070b2',
                title='[bold]Main Menu[/]'
            )

            table.add_column('Number', justify='center')
            table.add_column('Workout Name')

            for workout in self.config["workouts"]:
                i += 1
                table.add_row(f"{i}", workout.title())
                selection_lookup[i] = workout

            i += 1
            table.add_row(f"{i}", "Main Menu")
            selection_lookup[i] = "Main Menu"

            i += 1
            table.add_row(f"{i}", "Quit")
            selection_lookup[i] = "Quit"

            console.print(table)

        else:
            self._display_menu_banner("Available Workouts")

            i = 0
            selection_lookup = {}
            for workout in self.config["workouts"]:
                i += 1
                print(f"{i}. {workout.title()}")
                # self.current_option_number = i
                selection_lookup[i] = workout

            i += 1
            print(f"{i}. Main Menu")
            selection_lookup[i] = "Main Menu"

            i += 1
            print(f"{i}. Quit")
            selection_lookup[i] = "Quit"

        answer = None
        while answer is None:
            answer = input("Choose: ")
            if answer is None or answer == "":
                answer = None
                continue
            try:
                answer = int(answer)
            except ValueError:
                answer = None
                continue

            if answer not in selection_lookup:
                answer = None
                continue

        selection = selection_lookup[answer]
        print(f"{answer=} {selection=}")
        if selection == "Main Menu":
            self._display_main_menu()

        elif selection == "Quit":
            self._quit()

        elif selection in self.config["workouts"]:
            self._display_exercises_in_workout(selection)
        self._display_select_workout_menu()


    def _get_max_len_columns(self, workout_name: str) -> Tuple[int, int, int, int]:
        max_len_name = len("Exercise Name")
        max_len_equipment = len("Equipment")
        max_len_alternating_sides = len("Alternating Sides")
        max_len_body_position = len("Body Position")

        for exercise in self.config["workouts"][workout_name]["exercises"]:

            if len(exercise["name"]) > max_len_name:
                max_len_name = len(exercise["name"])

            if len(exercise["equipment"]) > max_len_equipment:
                max_len_equipment = len(exercise["equipment"])

            if len(exercise["body_position"]) > max_len_body_position:
                max_len_body_position = len(exercise["body_position"])

        return max_len_name, max_len_equipment, max_len_alternating_sides, max_len_body_position

    def _display_exercises_in_workout(self, workout_name: str) -> None:

        if DEFAULT_RICH:

            table = Table(
                show_header=True,
                header_style='bold #2070b2',
                title=f'[bold]Workout: {workout_name}[/]'
            )

            table.add_column('Num', justify='center')
            table.add_column('Exercise Name')
            table.add_column('Equipment')
            table.add_column('Alt. Sides', justify='center')
            table.add_column('Body Position')

            i = 0

            for exercise in self.config["workouts"][workout_name]["exercises"]:
                i += 1
                alternating = "Yes" if exercise["alternating_sides"] else "No"
                table.add_row(
                    f"{i}",
                    exercise['name'],
                    exercise['equipment'],
                    alternating,
                    exercise['body_position']
                )


            console.print(table)

            print("")

            table = Table(
                show_header=False,
                header_style='bold #2070b2',
                title='[bold]Selection[/]'
            )
            table.add_row("1", "Start Workout")
            table.add_row("2", "Choose Different Workout")
            table.add_row("3", "Main Menu")
            table.add_row("4", "Quit")

            console.print(table)

        else:
            i = 0
            self._print_banner(f"Workout: {workout_name}")

            max_len_name, max_len_equipment, max_len_alternating_sides, max_len_body_position = self._get_max_len_columns(workout_name)

            print(f"{'Num': <{3}} {'Exercise Name':<{max_len_name}} {'Equipment':<{max_len_equipment}} {'Alternating Sides':^{max_len_alternating_sides}} {'Body Position':<{max_len_body_position}}")
            for exercise in self.config["workouts"][workout_name]["exercises"]:
                i += 1
                alternating = "Yes" if exercise["alternating_sides"] else "No"
                print(f"{i:<{3}} {exercise['name']:<{max_len_name}} {exercise['equipment']:<{max_len_equipment}} {alternating:^{max_len_alternating_sides}} {exercise['body_position']:<{max_len_body_position}}")

            print("\n1. Start Workout")
            print("2. Choose Different Workout")
            print("3. Main Menu")
            print("4. Quit")

        answer = None

        while answer is None:
            answer = input("Choose: ")
            if answer is None or answer == "":
                answer = None
                continue

        answer = int(answer)
        if answer == 1:
            self._start_workout(workout_name)
        elif answer == 2:
            self._display_select_workout_menu()
        elif answer == 3:
            self._display_main_menu()
        elif answer == 4:
            self._quit()


    def _start_workout(self, workout_name: str) -> None:
        self.current_workout_name = workout_name
        print("\nStarting workout")
        self.config["current_workout"] = {
            "workout_name": workout_name,
            "start_time": datetime.now(),
            "exercises": {}
        }

        self._workout_session_start_time = datetime.now()
        self.current_exercise_number = 0
        self._next_exercise()

    def _next_exercise(self) -> None:
        self._reinit_weight_and_reps()
        if self.current_exercise_number < len(self.config["workouts"][self.current_workout_name]["exercises"]):
            exercise = self.config["workouts"][self.current_workout_name]["exercises"][self.current_exercise_number]
            self._start_exercise(exercise)
        else:
            self._end_workout()

    def _end_workout(self) -> None:
        self._workout_session_end_time = datetime.now()
        self._workout_session_elapsed_time = self._workout_session_end_time - self._workout_session_start_time
        self._workout_session_elapsed_time = str(self._workout_session_elapsed_time).split(".")[0]
        self.config["current_workout"]["end_time"] = self._workout_session_end_time
        self._quit()

    def _start_exercise(
            self,
            exercise: Dict[str, Union[str, bool]],
            ) -> None:
        self.current_exercise = exercise
        self.current_exercise_name = exercise["name"]

        if DEFAULT_RICH:

            table = Table(
                show_header=False,
                header_style='bold #2070b2',
                title=f'[bold]Ready to begin exercise #{self.current_exercise_number + 1}?[/]'
            )

            table.add_row("Name", f"{exercise['name']}")
            table.add_row("Equipment", f"{exercise['equipment']}")
            table.add_row("Body Position", f"{exercise['body_position']}")
            if exercise['alternating_sides']:
                table.add_row("Alternating Sides", "Yes")
            else:
                table.add_row("Alternating Sides", "No")

            console.print(table)


            print("")

            table = Table(
                show_header=False,
                header_style='bold #2070b2',
                title='[bold]Selection[/]'
            )
            table.add_row("1", "Start Execise")
            table.add_row("2", "Skip This Exercise")
            table.add_row("3", f"Review Exercises for workout '{self.current_workout_name}'")
            table.add_row("4", "Select Workout")
            table.add_row("5", "Main Menu")
            table.add_row("6", "Quit")

            console.print(table)

        else:
            print(f"\nReady to begin exercise #{self.current_exercise_number + 1}?")
            print(f"Name: {exercise['name']}")
            print(f"Equipment: {exercise['equipment']}")
            print(f"Body Position: {exercise['body_position']}")
            if exercise['alternating_sides']:
                print("Alternating Sides: Yes")
            else:
                print("Alternating Sides: No")

            print("\n1. Start Exercise")
            print("2. Skip This Exercise")
            print(f"3. Review Exercises for workout '{self.current_workout_name}'")
            print("4. Select Workout")
            print("5. Main Menu")
            print("6. Quit")

        answer = None
        while True:
            answer = input("Choose [1]: ")
            if answer is None or answer == "":
                answer = "1"
            try:
                answer = int(answer)
            except ValueError:
                answer = None
                continue

            if answer == 1:
                set_number = 0
                for i in range(3):
                    set_number += 1
                    self._start_set(set_number)
                self.current_exercise_number += 1
                self._end_exercise()
                self._next_exercise()

            elif answer == 2:
                self._workout_session_exercises_not_completed += 1
                self.current_exercise_number += 1
                self._next_exercise()
            elif answer == 3:
                self._display_exercises_in_workout(self.current_workout_name)
            elif answer == 4:
                self._display_select_workout_menu()
            elif answer == 5:
                self._display_main_menu()
            elif answer == 6:
                self._quit()
            else:
                answer = None

    def _end_exercise(self) -> None:
        self._workout_session_exercises_completed += 1

    def _start_set(self, set_number: int) -> None:
        print(f"\nStarting set number: '{set_number}'")
        print(f"Exercise: '{self.current_exercise_name}'")

        self._sleep_or_interrupt(self.seconds_before_start_exercise)

        elapsed_time = self._start_set_timer()

        print(f"You completed that set in '{elapsed_time}' seconds\n")

        self._end_set(set_number, elapsed_time)

    def _get_weight_or_rep(
        self,
        name: str = "weight",
        previous: Optional[int] = None,
        side: Optional[str] = None) -> int:

        val = None
        question = None

        if previous is None:
            if side is None:
                question = f"Enter {name}: "
            else:
                question = f"Enter {side} {name}: "
        else:
            if side is None:
                question = f"Enter {name} [{previous}]: "
            else:
                question = f"Enter {side} {name} [{previous}]: "

        while val is None:
            val = input(question)

            if val is None or val == "":
                if previous is None or previous == "":
                    val = None
                    continue
                else:
                    val = previous

            try:
                val = int(val)
            except ValueError:
                val = None
                continue

        return val

    def _end_set(self, set_number: int, elapsed_time: float) -> None:
        leftside_reps = None
        leftside_weight = None
        rightside_reps = None
        rightside_weight = None

        weight = None
        reps = None

        if self.current_exercise_name not in self.config["current_workout"]["exercises"]:
            self.config["current_workout"]["exercises"][self.current_exercise_name] = {}

        if "sets" not in self.config["current_workout"]["exercises"][self.current_exercise_name]:
            self.config["current_workout"]["exercises"][self.current_exercise_name]["sets"] = {}

        if self.current_exercise["alternating_sides"]:

            leftside_weight = self._get_weight_or_rep(
                name="weight",
                previous=self.previous_leftside_weight,
                side="leftside"
            )

            leftside_reps = self._get_weight_or_rep(
                name="reps",
                previous=self.previous_leftside_reps,
                side="leftside"
            )

            previous_weight = leftside_weight
            if self.previous_rightside_weight is not None:
                previous_weight = self.previous_rightside_weight

            rightside_weight = self._get_weight_or_rep(
                name="weight",
                previous=previous_weight,
                side="rightside"
            )

            previous_reps = leftside_reps
            if self.previous_rightside_reps is not None:
                previous_reps = self.previous_rightside_reps

            rightside_reps = self._get_weight_or_rep(
                name="reps",
                previous=previous_reps,
                side="rightside"
            )


            self.previous_leftside_weight = leftside_weight
            self.previous_rightside_weight = rightside_weight
            self.previous_leftside_reps = leftside_reps
            self.previous_rightside_reps = rightside_reps

            self.config["current_workout"]["exercises"][self.current_exercise_name]["sets"][set_number] = {
                "seconds": float(elapsed_time),
                "leftside_reps": leftside_reps,
                "leftside_weight": leftside_weight,
                "rightside_reps": rightside_reps,
                "rightside_weight": rightside_weight,
            }

        else:

            weight = self._get_weight_or_rep(
                name="weight",
                previous=self.previous_weight
            )

            self.previous_weight = weight

            reps = self._get_weight_or_rep(
                name="reps",
                previous=self.previous_reps
            )

            self.previous_reps = reps

            self.config["current_workout"]["exercises"][self.current_exercise_name]["sets"][set_number] = {
                "seconds": float(elapsed_time),
                "reps": reps,
                "weight": weight,
            }

        if set_number == 1 or set_number == 2:

            print(f"\nBreak for '{self.interset_break_seconds}' seconds")
            if "interset_messages" in self.config:
                messages = self.config["interset_messages"]
                for messsage in messages:
                    print(messsage)

            self._display_countdown(self.interset_break_seconds)

    def _display_countdown(self, seconds: int) -> None:
        """Display a countdown timer for the given number of seconds

        Args:
            seconds (int): The number of seconds to countdown
        """
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Break[/]", total=seconds)
            try:
                for i in range(seconds):
                    time.sleep(1)
                    progress.update(task, advance=1)
            except KeyboardInterrupt:
                progress.stop()
                print("\nBreak interrupted by user (Ctrl+C).")

    def _display_review_previous_workout_menu(self) -> None:
        self._display_menu_banner("Review Previous Workout")
        self._display_previous_workouts()
        self._display_menu("Review Previous Workout")
        self._prompt_user("Review Previous Workout")

    def _display_previous_workouts(self) -> None:
        pass


    def _display_menu(self, menu_name: str, display_border: bool = True) -> None:

        if menu_name == "Quit":
            self._quit()

        if menu_name not in self.config["menus"]:
            raise Exception(f"Could not find menu '{menu_name}'")

        start = self.current_option_number + 1

        # if display_border:
        #     print("\n=====================================")

        for i, option in enumerate(self.config["menus"][menu_name]["options"], start=start):
            # option_name = self.config["menus"][menu_name]["options"][option]
            print(f"{i}. {option}")
            self.current_option_number = i
            self.selection_lookup[i] = option
            # self.current_option_number = int(option)
        # print("Displayed menu")

    def _prompt_user(self, menu_name: str) -> None:
        answer = None
        while answer is None:
            answer = input("Choose: ")
            if answer is None or answer == "":
                answer = None
                continue

            try:
                answer = int(answer)
            except ValueError:
                answer = None
                continue

            if answer not in self.selection_lookup:
                answer = None
                continue

            selection = self.selection_lookup[answer]
            if selection == "Quit":
                self._quit()

            if selection not in self.config["functions"]:
                raise Exception(f"Seletion '{selection}' does not exist in the functions lookup!")

            self.current_option_number = 0
            self.selection_lookup = {}
            self.config["functions"][selection]()

    def _quit(self) -> None:
        if "current_workout" in self.config and self.config["current_workout"] is not None:

            if DEFAULT_RICH:

                table = Table(
                    show_header=False,
                    header_style='bold #2070b2',
                    title='[bold]Workout Session Summary[/]'
                )

                table.add_row("Workout Name", f"{self.current_workout_name}")
                table.add_row("Start Time", f"{self._workout_session_start_time}")
                table.add_row("End Time", f"{self._workout_session_end_time}")
                table.add_row("Elapsed Time", f"{self._workout_session_elapsed_time}")
                table.add_row("Exercises Completed", f"{self._workout_session_exercises_completed}")
                table.add_row("Exercises Not Completed", f"{self._workout_session_exercises_not_completed}")

                console.print(table)
            else:

                print("\n=====================================")
                print("Workout Session Summary")
                print(f"{self.current_workout_name}")
                print(f"Start Time: {self._workout_session_start_time}")
                print(f"End Time: {self._workout_session_end_time}")
                print(f"Elapsed Time: {self._workout_session_elapsed_time}")
                print(f"Exercises Completed: {self._workout_session_exercises_completed}")
                print(f"Exercises Not Completed: {self._workout_session_exercises_not_completed}")
            self._save_workout_session()
        else:
            print("No workout session to summarize and save")


        sys.exit(0)

    def _save_workout_session(self) -> None:
        if self.outfile is None or self.outfile == "":
            # Save the workout session to the workout file
            # Get current date in YYY-MM-DD format
            current_date = datetime.now().strftime("%Y-%m-%d")
            outdir = self.config["workout_file"]["outdir"]
            if not os.path.exists(outdir):
                pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
                logging.info(f"Created directory '{outdir}'")
            outfile = os.path.join(outdir, f"{current_date}.yaml")
        else:
            outfile = self.outfile

        # Save the workout session to the workout file
        # Write the Python dictionary to a YAML file
        with open(outfile, "w") as file:
            documents = yaml.dump(self.config["current_workout"], file)

        console.print(f"Saved workout session to '{outfile}'")
        logging.info(f"Saved workout session to '{outfile}'")

    def _sleep_or_interrupt(self, timeout: int) -> None:
        print(f"Get ready to start in {timeout} seconds.")
        print("Press Enter to start immediately.")
        try:
            # Wait for the specified time or until Enter key is pressed
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if rlist:
                # Enter key pressed, interrupt the sleep
                sys.stdin.readline()
                # print("Pause interrupted by user.")
            else:
                # print("Break over.")
                pass
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nPause interrupted by user (Ctrl+C).")

    def _start_set_timer(self, seconds_per_set: int = None) -> float:
        if seconds_per_set is None:
            seconds_per_set = self.config["seconds_per_set"]


        f = Figlet(font='big')

        print(colored(f.renderText('Start'), 'green'))

        print("\nStarted the timer for the set.")
        print("Press [Enter] to stop the timer.")

        start_time = time.time()
        elapsed_time = 0

        try:
            # Wait for the specified time or until Enter key is pressed
            rlist, _, _ = select.select([sys.stdin], [], [], seconds_per_set)

            elapsed_time = time.time() - start_time
            if rlist:
                # Enter key pressed, interrupt the sleep
                sys.stdin.readline()
                print("Timer stopped.")
            else:
                print("Time exceeded for completing the set.  Everything okay?")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nSet interrupted by user (Ctrl+C).")

        return f"{elapsed_time:.2f}"


def main() -> None:
    tracker = Tracker()
    tracker.run()


if __name__ == "__main__":
    main()
