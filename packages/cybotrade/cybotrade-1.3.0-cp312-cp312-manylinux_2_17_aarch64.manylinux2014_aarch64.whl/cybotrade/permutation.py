import asyncio
from datetime import datetime
from itertools import product
from typing import Any, Dict, List
import json

from .strategy import Strategy
from .models import Performance, RuntimeConfig, RuntimeMode 
from .runtime import Runtime

class BacktestPerformance:
    def __init__(self, config: RuntimeConfig):
        self.candle_topics = config.candle_topics

        if config.initial_capital == None:
            self.initial_capital = 10_000
        else:
            self.initial_capital = config.initial_capital 

        self.trades = {}

        if config.start_time != None:
            self.start_time = int(config.start_time.timestamp()) * 1000

        if config.end_time != None:
            self.end_time = int(config.end_time.timestamp()) * 1000

        self.version = "1.2.0"


    def set_trade_result(self, id: str, perf: Performance):
        self.trades[id] = perf

    def generate_json(self):
        perf_json = json.dumps(self.__dict__, default=str)
        date = datetime.now().date()
        date = ''.join(str(date).split('-'))
        time = datetime.now().timestamp()
        time = ''.join(str(time).split('.')[0].split(':'))

        file = open(f"performance-{date}{time}.json", "w")
        file.write(perf_json)

class Permutation:
    results = []

    def __init__(self, config: RuntimeConfig):
        self.config = config
    
    async def run(self, strategy_params: Dict[str, List[Any]], strategy):
        result = BacktestPerformance(self.config)

        keys = list(strategy_params.keys())
        permutations = list(product(*(strategy_params[key] for key in keys)))
        coro_list = []

        if len(permutations) is 0:
            coro_list.append(self.process_permutations([], [], strategy))
        else:
            for perm in permutations:
                coro_list.append(self.process_permutations(keys, perm, strategy))

        await asyncio.gather(*coro_list)

        for id, perf in self.results:
            result.set_trade_result(id, perf)

        result.generate_json()
            
    async def process_permutations(self, keys: List[str], perm, strategy_class):
        runtime = Runtime.__new__(Runtime)
        strategy = strategy_class()
        await runtime.connect(self.config, strategy)
        permutation_key = []

        for i in range(len(keys)):
            await runtime.set_param(keys[i], str(perm[i]))
            permutation_key.append(f"{keys[i]}={perm[i]}")

        result = await runtime.start()
        self.results.append([",".join(permutation_key), result])
