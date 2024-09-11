import requests
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum
import asyncio
import aiohttp
import time

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
    q: Optional[str] = None # Full title of the dataset, or whatever other parameter you want
    alias: Optional[str] = None
    code: Optional[Code] = None
    codeIsNull: Optional[bool] = None
    private: Optional[bool] = None
    releasedFrom: Optional[int] = None
    contributesTo: Optional[int] = None
    hasSourceDataset: Optional[int] = None
    hasGbifKey: Optional[bool] = None
    gbifKey: Optional[str] = None
    gbifPublisherKey: Optional[str] = None
    withoutSectorInProject: Optional[int] = None
    lastImportState: Optional[LastImportState] = None
    editor: Optional[int] = None
    reviewer: Optional[int] = None
    origin: Optional[List[Origin]] = None
    type: Optional[List[Type]] = None
    license: Optional[List[License]] = None
    rowType: Optional[List[object]] = None
    modified: Optional[str] = None # Date in the form 2024-09-06
    modifiedBefore: Optional[str] = None
    modifiedBy: Optional[str] = None
    created: Optional[str] = None
    createdBefore: Optional[str] = None
    createdBy: Optional[str] = None
    issued: Optional[str] = None
    issuedBefore: Optional[str] = None
    minSize: Optional[int] = None
    sortBy: Optional[SortBy] = None
    reverse: Optional[bool] = None


# Base URL for the Catalogue of Life ChecklistBank API
SEARCH_URL = "https://api.checklistbank.org/nameusage/search"

# URL for dataset searching
BASE_URL = "https://api.checklistbank.org/"
DATASET_ENDPOINT = "dataset"

async def fetch_dataset_page(session, search_filters, offset):
    """
    Fetch a single page of datasets asynchronously using aiohttp.
    """
    url = BASE_URL + DATASET_ENDPOINT
    search_filters['offset'] = offset
    
    # Log before making the request
    print(f"Making request for offset: {offset}")

    async with session.get(url, params=search_filters) as response:
        response.raise_for_status()
        data = await response.json()

        # Log after receiving the response
        print(f"Received response for offset: {offset}")

        return data.get('result', []), data.get('total', 0)


async def get_dataset_async(search_filters=None, size=None, max_concurrent=2):
    """
    Retrieve datasets asynchronously using aiohttp and asyncio.
    
    Parameters:
    - search_filters (dict): Parameters for filtering datasets.
    - size (int): Number of datasets to retrieve (or None to fetch all).
    - max_concurrent (int): Maximum number of concurrent requests.
    
    Returns:
    list: A list of datasets
    """
    if search_filters is None:
        search_filters = {}

    limit = search_filters.get('limit', 1000)   # Max limit per request is 1000
    search_filters['limit'] = min(1000, limit)
    offset = search_filters.get('offset', 0)
    
    datasets = []
    total_datasets = None
    total_fetched = 0
    
    async with aiohttp.ClientSession() as session:
        # First request to get the total number of datasets and first page of results
        initial_results, total_datasets = await fetch_dataset_page(session, search_filters, offset)
        datasets.extend(initial_results)
        total_fetched += len(initial_results)

        # If we already fetched everything in the first call
        if size is None:
            size = total_datasets

        if total_fetched >= size:
            return datasets[:size]

        # Calculate remaining offsets and schedule tasks
        tasks = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fetch_with_semaphore(offset):
            async with semaphore:
                return await fetch_dataset_page(session, search_filters, offset)

        offsets = range(offset + limit, size, limit)
        for page_offset in offsets:
            tasks.append(fetch_with_semaphore(page_offset))

        # Gather all results concurrently
        results = await asyncio.gather(*tasks)

        # Extend dataset with results from all concurrent pages
        for result in results:
            datasets.extend(result[0])  # result[0] contains the 'result' from fetch_dataset_page
            total_fetched += len(result[0])

            if total_fetched >= size:
                return datasets[:size]

    return datasets[:total_datasets]

async def print_elapsed_time():
    """
    Asynchronous function to print the elapsed time every second.
    """
    start_time = time.time()
    while not stop_timer:  # Stop the timer when the flag is set
        await asyncio.sleep(1)  # Sleep for 1 second
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")


# Example usage
async def main():
    global stop_timer
    
    stop_timer = False  # Declare the flag as global so we can modify it

    search_filters = DatasetFilter(
        limit=1000,   # 1000 records per request
        offset=0     # Start from the beginning
    )
        
    # Run both the dataset fetch and the elapsed time tracker concurrently
    fetch_task = asyncio.create_task(get_dataset_async(search_filters=asdict(search_filters), size=55000, max_concurrent=2))
    timer_task = asyncio.create_task(print_elapsed_time())  # Track elapsed time while fetching datasets

    # Wait for the dataset fetching task to complete
    datasets = await fetch_task

    # Stop the elapsed time tracker
    stop_timer = True
    await timer_task  # Wait for the timer task to finish

    print(f"Retrieved {len(datasets)} datasets.")


if __name__ == "__main__":
    asyncio.run(main())