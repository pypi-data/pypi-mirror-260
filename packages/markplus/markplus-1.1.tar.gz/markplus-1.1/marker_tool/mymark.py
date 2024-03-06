import sys

from marker_tool.interpreter import Interpreter
from marker_tool.utils import write_json_to_file


def main() -> None:
    # Check for correct number of arguments.
    if len(sys.argv) != 4:
        raise ValueError(
            (
                "Insufficient arguments! Expected 3 arguments <module_name> "
                f"<exercise_name> <code_path> but got {len(sys.argv) - 1}"
            )
        )

    # Mark code and write feedback.

    interpreter = Interpreter(sys.argv[1], sys.argv[2], sys.argv[3], debug_mode=True)
    interpreter.run()

    marks = interpreter.get_marks()
    feedback = interpreter.get_feedback()

    write_json_to_file("./comments.json", feedback)
    write_json_to_file("./marks.json", marks)

    interpreter.print_warnings()


if __name__ == "__main__":
    main()
