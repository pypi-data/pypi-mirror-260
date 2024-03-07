from tributaries import my_sweep, my_plots, my_checkpoints


# Launching

# List of hyperparams to launch
my_sweep.hyperparams = [
    f"""task=classify/imagenet
    Eyes=ResNet50
    experiment=ImageNet
    ram_capacity=1.3e6
    dataset.transform='transforms.Compose([transforms.Resize(64),transforms.CenterCrop(64)])'
    dataset.root=/home/cxu-serve/p1/datasets/imagenet/
    """
]

my_sweep.mem = 160

# Plotting

my_plots.plots.append(['ImageNet'])  # Lists of experiments to plot together, supports regex .*!
my_plots.title = 'ResNet50 On ImageNet-1k'

# Checkpoints

my_checkpoints.experiments = my_plots.plots[0]
