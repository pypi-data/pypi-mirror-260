import json
import os


def read_events(path, exclude_legacy=False):
    journal_paths = []

    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        
        if os.path.isfile(entry_path) and entry.startswith("Journal.") and entry.endswith(".log"):
            if exclude_legacy and "-" not in entry:
                continue

            journal_paths.append(entry_path)
    
    for i in range(len(journal_paths)):
        path = journal_paths[i]
        
        for event in _read_journal(path):
            yield event
        
        progress_text = f"{i+1}/{len(journal_paths)} journal files processed"
        if i == len(journal_paths) - 1:
            print(" " * len(progress_text), flush=True, end="\r")
        else:
            print(progress_text, flush=True, end="\r")


def _read_journal(path):
    with open(path) as journal_file:
        for line in journal_file:
            event = json.loads(line)
            
            yield event
