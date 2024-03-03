import starfish.engine as sdk
from datetime import datetime, timedelta
import time
from decimal import Decimal
import pandas as pd
import numpy as np
import talib as ta
from typing import Dict

G_PARAMS = {}

Cashs = Dict[str, sdk.Cash]
Orders = Dict[int, sdk.Order]
