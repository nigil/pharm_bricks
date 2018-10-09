import os
import time


def delete_old_reaction_files(result_file_dir):
    now = time.time()

    for past_file in os.listdir(result_file_dir):
        past_file_path = os.path.join(result_file_dir, past_file)
        created_time = os.path.getmtime(past_file_path)

        if (now - created_time) > 60 * 10:
            os.remove(past_file_path)
