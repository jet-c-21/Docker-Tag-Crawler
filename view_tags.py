import pandas as pd

csv_path = 'nvidia_cuda_tags.csv'
df = pd.read_csv(csv_path)

filtered_df = df[df['tag'].str.contains('ubuntu18.04') &
                 df['tag'].str.contains('devel')]
print(filtered_df, '\n')


def get_pull_and_run_command(df, idx: int):
    picked_tag = df.iloc[idx]
    image_name = f"{picked_tag['repo']}:{picked_tag['tag']}"
    print(f"image = {image_name} \n")

    pull_cmd = f"docker pull {image_name}"
    run_cmd = f"docker run --gpus all -it --rm {image_name}"

    print(pull_cmd)
    print(run_cmd)


get_pull_and_run_command(df, 71)
