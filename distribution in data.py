import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
train_df = pd.read_csv(r"C:\Users\ruchi\OneDrive\Desktop\chennai city project\train_data.csv")
val_df = pd.read_csv(r"C:\Users\ruchi\OneDrive\Desktop\chennai city project\val_data.csv")
test_df = pd.read_csv(r"C:\Users\ruchi\OneDrive\Desktop\chennai city project\test_data.csv")

# Select numerical columns (excluding target variable)
features = [col for col in train_df.columns if col != "PM2.5"]

# Plot distributions
plt.figure(figsize=(12, 8))
for feature in features:
    sns.kdeplot(train_df[feature], label=f'Train - {feature}', fill=True, alpha=0.3)
    sns.kdeplot(val_df[feature], label=f'Validation - {feature}', fill=True, alpha=0.3)
    sns.kdeplot(test_df[feature], label=f'Test - {feature}', fill=True, alpha=0.3)
    plt.title(f'Distribution of {feature}')
    plt.legend()
    plt.show()
