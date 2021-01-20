
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import requests
import re
import pandas as pd
import sys

from StrategyStackOverflow import StrategyStackOverflow
from Scrapper import Scrapper

class Context():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: Scrapper) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> Scrapper:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Scrapper) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def beginScrappng(self) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        pageNo = self._strategy.PAGES

        for n in range(1, pageNo):
            complete_page_data = self._strategy.jobs_page(n)
            jobs_data = self._strategy.process_page_data(complete_page_data)
            print(jobs_data)
            self._strategy.saveResults(jobs_data)

##Main Begins
if __name__ == '__main__':
    strategies = [StrategyStackOverflow]

    for strategy in strategies:
        context = Context(strategy())
        context.beginScrappng()

