"""
Copyright © 2015-2018 Constverum <constverum@gmail.com>. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__title__ = 'ProxyBrokerSPS'
__package__ = 'proxybrokersps'
__version__ = '0.0.2'
__short_description__ = '[Finder/Checker/Server] Finds public proxies from multiple sources and concurrently checks them. Supports HTTP(S) and SOCKS4/5.'  # noqa
__author__ = 'Aa-ronT'
__author_email__ = 'aarontrading2@gmail.com'
__url__ = 'https://github.com/Aa-ronT/ProxyBrokerSPS'
__license__ = 'Apache License, Version 2.0'


from .proxy import Proxy  # noqa
from .judge import Judge  # noqa
from .providers import Provider  # noqa
from .checker import Checker  # noqa
from .server import Server, ProxyPool  # noqa
from .api import Broker  # noqa

import asyncio
import logging  # noqa
import warnings  # noqa
import sys

logger = logging.getLogger('asyncio')
logger.addFilter(logging.Filter('has no effect when using ssl'))

warnings.simplefilter('always', UserWarning)
warnings.simplefilter('once', DeprecationWarning)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

__all__ = (Proxy, Judge, Provider, Checker, Server, ProxyPool, Broker)
