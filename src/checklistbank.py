import requests
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum
import asyncio
import aiohttp

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
    modified: Optional[str] = None # Date in the form 2024-09-06
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
BASE_URL = "https://api.checklistbank.org/"

DATASET_ENDPOINT = "dataset"

def get_dataset(search_filters={}, size=None):
    """
    Retrieve a list of checklists for a requested dataset/purpose.
    
    Parameters:
    search_filters (dict): A dictionary of parameters used to filter datasets (default is None). 
                           This should be done via the DatasetFilter dataclass, using asdict.
    size (int): The size of the list we want returned (default is None). 
                If the list size is None, then this means we will get ALL of them.

    Returns:
    list: A list of datasets
    """

    url = BASE_URL+DATASET_ENDPOINT

    limit = search_filters.get('limit', 1000)
    offset = search_filters.get('offset', 0)

    datasets = []
    total_fetched = 0
    total_datasets =  None
    id = 0
    while True:
        print("run ", id)
        id+=1
        search_filters['limit'] = min(limit,1000) # Ensure the limit is 1000 or under
        search_filters['offset'] = offset

        # Make response
        response = requests.get(url, params=search_filters)

        # Check response validity
        if response.status_code != 200:
            print(f"Error: {response.status_code} for URL: {response.url}")
            return None

        # Try parsing response
        try:
            data = response.json()
        except:
            print("Error: The file could not be parsed, maybe it's not JSON?")
            return None
        
        # Get the datasets from the response
        current_datasets = data.get('result', [])
        datasets.extend(current_datasets)
        total_fetched += len(current_datasets)

        # Get the total number of checklists
        if total_datasets is None:
            total_datasets = data.get('total', 0)
        
        #Check if we fetched the requested number of datasets (or all of them if the size is None)
        if size is not None and total_fetched >= size:
            return datasets[:size]  # Return only the requested number of datasets

        if total_fetched >= total_datasets:
            return datasets
        
        offset += limit
    return datasets

# Example usage
def main():
    print(len(get_dataset()))

# Run the function
if __name__ == "__main__":
    main()