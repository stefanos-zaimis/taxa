import requests
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum

class Code(Enum):
    BACTERIAL = "BACTERIAL"
    BOTANICAL = "BOTANICAL"
    CULTIVARS = "CULTIVARS"
    PHYTO = "PHYTO"
    VIRUS = "VIRUS"
    ZOOLOGICAL = "ZOOLOGICAL"
    PHYLO = "PHYLO"

class LastImportState(Enum):
    WAITING = "WAITING"
    PREPARING = "PREPARING"
    DOWNLOADING = "DOWNLOADING"
    PROCESSING = "PROCESSING"
    DELETING = "DELETING"
    INSERTING = "INSERTING"
    MATCHING = "MATCHING"
    INDEXING = "INDEXING"
    ANALYZING = "ANALYZING"
    ARCHIVING = "ARCHIVING"
    EXPORTING = "EXPORTING"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class Origin(Enum):
    EXTERNAL = "EXTERNAL"
    PROJECT = "PROJECT"
    RELEASE = "RELEASE"
    XRELEASE = "XRELEASE"

class Type(Enum):
    NOMENCLATURAL = "NOMENCLATURAL"
    TAXONOMIC = "TAXONOMIC"
    PHYLOGENETIC = "PHYLOGENETIC"
    ARTICLE = "ARTICLE"
    LEGAL = "LEGAL"
    THEMATIC = "THEMATIC"
    IDENTIFICATION = "IDENTIFICATION"
    OTHER = "OTHER"

class License(Enum):
    CC0 = "CC0"
    CC_BY = "CC_BY"
    CC_BY_SA = "CC_BY_SA"
    CC_BY_NC = "CC_BY_NC"
    CC_BY_ND = "CC_BY_ND"
    CC_BY_NC_SA = "CC_BY_NC_SA"
    CC_BY_NC_ND = "CC_BY_NC_ND"
    UNSPECIFIED = "UNSPECIFIED"
    OTHER = "OTHER"

class SortBy(Enum):
    KEY = "KEY"
    ALIAS = "ALIAS"
    TITLE = "TITLE"
    CREATOR = "CREATOR"
    RELEVANCE = "RELEVANCE"
    CREATED = "CREATED"
    MODIFIED = "MODIFIED"
    IMPORTED = "IMPORTED"
    LAST_IMPORT_ATTEMPT = "LAST_IMPORT_ATTEMPT"
    SIZE = "SIZE"


@dataclass
class DatasetFilter:
    offset: Optional[int] = 0
    limit: Optional[int] = 1000
    title: Optional[str] = None
    alias: Optional[str] = None
    code: Optional[Code] = None
    code_is_null: Optional[bool] = None
    private: Optional[bool] = None
    released_from: Optional[int] = None
    contributes_to: Optional[int] = None
    has_source_dataset: Optional[int] = None
    has_gbif_key: Optional[bool] = None
    gbif_key: Optional[str] = None
    gbif_publisher_key: Optional[str] = None
    without_sector_in_project: Optional[int] = None
    last_import_state: Optional[LastImportState] = None
    editor: Optional[int] = None
    reviewer: Optional[int] = None
    origin: Optional[List[Origin]] = None
    data_type: Optional[List[Type]] = None
    checklist_license: Optional[List[License]] = None
    row_type: Optional[List[object]] = None
    modified: Optional[str] = None
    modified_before: Optional[str] = None
    modified_by: Optional[str] = None
    created: Optional[str] = None
    created_before: Optional[str] = None
    created_by: Optional[str] = None
    issued: Optional[str] = None
    issued_before: Optional[str] = None
    min_size: Optional[int] = None
    sort_by: Optional[SortBy] = None
    reverse: Optional[bool] = None


# Base URL for the Catalogue of Life ChecklistBank API
SEARCH_URL = "https://api.checklistbank.org/nameusage/search"

# URL for dataset searching
DATASET_URL = "https://api.checklistbank.org/dataset"

def get_dataset(search_filters=None, size=None):
    """
    Retrieve a list of checklists for a requested dataset/purpose.
    
    Parameters:
    search_filters (dict): A dictionary of parameters used to filter datasets (default is None). This should be done via using the dataclass DatasetFilter asdict.
    size (int): The size of the list we want returned (default is None). If the list size is None, then this means we will get ALL of them.

    Returns:
    list: A list of datasets
    """
    limit = search_filters['limit']
    offset = search_filters["offset"]

    response = requests.get(DATASET_URL, params=search_filters)

    if response.status_code != 200:
        print(f"Error: {response.status_code} for URL: {response.url}")
        return None

    try:
        data = response.json()
    except:
        print("There was an error parsing the file, maybe it's not JSON?")
        return

    total_checklists = data['total'] - offset - limit

    return data

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
    search = DatasetFilter(
        limit=2
    )
    print(get_dataset(search_filters=asdict(search)))