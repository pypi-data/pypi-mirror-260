import time
import concurrent.futures

from rich.console import Console

from .util import MetalArchives
from ..interface import BandProfile, BandExternalLinks, SearchResults


class BandError(Exception):
    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url

    def __repr__(self):
        return self.__name__ + f'<{self.status_code}: {self.url}>'


class Band:

    @staticmethod
    def search_profile(band_name: str, user_agent: str | None = None, **kwargs) -> SearchResults:
        query_str = MetalArchives.search_query(band_name=band_name, **kwargs)
        search_url = MetalArchives.SEARCH + '?' + query_str

        while True:
            response = MetalArchives.get_page(search_url, user_agent=user_agent)
            status_code = response.status

            if status_code == 520:
                time.sleep(30)
                continue

            elif status_code == 429:
                time.sleep(10)
                continue

            elif status_code != 200:
                raise BandError(status_code, search_url)
            
            break

        return SearchResults(search_url, response.data)
    
    @staticmethod
    def get_profile(profile_url: str, user_agent: str | None = None) -> BandProfile:
        while True:
            response = MetalArchives.get_page(profile_url, user_agent=user_agent)
            status_code = response.status

            if status_code == 520:
                time.sleep(30)
                continue

            elif status_code == 429:
                time.sleep(10)
                continue

            elif status_code != 200:
                raise BandError(status_code, profile_url)
            
            break

        return BandProfile(profile_url, response.data)
    
    @staticmethod
    def get_profile_links(metallum_id: int, user_agent: str | None = None) -> BandExternalLinks:
        links_url = MetalArchives.links_query(metallum_id)
        while True:
            response = MetalArchives.get_page(links_url, user_agent=user_agent)
            status_code = response.status

            if status_code == 520:
                time.sleep(30)
                continue

            elif status_code == 429:
                time.sleep(10)
                continue

            elif status_code != 200:
                raise BandError(status_code, links_url)
            
            break

        return BandExternalLinks(metallum_id, response.data)
    
    @staticmethod
    def _get_profiles_thread(profile_url: str, verbose=False) -> tuple[BandProfile | None, str]:
        console = Console()

        while True:
            response = MetalArchives.get_page(profile_url)
            status_code = response.status

            if verbose:
                relative_url = profile_url.replace(MetalArchives.ROOT, '')
                console.log((f'GET {relative_url}'))

            if status_code == 520:
                time.sleep(30)
                continue

            elif status_code == 429:
                time.sleep(10)
                continue

            elif status_code != 200:
                raise BandError(status_code, profile_url)
            
            break

        return BandProfile(profile_url, response.data), profile_url

    @staticmethod
    def _get_links_thread(metallum_id: int, verbose=False) -> tuple[BandExternalLinks | None, str]:
        links_url = MetalArchives.links_query(metallum_id)
        
        console = Console()

        while True:
            response = MetalArchives.get_page(links_url)
            status_code = response.status

            if verbose:
                relative_url = links_url.replace(MetalArchives.ROOT, '')
                console.log((f'GET {relative_url}'))

            if status_code == 520:
                time.sleep(30)
                continue

            elif status_code == 429:
                time.sleep(10)
                continue

            elif status_code != 200:
                raise BandError(status_code, links_url)

            break

        return BandExternalLinks(metallum_id, response.data), links_url

    @classmethod
    def get_profiles(cls, profile_urls: list[str], segment_size=8, depth=0, 
                     max_depth=3, wait=3, verbose=False) -> list[BandProfile]:

        profile_urls_len = len(profile_urls)
        profiles = list()
        
        if profile_urls_len == 0:
            return profiles

        console = Console()
        profile_urls_swap = list()
        
        if verbose:
            console.log(f'Executing wave {depth} | {profile_urls_len} profiles')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            processed_urls = set()

            # don't throw them all in at once
            for segment_start in range(0, profile_urls_len + segment_size, segment_size):
                segment_end = min(segment_start + segment_size, profile_urls_len)

                band_futures = list()
                for url in profile_urls[segment_start:segment_end]:
                    if url not in processed_urls:
                        future = executor.submit(cls._get_profiles_thread, url, verbose=verbose)
                        band_futures.append(future)
                        processed_urls.add(url)
                        time.sleep(wait)

                # examine the remains
                for future in concurrent.futures.as_completed(band_futures):
                    profile, profile_url = future.result()
                    if profile is None:
                        profile_urls_swap.append(profile_url)
                    else:
                        profiles.append(profile)

        # if there's any left, throw them back into the pit
        if len(profile_urls_swap) > 0 and max_depth > depth:
            if verbose:
                console.log((f'Wave {depth} completed with errors'))

            profiles += cls.get_profiles(profile_urls_swap, segment_size=segment_size,
                                         depth=depth + 1, max_depth=max_depth)
        
        return profiles
    
    @classmethod
    def get_profiles_links(cls, metallum_ids: list[int], segment_size=8, 
                           depth=0, max_depth=3, verbose=False, wait=3) -> list[BandExternalLinks]:

        links = list()
        metallum_ids_count = len(metallum_ids)

        if metallum_ids_count == 0:
            return links

        console = Console()
        link_url_swap = list()
        
        if verbose:
            console.log(f'Executing wave {depth} | {metallum_ids_count} link pages')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            processed_urls = set()

            # don't throw them all in at once
            for segment_start in range(0, metallum_ids_count + segment_size, segment_size):
                segment_end = min(segment_start + segment_size, metallum_ids_count)

                band_futures = list()
                for url in metallum_ids[segment_start:segment_end]:
                    if url not in processed_urls:
                        future = executor.submit(cls._get_links_thread, url, verbose=verbose)
                        band_futures.append(future)
                        processed_urls.add(url)
                        time.sleep(wait)

                # examine the remains
                for future in concurrent.futures.as_completed(band_futures):
                    profile, profile_url = future.result()
                    if profile is None:
                        link_url_swap.append(profile_url)
                    else:
                        links.append(profile)

        # if there's any left, throw them back into the pit
        if len(link_url_swap) > 0 and max_depth > depth:
            if verbose:
                console.log((f'Wave {depth} completed with errors'))

            links += cls.get_profiles(link_url_swap, segment_size=segment_size,
                                      depth=depth + 1, max_depth=max_depth)
        
        return links
