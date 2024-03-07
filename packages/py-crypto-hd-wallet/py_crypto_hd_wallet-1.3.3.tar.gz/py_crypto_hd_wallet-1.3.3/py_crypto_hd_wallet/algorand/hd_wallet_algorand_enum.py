# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Module with enums for Algorand wallets."""

# Imports
from enum import auto, unique

from bip_utils import AlgorandLanguages, AlgorandWordsNum

from py_crypto_hd_wallet.common import HdWalletDataTypes, HdWalletKeyTypes


# Alias for AlgorandWordsNum
HdWalletAlgorandWordsNum = AlgorandWordsNum
# Alias for AlgorandLanguages
HdWalletAlgorandLanguages = AlgorandLanguages


@unique
class HdWalletAlgorandDataTypes(HdWalletDataTypes):
    """Enumerative for wallet Algorand data types."""

    WALLET_NAME = auto()
    COIN_NAME = auto()
    MNEMONIC = auto()
    SEED_BYTES = auto()
    KEY = auto()


@unique
class HdWalletAlgorandKeyTypes(HdWalletKeyTypes):
    """Enumerative for wallet Algorand key types."""

    PRIV = auto()
    PUB = auto()
    ADDRESS = auto()
