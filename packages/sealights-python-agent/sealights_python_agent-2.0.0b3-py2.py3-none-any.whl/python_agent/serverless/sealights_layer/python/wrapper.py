import importlib
import json
import os
import re
import sys
import time
from typing import List

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent'))
import coverage
from agent.agent_config import AgentConfig
from agent.footprints import FootprintModel
from agent.logging import debug, error, info, warn

PYTHON_FILES_REG = r"^[^.#~!$@%^&*()+=,]+\.pyw?$"

cov = coverage.Coverage(data_file='/tmp/.coverage')

orig_lambda_handler = os.environ.get('ORIG_NAME', '')
orig_module_name, orig_function_name = orig_lambda_handler.rsplit('.', 1)
orig_module = importlib.import_module(orig_module_name)
orig_function = getattr(orig_module, orig_function_name)


def lambda_handler(event, context):
    debug("Debug mode is on")
    is_sealights_ready = False
    agent_config: AgentConfig = {}
    build_digest: dict[str, dict[int, str]] = {}
    proxy_url = os.environ.get('SL_PROXY', '')
    token = os.environ.get('SL_TOKEN', '')
    try:
        config_data = config_loader()
        build_digest = load_build_digest_from_json(config_data)
        token = config_data.get('token', token)
        agent_config = AgentConfig(config_data)
        agent_config.validate()
        debug("Starting Sealights Coverage")
        cov.start()
        is_sealights_ready = True
        info("Starting Sealights lambda wrapper handler")
    except Exception as e:
        error(e)
        warn("Sealights coverage is disabled")
        is_sealights_ready = False
    start_time = int(time.time())
    debug("Original lambda function starting")
    lambda_response = orig_function(event, context)
    debug("Original lambda function returned")
    end_time = int(time.time())
    if is_sealights_ready:
        debug("Stopping Sealights Coverage")
        cov.stop()
        info("Getting Sealights Footprints")
        footprints = get_footprints_from_coverage(cov.get_data(), build_digest)
        footprints_length = len(footprints)
        if footprints_length == 0:
            warn("No footprints found, skipping Sealights Footprints report")
            return lambda_response
        else:
            info(f"Found {footprints_length} footprints")
        debug("Creating Sealights Footprint Model")
        fm = FootprintModel(
            agent_config=agent_config,
            methods=footprints,
            start_time=start_time,
            end_time=end_time
        )
        info("Posting Sealights Footprints started")
        fm.send_collector(agent_config, proxy_url, token)
        info("Posting Sealights Footprints completed")
        cov.erase()
        info("Finished Sealights lambda wrapper handler")
    return lambda_response


def config_loader():
    debug("Loading Sealights Configuration")
    file_path = './sl_lambda_config.json'
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f'Failed to load config from {file_path}: {e}')
    return data


def get_top_relative_path(filepath):
    return os.path.relpath(filepath, os.getcwd()).replace("\\", "/")


def load_build_digest_from_json(data) -> dict[str, dict[int, str]]:
    debug("Loading Sealights Build Digest")
    try:
        build_digest = data.get('buildDigest', {})
        file_lines_methods: dict[str, dict[int, str]] = {}
        for file_path, methods in build_digest.items():
            lines_methods: dict[int, str] = {}
            for method, lines in methods.items():
                debug(f'File: {file_path} Method: {method} Line: {lines} to file {file_path}')
                for line in lines:
                    lines_methods[line] = method
            file_lines_methods[file_path] = lines_methods
    except Exception as e:
        raise ValueError(f'Failed to load build digest from json: {e}')
    if not file_lines_methods:
        raise ValueError(
            'No build digest found in json, re-run sl-python configlambda command to generate a new build digest.')
    return file_lines_methods


def get_footprints_from_coverage(coverage_data: coverage.CoverageData, build_digest: dict[str, dict[int, str]]) -> dict[
    str, List[int]]:
    footprints = {}
    for filename in coverage_data.measured_files():
        if not re.match(PYTHON_FILES_REG, os.path.split(filename)[1]):
            continue
        relative_path = get_top_relative_path(filename).replace("\\", "/")
        file_digest: dict[int, str] = build_digest.get(relative_path)
        if not file_digest:
            debug(f'File {relative_path} not found in build digest, skipping')
            continue
        covered_lines = coverage_data.lines(filename)
        for line in covered_lines:
            unique_id = file_digest.get(int(line))
            if unique_id:
                if unique_id not in footprints:
                    footprints[unique_id] = [line]
                else:
                    footprints[unique_id].append(line)
            else:
                warn(
                    f'Line {line} in file {relative_path} was covered but not found in build digest thus will not be reported, re-run sl-python configlambda command to generate a new build digest.')
    return footprints
