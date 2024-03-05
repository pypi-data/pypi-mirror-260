# Welcome to GaussBean!

## A *GAUSS*ian *BE*am *AN*alysis repository, originally made for analysis of passive plasma lens data in the CU WARG group.

As mentioned in the (short) description above, this is a *repository* for Gaussian Beam Analysis. All of the functionality seen in the "gaussbean" folder is associated with a package in PyPi that can be installed at the bottom of the instructions in this README. So, this is simply a repository that all the code is stored in and after you clone it to create the needed conda/mamba environment, you can delete everything that was cloned from GitHub and use "pip install" to install the actual package in the environment that you created.

### Before Installing

Before you try to install GaussBean, make sure that you have Anaconda (or some fork of Anaconda, like Miniconda or Mamba) installed. Instructions on how to install each of those are given at the links below:

Anaconda: https://docs.anaconda.com/free/anaconda/install/index.html \
Miniconda: https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html \
Mamba: https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html

If those links don't work, you should be able to just Google "____ installation" and find out how to install any of those distributions.

### Dependencies

There are dependencies needed for GaussBean, but when creating the environment itself, all of the necessary dependencies should automatically install if they aren't already on your system.

### Installation

GaussBean was originally built using Anaconda, so once you have the Anaconda (or forked) distribution installed (as mentioned above), go to your <ins>terminal</ins> and use Git to clone GaussBean from this repository (if you have access to the CU-PWFA organization) :

```
git clone https://github.com/CU-PWFA/GaussBean.git
```

Alternatively, you can use the following command, which should work even if you are not a part of the CU-PWFA organization:

```
git clone https://github.com/leahghartman/GaussBean
```

Now, from your terminal, navigate to the top level of the directory where GaussBean was cloned (if you run the command "ls -a," you should see a file named "gaussbean.yml"; if you don't see this file, you are not at the top level of the directory) and run the following command:

```
conda env create -f gaussbean.yml
```

This command *should* create a conda (or mamba) environment named "gaussbean". If the environment won't build, you can create your own conda environment and manually install all of the dependencies listed in the "gaussbean.yml" file.

Now, enter the environment that we just created using the command below in the terminal:

```
conda activate gaussbean
```

Finally, install the gaussbean package using pip (note: this is a force-install because issues were occurring with the package not updating even after updating the PyPi package itself):

```
pip install --no-cache-dir --upgrade gaussbean
```

Once you're done with this step, you can pretty much delete the top level of the directory related to this package. Every time you want to do any data analysis with this package, you can just activate the conda/mamba environment, open a Jupyter Notebook, select the "gaussbean" kernel, import gaussbean, and go to town!

And that's it! Have fun! :)

### Setting up IPython

If you are using JupyterLab, a single Jupyter Notebook, or an application like Spyder, you can use the following command in your terminal to use <ins>ipykernel</ins>, which makes it easier to use our new environment in any of the previously-listed applications:

```
python -m ipykernel install --user --name=gaussbean
```

Now, when you open (or create) a Jupyter Notebook, it should give you the option to use the "gaussbean" kernel.

### Using GaussBean

If you want an example of how to use GaussBean, you can take a look into the "examples" folder in the GitHub repository, where you should find an example Jupyter Notebook that goes through *most* of the functionality of the package.

If you have questions, there is lots of documentation in the .py files themselves (inputs, function purposes, comments, etc.), the example notebook previously mentioned, and detailed documentation of each function and everything the package can do on PyPi. If you want to raise a concern about code or an issue, you can open an issue on GitHub, or just contact any of the contributors to the package.

### Uninstalling

To uninstall GaussBean, you can delete the conda/mamba environment using the command below:

```
conda remove --name gaussbean --all
```

Remove all folders and files relating to the GaussBean environment (which you cloned from this repository) and finally, if you installed GaussBean across your entire system rather than just inside the "gaussbean" environment, run

```
pip uninstall gaussbean
```
