import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# File path
file_path = "Overall/XUNdrug/ZSCORE_EIGEN - Z_Score_XUNdrug.csv"  
name = file_path[:file_path.find(" ")]

# Load your dataset
df = pd.read_csv(file_path)

# Select numeric columns (assuming all 74 columns are numeric)
X = df.select_dtypes(include=[np.number])

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA to retain 95% of variance
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

# Get the explained variance ratio
explained_variance = pca.explained_variance_ratio_

# Create a DataFrame with the transformed data (principal components)
pca_columns = [f'PC{i+1}' for i in range(X_pca.shape[1])]
df_pca = pd.DataFrame(X_pca, columns=pca_columns)

# Add explained variance as metadata (optional)
df_variance = pd.DataFrame({'Explained Variance': explained_variance}, index=pca_columns)

# Save the PCA-transformed data to a CSV
df_pca.to_csv(name + " - PCA.csv", index=False)

# Save the explained variance to a separate CSV (optional)
df_variance.to_csv(name + " - Variance.csv")

# Get the PCA components (loadings)
loadings = pca.components_

# Convert the loadings into a DataFrame for better readability
loadings_df = pd.DataFrame(loadings.T, index=X.columns, columns=pca_columns)

# Calculate and add contribution percentages
contributions = loadings_df.pow(2).div(loadings_df.pow(2).sum(axis=0), axis=1) * 100

# Save the loadings and contributions to a CSV file
loadings_df.to_csv(name + ' - loadings.csv')
contributions.to_csv(name + ' - contributions.csv')

# Identify the top contributing factors for each principal component with their contributions
top_contributors = {}

for col in contributions.columns:
    top_factors = contributions[col].sort_values(ascending=False).head(10)  # Change 10 to desired number
    top_contributors[col] = top_factors

# Print the top contributing factors for each principal component with their contributions
for pc, factors in top_contributors.items():
    print(f"\nTop factors contributing to {pc}:")
    for factor, contribution in factors.items():
        print(f"{factor}: {contribution:.2f}%")

print("PCA data, explained variance, loadings, and contributions saved to CSV.")
