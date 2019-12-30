# -*- coding: utf-8 -*-
# Copyright (c) 2019 BuildGroup Data Services Inc.
import copy
import logging
import random

from davinci_crawling.net import get_json
from davinci_crawling.proxy.proxy import Proxy
from django.conf import settings

AUTHORIZED_PROXIES_URL = "https://proxymesh.com/api/proxies/"

PROXY_TEMPLATE = "%s:%s@%s"

_logger = logging.getLogger("davinci_crawling")


def get_proxy_mesh_settings():
    if hasattr(settings, 'DAVINCI_CONF') and \
            "proxy" in settings.DAVINCI_CONF["architecture-params"] \
            and "proxy_mesh" in settings.DAVINCI_CONF["architecture-params"][
                "proxy"]:
        return settings.DAVINCI_CONF[
            "architecture-params"]["proxy"]["proxy_mesh"]
    else:
        return None


PROXY_MESH_SETTINGS = get_proxy_mesh_settings()


class ProxyMesh(Proxy):

    available_proxies = None
    to_use_proxies = None

    def get_to_use_proxies(self):
        if not self.to_use_proxies:
            self.to_use_proxies = self.get_available_proxies()

        return self.to_use_proxies

    def set_to_use_proxies(self, proxies):
        self.to_use_proxies = proxies

    @classmethod
    def get_available_proxies(cls):
        """
        Proxy Mesh has a list of proxies to use, this method will acess proxy
        mesh api to get this list of ips.
        Returns:

        """
        if not cls.available_proxies and PROXY_MESH_SETTINGS:
            custom_header = {
                "authorization": PROXY_MESH_SETTINGS["authentication"]
            }
            response = get_json(PROXY_MESH_SETTINGS["authorized_proxies_url"],
                                custom_header=custom_header, use_proxy=False)
            response = response.json()
            proxies = []

            for proxy in response["proxies"]:
                _proxy = PROXY_TEMPLATE % (settings.PROXY_MESH_USER,
                                           settings.PROXY_MESH_PASSWORD,
                                           proxy)
                _proxy = {
                    'http': 'http://' + _proxy,
                    'https': 'https://' + _proxy,
                    'no_proxy': 'localhost,127.0.0.1'   # excludes
                }
                proxies.append(_proxy)
            cls.available_proxies = proxies

        return cls.available_proxies

    def get_proxy_address(self):
        """
        Just get the list of available proxies and random select a proxy.
        """
        proxies = self.get_to_use_proxies()

        if not proxies:
            return None

        quality_proxy_quantities = max(6, int(len(proxies) * 0.5))
        quality_proxy_quantities = min(quality_proxy_quantities, len(proxies))

        proxy = random.choice(proxies[0:quality_proxy_quantities])
        _logger.debug("Using %s proxy", proxy["http"].split("@")[1])
        return copy.deepcopy(proxy)