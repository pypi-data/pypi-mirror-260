# MLChemTools Python Package

## Overview

**MLChemTools** is a Python package designed to streamline cheminformatics workflows, particularly in the field of machine learning for chemistry (MLChem). It provides a range of functionalities that simplify and expedite common cheminformatics tasks. Leveraging established libraries such as RDKit, Mordred, and PubChem, MLChemTools offers the following key features:

### Chemical Descriptor Generation

MLChemTools facilitates the generation of diverse chemical descriptors, including fingerprints and molecular properties, utilizing the capabilities of RDKit and Mordred. These descriptors encapsulate crucial chemical information essential for machine learning tasks.

### Data Preprocessing

The package streamlines data preprocessing, a fundamental step in machine learning. It assists in handling tasks like data cleaning, normalization, and feature engineering, ensuring the data is suitable for machine learning algorithms.

### Machine Learning Model Building

MLChemTools empowers users to construct and evaluate machine learning models for both classification and regression problems within the realm of chemistry. This enables the exploration of various relationships between chemical structures and desired properties or activities.

By offering a user-friendly and comprehensive collection of tools, MLChemTools aims to:

- **Enhance Efficiency:** Automate and streamline repetitive cheminformatics tasks, allowing researchers to focus on more strategic aspects of their work.
- **Reduce Complexity:** Provide an intuitive interface that lowers the barrier to entry for individuals with varying levels of cheminformatics expertise.
- **Promote Reproducibility:** Encourage the development and sharing of reproducible cheminformatics workflows by facilitating code and data organization.

In essence, MLChemTools serves as a valuable asset for researchers and practitioners in MLChem, aiding them in efficiently constructing, evaluating, and deploying machine learning models to address diverse chemical problems.

## Functions

1. **`cal_rdkit_descriptor(input_file, output_file, smiles_column):`**
    - **Parameters:**
        - `input_file`: Path to the input CSV file containing SMILES data.
        - `output_file`: Path to the output CSV file to save the data with RDKit descriptors.
        - `smiles_column`: Name of the column containing SMILES strings in the input CSV file.
    - **Description:** Calculates RDKit descriptors for each molecule in the input CSV file based on the provided SMILES column. It removes duplicates, adds a new column with RDKit molecule objects, calculates descriptors, and saves the data with descriptors to a new CSV file.

2. **`calculate_pubchem_fingerprints(df_unique, smiles_column):`**
   - **Parameters:**
     - `df_unique`: A pandas DataFrame containing unique molecules.
     - `smiles_column`: Name of the column containing SMILES strings in the DataFrame.
   - **Description:** Calculates PubChem fingerprints for each molecule in the provided DataFrame based on the SMILES column. It utilizes external PaDEL software and requires downloading fingerprint XML files before use. The calculated fingerprints are returned as a new DataFrame.

3. **`cal_lipinski_descriptors(file_path, smiles_column, verbose=False):`**
   - **Parameters:**
     - `file_path`: Path to the input CSV file containing SMILES data.
     - `smiles_column`: Name of the column containing SMILES strings in the input CSV file.
     - `verbose` (optional): Boolean flag indicating whether to print additional information (default: False).
   - **Description:** Calculates Lipinski descriptors (molecular weight, LogP, the number of hydrogen bond donors, and the number of hydrogen bond acceptors) for each molecule in the input CSV file based on the SMILES column. It removes duplicates, calculates descriptors, and saves the data with descriptors to a new CSV file.

4. **`calculate_morgan_fpts(data):`**
   - **Parameters:**
     - `data`: A list of SMILES strings.
   - **Description:** Calculates Morgan fingerprints for each SMILES string in the provided list. It returns a NumPy array containing the fingerprints.

5. **`cal_morgan_fpts(input_file, output_file, smiles_column):`**
   - **Parameters:**
     - `input_file`: Path to the input CSV file containing SMILES data.
     - `output_file`: Path to the output CSV file to save the data with Morgan fingerprints.
     - `smiles_column`: Name of the column containing SMILES strings in the input CSV file.
   - **Description:** Calculates Morgan fingerprints for each molecule in the input CSV file based on the SMILES column. It removes duplicates, calculates fingerprints, and saves the data with fingerprints to a new CSV file.

6. **`calculate_mordred_descriptors(smiles_column):`**
   - **Parameters:**
     - `smiles_column`: A pandas Series containing SMILES strings.
   - **Description:** Calculates Mordred descriptors for each SMILES string in the provided Series. It uses the Mordred library and returns a pandas DataFrame containing the calculated descriptors.

7. **`cal_mordred_descriptors(input_file, output_file, smiles_column):`**
   - **Parameters:**
     - `input_file`: Path to the input CSV file containing SMILES data.
     - `output_file`: Path to the output CSV file to save the data with Mordred descriptors.
     - `smiles_column`: Name of the column containing SMILES strings in the input CSV file.
   - **Description:** Calculates Mordred descriptors for each molecule in the input CSV file based on the SMILES column. It removes duplicates, calculates descriptors, and saves the data with descriptors to a new CSV file.

8. **`diagnosis_csv(file_path):`**
   - **Parameters:**
     - `file_path`: Path to the CSV file to be analyzed.
   - **Description:** Performs a comprehensive analysis of the provided CSV file, including:
     - Identifying missing values and their percentage.
     - Dropping rows with missing values.
     - Displaying information about the cleaned DataFrame (data types, unique values, etc.).
     - Creating histograms and scatter matrices for numeric columns.

9. **`dpreprocess_csv_1(csv_file_path, object_columns):`**
   - **Parameters:**
     - `csv_file_path`: Path to the CSV file to be preprocessed.
     - `object_columns` (optional): List of column names to be converted to categorical codes.
   - **Description:** Preprocesses the CSV file by converting specified object columns to categorical codes.

