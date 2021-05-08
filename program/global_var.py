# All paths
TWITCH_PATH = "assets/twitch/"
OUTPUT_DIR = "output/"
OUTPUT_LOG_PATH = f"{OUTPUT_DIR}log/log.txt"
COUNTRY_CODES = ["ES", "RU"]
# COUNTRY_CODES = ["DE", "ENGB", "ES", "FR", "PTBR", "RU"]
TARGET_INPUTS = [f"{code}/musae_{code}_edges.csv" for code in COUNTRY_CODES]
ALL_OUTPUT_DIR = [
    OUTPUT_DIR,
    f"{OUTPUT_DIR}log",
    f"{OUTPUT_DIR}/SIR",
    f"{OUTPUT_DIR}/SIR/log",
    f"{OUTPUT_DIR}/SIR/graph",
    f"{OUTPUT_DIR}/SIS",
    f"{OUTPUT_DIR}/SIS/log",
    f"{OUTPUT_DIR}/SIS/graph",
    f"{OUTPUT_DIR}/SIRS",
    f"{OUTPUT_DIR}/SIRS/log",
    f"{OUTPUT_DIR}/SIRS/graph"
]
ALL_OUTPUT_DIR += [
    f"{OUTPUT_DIR}/SIR/log/{country_code}/" for country_code in COUNTRY_CODES]
ALL_OUTPUT_DIR += [
    f"{OUTPUT_DIR}/SIS/log/{country_code}/" for country_code in COUNTRY_CODES]
ALL_OUTPUT_DIR += [
    f"{OUTPUT_DIR}/SIRS/log/{country_code}/" for country_code in COUNTRY_CODES]

# COUNTRY_CODES = ["TS"]
# TARGET_INPUTS = ["test_input_edges.csv"]
