# -*- coding: utf-8 -*-
"""Utils for handling the url in the crawler."""

from settings import FILTERS


def append_filters_to_url(url, crawler_config, filters):
    """Replace the active config filters in the url.

    :param url: String, craler url
    :param filters: Dict filter values
    """
    if not filters or not crawler_config:
        return url

    for filer_available in FILTERS:
        if filer_available in filters:
            filter_base = getattr(
                crawler_config, "filter_{0}".format(filer_available))
            if filter_base:
                filter_dict = {filer_available: filters[filer_available]}
                filter_value = filter_base.format(**filter_dict)
                url += "&{0}".format(filter_value)
    return url


def get_filters_from_request(request):
    """Get the filter parameters from the request.

    :param request: request object
    :return: Dict
    """
    dict_data = {}
    keys = request.args.keys()
    for key in keys:
        value = request.args.get(key)
        decoded_value = value[0].decode('UTF-8')
        decoded_key = key.decode('UTF-8')
        dict_data[decoded_key] = decoded_value
    return dict_data