10. **`preprocess_csv_2(csv_file_path, object_columns=None):`**
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file to be preprocessed.
      - `object_columns` (optional): List of column names to be converted to categorical codes (defaults to None, meaning all object columns are converted).
    - **Description:** Preprocesses the CSV file by converting specified object columns to categorical codes.

11. **`preprocess_csv_3(csv_file_path, object_columns=None):`**
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file to be preprocessed.
      - `object_columns` (optional): List of column names to be converted to categorical codes (defaults to None, meaning all object columns are converted).
    - **Description:** Preprocesses the CSV file by converting specified object columns to categorical codes.

12. **`preprocess_csv_4(csv_file_path, object_columns=None, columns_to_delete=None):`**
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file to be preprocessed.
      - `object_columns` (optional): List of column names to be converted to categorical codes (defaults to None, meaning all object columns are converted).
      - `columns_to_delete` (optional): List of column names to be deleted from the DataFrame.
    - **Description:** Preprocesses the CSV file by converting specified object columns to categorical codes and deleting specified columns.

13. **`preprocess_csv_5(csv_file_path, object_columns=None):`**
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file to be preprocessed.
      - `object_columns` (optional): List of column names to be converted to categorical codes (defaults to None, meaning all object columns are converted that cannot be converted to float).
    - **Description:** Preprocesses the CSV file by converting specified object columns to categorical codes.

14. **`preprocess_csv_6(csv_file_path, object_columns=None, delete_column=None):`**
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file to be preprocessed.
      - `object_columns` (optional): List of column names to be converted to categorical codes (defaults to None, meaning all object columns are converted that cannot be converted to float).
      - `delete_column` (optional): Name of the specific column to be deleted from the DataFrame.
    - **Description:** Preprocesses the CSV file by converting specified object columns to categorical codes and deleting a specific column.

15. **`remove_duplicates(csv_file_path, column_name):`**
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file.
      - `column_name`: Name of the column to use for identifying and removing duplicate entries.

16. **`delete_columns(csv_file_path, columns_to_delete):`**
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file.
      - `columns_to_delete`: List of column names to be deleted from the DataFrame.

17. **`prepare_analyze_and_lazy_predict(file_path, target_column):`**
    - **Description:** Performs exploratory data analysis (EDA), data cleaning, and attempts to fit various regression models.
    - **Parameters:**
      - `file_path`: Path to the CSV file containing the data.
      - `target_column`: Name of the column containing the target variable.
    - **Returns:** None

18. **`explore_and_visualize_regression_data(csv_file_path, target_column_name):`**
    - **Description:** Performs EDA and model evaluation for regression tasks.
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file containing the data.
      - `target_column_name`: Name of the target variable column.
    - **Returns:** None

19. **`get_target_values_meanings(y):`**
    - **Description:** Helps interpret classification models by mapping target variable values to their meanings.
    - **Parameters:**
      - `y`: Pandas Series containing the target variable values.
    - **Returns:** A dictionary mapping each unique target value to its corresponding meaning.

20. **`explore_and_visualize_classification_data(file_path=None, target_column=None):`**
    - **Description:** Performs EDA, model exploration, and evaluation for classification tasks.
    - **Parameters:**
      - `file_path` (optional): Path to the CSV file containing the data. (default: None)
      - `target_column` (optional): Name of the target variable column. (default: None)
    - **Returns:** None

21. **`Random_Forest_Regressor_analysis(csv_file_path, target_column_name):`**
    - **Description:** Performs hyperparameter tuning for a Random Forest Regressor and evaluates its performance.
    - **Parameters:**
      - `csv_file_path`: Path to the CSV file containing the data.
      - `target_column_name`: Name of the target variable column.
    - **Returns:** None

22. **`retrive_data_from_chembl(search_term, condition_column, condition_value, result_column):`**
    - **Description:** Retrieves and displays bioactivity data from the ChEMBL database using a search term and condition.
    - **Parameters:**
      - `search_term`: Search term for proteins.
      - `condition_column`: Name of the column containing the filtering condition.
      - `condition_value`: Value to filter by in the condition_column.
      - `result_column`: Name of the column containing the desired results.
    - **Returns:**
      - `targets_df`: DataFrame containing information about the target proteins.
      - `corresponding_values`: List of values corresponding to the condition_value.
      - `activity_df`: DataFrame containing activity information.
      - `df`: Processed DataFrame containing the protein and its activity.

23. **`finding_important_features_regressor(file_path=None, target_column=None):`**
    - **Description:** Calculates and visualizes feature importance for regression models.
    - **Parameters:**
      - `file_path` (optional): Path to the CSV file containing the data. (default: None)
      - `target_column` (optional): Name of the target variable column. (default: None)
    - **Returns:** None

24. **`finding_important_features_classifier(file_path=None, target_column=None):`**
    - **Description:** Calculates and visualizes feature importance for classification models.
    - **Parameters:**
      - `file_path` (optional): Path to the CSV file containing the data. (default: None)
      - `target_column` (optional): Name of the target variable column. (default: None)
    - **Returns:** None

25. **`other_function_name(parameters):`**
    - **Description:** Brief description of the function.
    - **Parameters:**
      - `parameter1`: Description of parameter1.
      - `parameter2`: Description of parameter2.
    - **Returns:** Description of the return value.

25. **`finding_important_features_classifier(file_path=None, target_column=None):`**
    - **Description:** Calculates and visualizes feature importance for classification models.
    - **Parameters:**
        - `file_path` (optional): Path to the CSV file containing the data (default: None).
        - `target_column` (optional): Name of the target variable column (default: None).
    - **Returns:** None
