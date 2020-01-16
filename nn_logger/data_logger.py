"""
Acessing google app

Copyright 2020 Denis Brailovsky, denis.brailovsky@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import json
import os
from datetime import datetime
from os.path import expanduser

create_folder = lambda pth: pth if os.path.exists(pth) else pth if os.makedirs(pth) is None else False
current_timestamp = lambda: datetime.now().strftime("%y%m%d_%H%M")

EXAMPLE_QUERY = {
    "query": {"ID": 0, "Date": None, "Run_Date": None, "Epoch": 1, "Loss": 0.5},
    "actions": {
        "Date": {"action": "timestamp"},
        "Run_Date": {"action": "run_timestamp"},
    }
}

DEFAULT_CONFIG = {
    "experiment_name": "testing",
    "visualise_path": "~/.nn_log/{experiment_name}/{experiment_num}/visualization",
    "save_path": "~/.nn_log/{experiment_name}/{experiment_num}/data",
    "titles": ["ID", "Date", "Run_Date", "Epoch", "Loss"]
}


class LogQuery(object):
    def __init__(self, titles, run_timestamp=None):
        self.run_timestamp = run_timestamp
        if run_timestamp is None:
            self.run_timestamp = current_timestamp()
        self.actions = {
            "timestamp": current_timestamp,
            "run_timestamp": self.get_run_timestamp
        }
        self.titles = titles
        self.__empty_field = "<empty>"

    def get_run_timestamp(self):
        return self.run_timestamp

    def new(self, query,  titles=None):
        insert_query, actions = query["query"], {}
        if "actions" in query.keys():
            actions = query["actions"]
        if titles is None:
            titles = self.titles

        inserters = []
        insert_data = []

        for k in titles:
            if k not in insert_query.keys():
                inserters.append(None)
                insert_data.append(None)
            else:
                insert_data.append(insert_query[k])
                action = {"action": None}
                if k in actions.keys():
                    action = actions[k]
                if action["action"] is None:
                    inserters.append(None)
                else:
                    inserters.append(action)
        assert len(inserters) == len(insert_data)
        query = []
        for inserter, data in zip(inserters, insert_data):
            _data = data
            if inserter is not None:
                vargs = []
                kargs = {}
                if data is not None:
                    vargs.append(data)
                if "args" in inserter.keys() and inserter["args"] is not None:
                    if type(inserter["args"]) == dict:
                        kargs = inserter["args"]
                    elif type(inserter["args"]) == list:
                        vargs += inserter["args"]
                _data = self.actions[inserter["action"]](*vargs, **kargs)
            query.append(_data)
        print(query)
        return self.__qvalues(query)

    def __qvalues(self, query):
        query = [str(q) if q is not None else self.__empty_field for q in query]
        return query


class DataLogging(object):
    def __init__(self, config=None, experiment_name=None, run_time=None):
        self.run_time = run_time
        if config is not None:
            if type(config) == str:
                with open(config, 'r') as f:
                    config = json.load(f)
            else:
                pass
        else:
            config = DEFAULT_CONFIG
        if experiment_name is not None:
            config["experiment_name"] = experiment_name
        if run_time is None:
            self.run_time = current_timestamp()
        self.experiment_name = config["experiment_name"]
        self.visualize_folder = create_folder(
            expanduser(config["visualise_path"].format(experiment_name=self.experiment_name,
                                                       experiment_num=self.run_time)))
        self.save_data_folder = create_folder(
            expanduser(config["save_path"].format(experiment_name=self.experiment_name,
                                                  experiment_num=self.run_time)))
        self.table = os.path.join(self.save_data_folder, "log.csv")
        self.titles = config["titles"]

    def visualize(self, images, title):
        pass

    def add(self, query):
        print(query)
        with open(self.table, 'a') as f:
            f.write(",".join(query) + "\n")


