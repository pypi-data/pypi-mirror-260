def write_to_file(msg, file_name):
    with open(file_name, 'a') as f:
        f.write(f"{msg}\n")
