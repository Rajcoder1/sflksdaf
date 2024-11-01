import pandas as pd
import numpy as np

# Load data from a CSV file
file_path = "AdmetLab2.0/Te/Te - RawAdmet.csv"  
name = file_path[:file_path.find(" ")]
df = pd.read_csv(file_path)

# Calculate mean and standard deviation for each column
summary_data = df.aggregate(['mean', 'std']).transpose()

# Remove columns where the standard deviation is 0
summary_data = summary_data[summary_data['std'] != 0]

# Create a summary DataFrame with the mean and standard deviation
summary_df = pd.DataFrame({
    'Column Title': summary_data.index,
    'Mean': summary_data['mean'],
    'Standard Deviation': summary_data['std']
})

# Save the summary DataFrame to a CSV file
summary_df.to_csv(str(name + " - summary_output.csv"), index=False)

# Filter the original DataFrame to include only columns that are in summary_data
df_filtered = df[summary_data.index]

# Calculate z-scores for each value in the filtered DataFrame
z_score_df = (df_filtered - summary_data['mean']) / summary_data['std']

# Save the z-scores DataFrame to a CSV file
z_score_output_file = str(name + " - z_scores_output.csv")
z_score_df.to_csv(z_score_output_file, index=False)

# Calculate the sample covariance matrix from the z-scores DataFrame
cov_matrix = z_score_df.cov()  # ddof=1 for sample covariance


# Symmetrize the covariance matrix and set diagonal values to 1
#cov_matrix = (cov_matrix + cov_matrix.T) / 2
#np.fill_diagonal(cov_matrix.values, 1)

# Convert the covariance matrix to a DataFrame
cov_matrix_df = pd.DataFrame(cov_matrix)

# Save the covariance matrix to a CSV file
cov_matrix_df.to_csv(str(name + " - covariance_matrix.csv"), index=True)

# Calculate eigenvalues and eigenvectors from the covariance matrix
# Calculate eigenvalues and eigenvectors from the covariance matrix
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

# Sort eigenvalues in descending order and get the sorted indices
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

# Print the eigenvalues with factor labels
factor_labels = df_filtered.columns
arr=[]
for i, eigenvalue in enumerate(eigenvalues):
    print(f"Factor {i + 1} ({factor_labels[i]}): {eigenvalue}")
    arr.append(i)
arr=np.array(arr)

# Create a DataFrame for eigenvalues with sorted factor labels
eigenvalues_df = pd.DataFrame({'Factor': factor_labels[arr], 'Eigenvalue': eigenvalues})

# Save the eigenvalues DataFrame to a CSV file
eigenvalues_df.to_csv(str(name + " - eigen_output.csv"), index=False)

