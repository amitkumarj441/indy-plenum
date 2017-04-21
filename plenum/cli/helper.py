from plenum.cli.constants import UTIL_GRAMS_SIMPLE_CMD_FORMATTED_REG_EX, \
    UTIL_GRAMS_COMMAND_HELP_FORMATTED_REG_EX, \
    NODE_GRAMS_NODE_COMMAND_FORMATTED_REG_EX, \
    CLIENT_GRAMS_CLIENT_COMMAND_FORMATTED_REG_EX, \
    CLIENT_GRAMS_CLIENT_SEND_FORMATTED_REG_EX, \
    CLIENT_GRAMS_CLIENT_SHOW_FORMATTED_REG_EX, \
    CLIENT_GRAMS_ADD_KEY_FORMATTED_REG_EX, \
    CLIENT_GRAMS_NEW_KEYPAIR_FORMATTED_REG_EX, \
    CLIENT_GRAMS_LIST_IDS_FORMATTED_REG_EX, \
    CLIENT_GRAMS_BECOME_FORMATTED_REG_EX, \
    CLIENT_GRAMS_USE_KEYPAIR_FORMATTED_REG_EX, \
    UTIL_GRAMS_COMMAND_LIST_FORMATTED_REG_EX, \
    NODE_GRAMS_LOAD_PLUGINS_FORMATTED_REG_EX, \
    CLIENT_GRAMS_ADD_GENESIS_TXN_FORMATTED_REG_EX, \
    CLIENT_GRAMS_CREATE_GENESIS_TXN_FILE_FORMATTED_REG_EX, \
    UTIL_GRAMS_COMMAND_PROMPT_FORMATTED_REG_EX, \
    CLIENT_GRAMS_NEW_KEYRING_FORMATTED_REG_EX, \
    CLIENT_GRAMS_RENAME_KEYRING_FORMATTED_REG_EX, \
    CLIENT_GRAMS_USE_KEYRING_FORMATTED_REG_EX, \
    CLIENT_GRAMS_SAVE_KEYRING_FORMATTED_REG_EX, \
    CLIENT_GRAMS_LIST_KEYRINGS_FORMATTED_REG_EX
from stp_core.common.log import getlogger

logger = getlogger()


def getUtilGrams():
    return [
        UTIL_GRAMS_SIMPLE_CMD_FORMATTED_REG_EX,
        UTIL_GRAMS_COMMAND_HELP_FORMATTED_REG_EX,
        UTIL_GRAMS_COMMAND_PROMPT_FORMATTED_REG_EX,
        UTIL_GRAMS_COMMAND_LIST_FORMATTED_REG_EX
    ]


def getNodeGrams():
    return [
        NODE_GRAMS_NODE_COMMAND_FORMATTED_REG_EX,
        NODE_GRAMS_LOAD_PLUGINS_FORMATTED_REG_EX,
    ]


def getClientGrams():
    return [
        CLIENT_GRAMS_CLIENT_COMMAND_FORMATTED_REG_EX,
        CLIENT_GRAMS_CLIENT_SEND_FORMATTED_REG_EX,
        CLIENT_GRAMS_CLIENT_SHOW_FORMATTED_REG_EX,
        CLIENT_GRAMS_ADD_KEY_FORMATTED_REG_EX,
        CLIENT_GRAMS_NEW_KEYPAIR_FORMATTED_REG_EX,
        CLIENT_GRAMS_NEW_KEYRING_FORMATTED_REG_EX,
        CLIENT_GRAMS_RENAME_KEYRING_FORMATTED_REG_EX,
        CLIENT_GRAMS_LIST_IDS_FORMATTED_REG_EX,
        CLIENT_GRAMS_LIST_KEYRINGS_FORMATTED_REG_EX,
        CLIENT_GRAMS_BECOME_FORMATTED_REG_EX,
        CLIENT_GRAMS_ADD_GENESIS_TXN_FORMATTED_REG_EX,
        CLIENT_GRAMS_CREATE_GENESIS_TXN_FILE_FORMATTED_REG_EX,
        CLIENT_GRAMS_USE_KEYPAIR_FORMATTED_REG_EX,
        CLIENT_GRAMS_USE_KEYRING_FORMATTED_REG_EX,
        CLIENT_GRAMS_SAVE_KEYRING_FORMATTED_REG_EX
    ]


def getAllGrams(*grams):
    # Adding "|" to `utilGrams` and `nodeGrams` so they can be combined
    allGrams = []
    for gram in grams[:-1]:
        allGrams += gram
        allGrams[-1] += " |"
    return allGrams + grams[-1]
