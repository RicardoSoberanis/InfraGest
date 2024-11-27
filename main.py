
#!/usr/bin/env python3
import os
import pydgraph

import logging

from fastapi import FastAPI
from pymongo import MongoClient


import model_dgraph
import model_cassandra
import model_mongo


