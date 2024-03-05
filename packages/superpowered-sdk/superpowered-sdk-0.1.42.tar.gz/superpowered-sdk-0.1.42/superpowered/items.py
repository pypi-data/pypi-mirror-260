from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

from . import superpowered


def create_item(knowledge_base_id: str, content: str, metadata: dict, supp_id: str = None, link_to_source: str = None):
    """
    Create an item in a semi-structured knowledge base.

    Args:
        knowledge_base_id (str): The ID of the knowledge base.
        content (str): The content of the item.
        metadata (dict): The metadata of the item. Metadata is used for LLM-based filtering. Be sure your metadata schema is set up in the knowledge base.
        supp_id (str, optional): A supplemental ID for the item for internal use. Defaults to None.
        link_to_source (str, optional): A link to the source of the item. Defaults to None.

    Returns:
        dict: The item object.

    References:
        ``POST /knowledge_bases/{knowledge_base_id}/items``
    """
    data = {
        'content': content,
        'metadata': metadata,
    }
    if supp_id:
        data['supp_id'] = supp_id
    if link_to_source:
        data['link_to_source'] = link_to_source
    args = {
        'method': 'POST',
        'url': f'{superpowered.get_base_url()}/knowledge_bases/{knowledge_base_id}/items',
        'json': data,
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def _call_create_item(args: dict) -> dict:
    """
    Call create_item().

    Args:
        args (dict): The arguments for create_item().

    Returns:
        dict: The item object.
    """
    return create_item(**args)


def batch_create_items(knowledge_base_id: str, items: list[dict], batch_size: int = 25, verbose: bool = True) -> dict:
    """
    Create multiple items in a semi-structured knowledge base.

    NOTE: This function uses ``concurrent.futures.ProcessPoolExecutor`` to parallelize the API calls. You must call this function from within a ``if __name__ == '__main__':`` block or from within a function, otherwise you will see many errors in a loop.

    Args:
        knowledge_base_id (str): The ID of the knowledge base.
        items (list[dict]): The list of items to create. Each dictionary should have the following keys: ``content`` (required), ``metadata`` (required), ``supp_id`` (optional), ``link_to_source`` (optional).
        batch_size (int, optional): The batch size. Defaults to 25. Range: [1, 50].
        verbose (bool, optional): Whether to show a progress bar. Defaults to True.

    Returns:
        dict: The list of item objects.

    """
    batch_size = max(min(batch_size, 50), 1)

    # create args list for async_upload_item
    args = [{**{'knowledge_base_id': knowledge_base_id}, **item} for item in items]

    with ProcessPoolExecutor(max_workers=batch_size) as executor:
        if verbose:
            results = list(tqdm(executor.map(_call_create_item, args), total=len(args)))
        else:
            results = list(executor.map(create_item, args))

    return results


def list_items(knowledge_base_id: str, limit: int = None, next_page_token: str = None, supp_id: str = None) -> dict:
    """
    List items in a knowledge base.

    Args:
        knowledge_base_id (str): The ID of the knowledge base.
        limit (int, optional): The maximum number of items to return. Defaults to 25.
        next_page_token (str, optional): The next page token. Defaults to None.
        supp_id (str, optional): The supplemental ID of the item. Defaults to None.

    Returns:
        dict:
            items (list[dict]): The list of items.
            next_page_token (str): The next page token.

    References:
        ``GET /knowledge_bases/{knowledge_base_id}/items``
    """
    params = {
        'limit': limit,
    }
    if next_page_token:
        params['next_page_token'] = next_page_token
    if supp_id:
        params['supp_id'] = supp_id
    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/knowledge_bases/{knowledge_base_id}/items',
        'params': params,
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def get_item(knowledge_base_id: str, item_id: str):
    """
    Get an item in a knowledge base.

    Args:
        knowledge_base_id (str): The ID of the knowledge base.
        item_id (str): The ID of the item.

    Returns:
        dict: The item object.

    References:
        ``GET /knowledge_bases/{knowledge_base_id}/items/{item_id}``
    """
    args = {
        'method': 'GET',
        'url': f'{superpowered.get_base_url()}/knowledge_bases/{knowledge_base_id}/items/{item_id}',
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)


def delete_item(knowledge_base_id: str, item_id: str):
    """
    Delete an item in a knowledge base.

    Args:
        knowledge_base_id (str): The ID of the knowledge base.
        item_id (str): The ID of the item.

    Returns:
        bool: True if the item was deleted successfully, False otherwise.

    References:
        ``DELETE /knowledge_bases/{knowledge_base_id}/items/{item_id}``
    """
    args = {
        'method': 'DELETE',
        'url': f'{superpowered.get_base_url()}/knowledge_bases/{knowledge_base_id}/items/{item_id}',
        'auth': superpowered.auth(),
    }
    return superpowered.make_api_call(args)
