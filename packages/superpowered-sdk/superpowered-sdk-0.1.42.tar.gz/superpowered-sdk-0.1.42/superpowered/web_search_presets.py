
from . import superpowered


def create_web_search_preset(title: str, description: str = None, supp_id: str = None, include_domains: list[str] = None, exclude_domains: list[str] = None, start_date: str = None, end_date: str = None, timeframe_days: int = None) -> dict:
    """
    Create a web search preset.

    Args:
        title (str): The title of the web search preset.
        description (str, optional): The description of the web search preset. Defaults to None.
        supp_id (str, optional): A supplemental ID for the web search preset for internal use. Defaults to None.
        include_domains (list[str], optional): A list of domains to include in the search. Defaults to [].
        exclude_domains (list[str], optional): A list of domains to exclude from the search. Defaults to [].
        start_date (str, optional): The start date of the search. If ``timeframe_days`` is provided, this will be ignored. Defaults to None.
        end_date (str, optional): The end date of the search. If ``timeframe_days`` is provided, this will be ignored. Defaults to None.
        timeframe_days (int, optional): The previous N days to search over. For example, if ``timeframe_days`` is 7, the search will be for the last 7 days. Defaults to None.

    Returns:
        dict: The web search preset object.

    Note:
        The ``title`` and ``description`` fields are important for "Auto Query", which is used to automatically generate search queries for particular web search presets based on the user's input.

    References:
        ``POST /web_search_presets``
    """
    data = {
        'title': title,
    }
    if description:
        data['description'] = description
    if supp_id:
        data['supp_id'] = supp_id
    if include_domains:
        data['include_domains'] = include_domains
    if exclude_domains:
        data['exclude_domains'] = exclude_domains
    if start_date:
        data['start_date'] = start_date
    if end_date:
        data['end_date'] = end_date
    if timeframe_days:
        data['timeframe_days'] = timeframe_days

    args = {
        'method': 'POST',
        'url': f'{superpowered.get_base_url()}/web_search_presets',
        'json': data,
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def update_web_search_preset(web_search_preset_id: str, title: str = None, description: str = None, supp_id: str = None, include_domains: list[str] = None, exclude_domains: list[str] = None, start_date: str = None, end_date: str = None, timeframe_days: int = None) -> dict:
    """
    Update a web search preset object.

    Args:
        web_search_preset_id (str): The ID of the web search preset.
        title (str, optional): The title of the web search preset. Defaults to None.
        description (str, optional): The description of the web search preset. Defaults to None.
        supp_id (str, optional): The ID of the web search preset in your system. Defaults to None.
        include_domains (list[str], optional): A list of domains to include in the search. Defaults to [].
        exclude_domains (list[str], optional): A list of domains to exclude from the search. Defaults to [].
        start_date (str, optional): The start date of the search. If ``timeframe_days`` is provided, this will be ignored. Defaults to None.
        end_date (str, optional): The end date of the search. If ``timeframe_days`` is provided, this will be ignored. Defaults to None.
        timeframe_days (int, optional): The previous N days to search over. For example, if ``timeframe_days`` is 7, the search will be for the last 7 days. Defaults to None.

    Returns:
        dict: The web search preset object.

    References:
        ``PATCH /web_search_presets/{web_search_preset_id}``
    """
    data = {}
    if title:
        data['title'] = title
    if description:
        data['description'] = description
    if supp_id:
        data['supp_id'] = supp_id
    if include_domains:
        data['include_domains'] = include_domains
    if exclude_domains:
        data['exclude_domains'] = exclude_domains
    if start_date:
        data['start_date'] = start_date
    if end_date:
        data['end_date'] = end_date
    if timeframe_days:
        data['timeframe_days'] = timeframe_days
    
    args = {
        'method': 'PATCH',
        'url': f'{superpowered.get_base_url()}/web_search_presets/{web_search_preset_id}',
        'json': data,
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def list_web_search_presets(title: str = None, supp_id: str = None) -> list:
    """
    List all web search presets.

    Args:
        title (str, optional): The title of the web search preset. Defaults to None.
        supp_id (str, optional): The ID of the web search preset in your system. Defaults to None.

    Returns:
        list: A list of web search preset objects that match the filter criteria.

    Note:
        You can use ``title`` as a prefix to filter your search. For example, if you have a web search preset titled "FAQ", you can use ``title="F"`` to find it.

    References:
        ``GET /web_search_presets``
    """
    params = {}
    if title:
        params['title_begins_with'] = title
    if supp_id:
        params['supp_id'] = supp_id

    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/web_search_presets',
        'params': params,
        'auth': superpowered.auth(),
    }
    resp = superpowered.make_api_call(args)
    web_search_presets = resp.get('web_search_presets', [])

    while resp.get('next_page_token'):
        args['params']['next_page_token'] = resp['next_page_token']
        resp = superpowered.make_api_call(args)
        web_search_presets.extend(resp.get('web_search_presets', []))

    return web_search_presets


def get_web_search_preset(web_search_preset_id: str) -> dict:
    """
    Get an individual web search preset by it's ID.

    Args:
        web_search_preset_id (str): The ID of the web search preset.

    Returns:
        dict: The web search preset object.
    
    References:
       ``GET /web_search_presets/{web_search_preset_id}``
    """
    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/web_search_presets/{web_search_preset_id}',
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def delete_web_search_preset(web_search_preset_id: str) -> bool:
    """
    Delete a web search preset by it's ID.

    Args:
        web_search_preset_id (str): The ID of the web search preset.

    Returns:
        bool: True if the web search preset was deleted successfully, False otherwise.

    References:
        ``DELETE /web_search_presets/{web_search_preset_id}``
    """
    args = {
        'method': 'DELETE',
        'url': f'{superpowered.get_base_url()}/web_search_presets/{web_search_preset_id}',
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)
