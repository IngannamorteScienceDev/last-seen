from pathlib import Path

from lastseen.parser import parse_dialog_folder


if __name__ == "__main__":
    dialog_path = Path("samples/486429703")

    messages = parse_dialog_folder(dialog_path)

    print(f"Parsed total messages: {len(messages)}")
    print("First message datetime:", messages[0]["datetime"])
    print("Last message datetime:", messages[-1]["datetime"])
