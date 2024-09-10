import requests

# Base URL for the Catalogue of Life ChecklistBank API
SEARCH_URL = "https://api.checklistbank.org/nameusage/search"

# URL for dataset searching
DATASET_URL = "https://api.checklistbank.org/dataset"

def get_dataset(dataset_name = None, dataset_alias = None, limit = 1000, code = None, sort_by = None, type = None):
    """
    Retrieve the dataset key for a requested dataset/purpose.
    
    Parameters:
    dataset_name (str): The exct name of a dataset (e.g. "Catalogue of Life")
    dataset_alias (str): the alias of a dataset (e.g. "COL")
    limit (int): The number of results to return (default is 1000 - the maximum for checklistbank)
    code (enum): The type of nomenclatural code a particular dataset follows (the options are: BACTERIAL, BOTANICAL, CULTIVARS, PHYTO, VIRUS, ZOOLOGICAL, PHYLO)
    sort_by (enum): Sort the results by a given filter (options are: KEY, ALIAS, TITLE, CREATOR, RELEVANCE, CREATED, MODIFIED, IMPORTED, LAST_IMPORT_ATTEMPT, SIZE)
    type (enum): The type of data the dataset holds (options are: NOMENCLATURAL, TAXONOMIC, PHYLOGENETIC, ARTICLE, LEGAL, THEMATIC, IDENTIFICATION, OTHER)
    """

    # Query parameters
    params = {
        "q": dataset_name,
        "alias": dataset_alias,
        "code": code,
        "type": type,
        "limit": limit,
        "sortBy": sort_by
    }

    response = requests.get(DATASET_URL, params=params)

    print (response.json())


def get_key(rank, scientific_name, limit=1):
    """
    Retrieve the dataset key and taxon ID for a given rank and scientific name using the Catalogue of Life ChecklistBank API.

    Parameters:
    rank (str): The taxon rank (e.g., class, family, order).
    scientific_name (str): The scientific name of the taxon (e.g., 'Insecta').
    limit (int): The number of results to return (default is 1).

    Returns:
    tuple: The dataset key and taxon ID of the taxon if found, otherwise None.
    """
    # Query parameters for the API
    params = {
        "q": scientific_name,  # Query string (scientific name)
        "limit": limit,        # Limit the number of results
        "minRank": rank,       # Specify the rank of the taxon
        "maxRank": rank        # Specify the rank of the taxon
    }

    # Perform the API request
    response = requests.get(SEARCH_URL, params=params)

    # Check for errors and raise if bad response
    if response.status_code != 200:
        print(f"Error: {response.status_code} for URL: {response.url}")
        return None

    # Parse the JSON response
    data = response.json()

    # Extract results
    results = data.get('result', [])

    if results:
        # Extract datasetKey and ID
        dataset_key = results[0]['usage'].get('datasetKey')
        taxon_id = results[0]['usage'].get('id')
        
        # Return both datasetKey and ID
        return dataset_key, taxon_id
    else:
        print(f"No results found for {scientific_name} at rank {rank}.")
        return None

# Example usage
def main():
    rank = 'class'              # The rank of the taxon
    scientific_name = 'Insecta'  # The scientific name of the taxon

    result = get_key(rank, scientific_name)
    
    if result:
        dataset_key, taxon_id = result
        print(f"Dataset key for {scientific_name} ({rank}): {dataset_key}")
        print(f"Taxon ID for {scientific_name} ({rank}): {taxon_id}")
    else:
        print(f"Could not find dataset key or taxon ID for {scientific_name} at rank {rank}.")

# Run the function
if __name__ == "__main__":
    #main()
    get_dataset(dataset_alias="COL")