import requests
from dataclasses import dataclass, asdict 
from typing import List, Optional
from ranks import Rank
from enum import Enum

class Content(Enum):
    SCIENTIFIC_NAME = "SCIENTIFIC_NAME"
    AUTHORSHIP = "AUTHORSHIP"

class SortBy(Enum):
    NAME = "NAME"
    TAXONOMIC = "TAXONOMIC"
    INDEX_NAME_ID = "INDEX_NAME_ID"
    NATIVE = "NATIVE"
    RELEVANCE = "RELEVANCE"

class Facet(Enum):
    USAGE_ID = "USAGE_ID"
    DATASET_KEY = "DATASET_KEY"
    CATALOGUE_KEY = "CATALOGUE_KEY"
    DECISION_MODE = "DECISION_MODE"
    FIELD = "FIELD"
    ISSUE = "ISSUE"
    GROUP = "GROUP"
    NAME_ID = "NAME_ID"
    NOM_CODE = "NOM_CODE"
    NOM_STATUS = "NOM_STATUS"
    PUBLISHER_KEY = "PUBLISHER_KEY"
    RANK = "RANK"
    PUBLISHED_IN_ID = "PUBLISHED_IN_ID"
    SECTOR_KEY = "SECTOR_KEY"
    SECTOR_DATASET_KEY = "SECTOR_DATASET_KEY"
    SECTOR_PUBLISHER_KEY = "SECTOR_PUBLISHER_KEY"
    SECTOR_MODE = "SECTOR_MODE"
    SECONDARY_SOURCE = "SECONDARY_SOURCE"
    SECONDARY_SOURCE_GROUP = "SECONDARY_SOURCE_GROUP"
    STATUS = "STATUS"
    TAXON_ID = "TAXON_ID"
    NAME_TYPE = "NAME_TYPE"
    EXTINCT = "EXTINCT"
    ENVIRONMENT = "ENVIRONMENT"
    AUTHORSHIP = "AUTHORSHIP"
    AUTHORSHIP_YEAR = "AUTHORSHIP_YEAR"
    ALPHAINDEX = "ALPHAINDEX"
    ORIGIN = "ORIGIN"
    UNSAFE = "UNSAFE"

class DataType(Enum):
    PREFIX = "PREFIX"
    WHOLE_WORD = "WHOLE_WORDS"
    EXACT = "EXACT"

@dataclass
class ExactTaxonFilter:
    key: int = 3 # the dataset key
    id: Optional[str] = None # optional taxon id within said dataset
    q: Optional[str] = None
    name: Optional[str] = None
    scientificName: Optional[str] = None
    authorship: Optional[str] = None
    code: Optional[str] = None
    rank: Optional[str] = None
    status: Optional[str] = None
    verbose: Optional[bool] = None
    superkingdom: Optional[str] = None
    kingdom: Optional[str] = None
    subkingdom: Optional[str] = None
    superphylum: Optional[str] = None
    phylum: Optional[str] = None
    subphylum: Optional[str] = None
    superclass: Optional[str] = None
    taxon_class: Optional[str] = None
    subclass: Optional[str] = None
    superorder: Optional[str] = None
    order: Optional[str] = None
    suborder: Optional[str] = None
    superfamily: Optional[str] = None
    family: Optional[str] = None
    subfamily: Optional[str] = None
    tribe: Optional[str] = None
    subtribe: Optional[str] = None
    genus: Optional[str] = None
    subgenus: Optional[str] = None
    section: Optional[str] = None
    species: Optional[str] = None

@dataclass
class TaxonListFilter:
    key: int = 3
    offset: Optional[int] = 0
    limit: Optional[int] = 1000 # The maximum built-in limit
    facetLimit: Optional[int] = None
    content: Optional[List[Content]] = None
    sortBy: Optional[SortBy] = None
    q: Optional[str] = None
    highlight: Optional[bool] = None
    reverse: Optional[bool] = None
    fuzzy: Optional[bool] = None
    minRank: Optional[Rank] = None
    maxRank: Optional[Rank] = None
    facet: Optional[List[Facet]] = None
    type: Optional[DataType] = None

BASE_URL = "https://api.checklistbank.org/"
EXACT_SEARCH_ENDPOINT = "dataset/{key}/match/nameusage"
LIST_SEARCH_ENDPOINT = "dataset/{key}/nameusage/search"

def get_exact_taxon_id(search_filters):
    url = BASE_URL+EXACT_SEARCH_ENDPOINT.format(key=search_filters["key"])

    search_filters["limit"] = min(1000,search_filters["limit"])

    response = requests.get(url, params=search_filters)

    if response.status_code != 200:
        print(f"Error: {response.status_code} for URL: {response.url}")
        return None

    try:
        return response.json()
    except:
        print("Error: The file could not be parsed properly. Maybe it's not JSON?")
        return None

def get_taxa_id_list(search_filters):
    url = BASE_URL+LIST_SEARCH_ENDPOINT.format(key=search_filters["key"])
    response = requests.get(url, params=search_filters)

    if response.status_code != 200:
        print(f"Error: {response.status_code} for URL: {response.url}")
        return None

    try:
        return response.json()
    except:
        print("Error: The file could not be parsed properly. Maybe it's not JSON?")
        return None


def test_exact_taxon_id():
    search_filters = ExactTaxonFilter(
        key=3,
        scientificName="Insecta"
    )
    print(get_exact_taxon_id(search_filters=asdict(search_filters)))