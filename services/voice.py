from typing import Self, List, Tuple
import logging
from thefuzz import fuzz
from config import settings 

logger = logging.getLogger(__name__)


class VoiceService:
    """
    A singleton service responsible for searching and filtering voice samples.

    This service implements the Singleton pattern to ensure only one instance 
    manages the voice data throughout the application lifecycle.

    :ivar voices: Dictionary containing voice names and their corresponding IDs.
    :vartype voices: dict
    """
    _instance: Self = None

    def __new__(cls) -> Self:
        """
        Create or return the existing singleton instance of VoiceService.

        :return: The singleton instance of VoiceService.
        :rtype: VoiceService
        """
        if cls._instance is None:
            logger.debug("Create new VoiceService object.")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the service with settings and default thresholds.

        Ensures initialization occurs only once, even if __init__ is called multiple times.
        """
        if not hasattr(self, "_initialized"):
            self.voices = settings.VOICES
            self._initialized = True
            self._limit = 50
            self._threshold = 70

    def __call__(self, query: str) -> List[Tuple[str, str]]:
        """
        Execute the voice search orchestration flow.

        Cleans the input, filters available voices based on fuzzy matching, 
        and returns a sorted list of relevant results.

        :param query: The search string provided by the user.
        :type query: str
        :return: A list of tuples containing voice names and file IDs.
        :rtype: List[Tuple[str, str]]
        """
        logger.debug("search orchestrator")

        clean_query = self._prepare_query(query)

        if not clean_query:
            return self._get_default_voices()

        filtered = self._filter_voices(clean_query)
        sorted_results = self._sort_results(clean_query, filtered)

        return sorted_results[:self._limit]

    def _prepare_query(self, query: str) -> str:
        """
        Sanitize the input query for consistent matching.

        :param query: Raw input string.
        :type query: str
        :return: Lowercased and stripped search query.
        :rtype: str
        """
        logger.debug("Cleaning the input.")
        return query.lower().strip() if query else ""

    def _get_default_voices(self) -> List[Tuple[str, str]]:
        """
        Retrieve the default set of voices when no query is provided.

        :return: A list of the first N voices defined by the internal limit.
        :rtype: List[Tuple[str, str]]
        """
        logger.debug("Returns the default list.")
        return list(self.voices.items())[:self._limit]

    def _is_match(self, query: str, name: str) -> bool:
        """
        Check if a voice name matches the search query using fuzzy logic.

        Matches if the query is a substring of the name or if the fuzzy 
        partial ratio exceeds the predefined threshold.

        :param query: The cleaned search string.
        :type query: str
        :param name: The voice name to check against.
        :type name: str
        :return: True if it's a match, False otherwise.
        :rtype: bool
        """
        logger.debug("Verification.")
        name_lower = name.lower()
        return query in name_lower or fuzz.partial_ratio(query, name_lower) > self._threshold

    def _filter_voices(self, query: str) -> List[Tuple[str, str]]:
        """
        Filter the entire voice collection based on the search query.

        :param query: The cleaned search string.
        :type query: str
        :return: List of voices that passed the matching criteria.
        :rtype: List[Tuple[str, str]]
        """
        logger.debug("Selection of votes that match the query.")
        return [
            (name, file_id) 
            for name, file_id in self.voices.items() 
            if self._is_match(query, name)
        ]

    def _sort_results(self, query: str, results: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """
        Sort the filtered results by relevance using the Levenshtein distance ratio.

        :param query: The cleaned search string used for comparison.
        :type query: str
        :param results: The list of filtered (name, id) tuples.
        :type results: List[Tuple[str, str]]
        :return: Results sorted in descending order of similarity.
        :rtype: List[Tuple[str, str]]
        """
        logger.debug("Sort by relevance.")

        return sorted(
            results, 
            key=lambda x: fuzz.ratio(query, x[0].lower()), 
            reverse=True
        )
