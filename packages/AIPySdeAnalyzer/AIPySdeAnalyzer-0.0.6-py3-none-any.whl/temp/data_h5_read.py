import h5py

file_path = 'datasgRNA.h5'  # Replace with your HDF5 file path

# Open the file in read mode
def print_structure(name, obj):
        print(name, type(obj))

with h5py.File(file_path, 'r') as hdf:
    hdf.visititems(print_structure)



# hdf.visititems(print_structure)
# ```

# ### Step 3: Explore the File Structure

# HDF5 files are hierarchical, similar to directories on a filesystem. You may need to explore the structure to find the data you're interested in.

# ```python
#     # List all groups and datasets in the file
#     def print_structure(name, obj):
#         print(name, type(obj))

#     hdf.visititems(print_structure)
# ```

# ### Step 4: Read a Dataset

# Once you've identified the dataset you want to extract, you can read it into memory. Assume `'/my_data'` is the path within the HDF5 file to the dataset you're interested in.

# ```python
#     dataset = hdf['/my_data'][:]  # Read the entire dataset into a NumPy array
# ```

# ### Step 5: Work with the Data

# After reading the dataset into a NumPy array, you can proceed with processing or analyzing the data as needed. For example, you might convert it into a Pandas DataFrame for easier manipulation.

# ```python
# import pandas as pd

# df = pd.DataFrame(dataset)
# print(df)