import json

from pathlib import Path

import logging

logger = logging.getLogger(__name__)


def make_metadata(challenges, metadata_file: Path, args):
    output = [challenge.serialize(args) for challenge in challenges]

    with metadata_file.open("w") as f:
        json.dump(output, f)

    logger.debug("Saved metadata")
