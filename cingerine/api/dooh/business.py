import uuid

from cingerine.database import db
from cingerine.database.models import Player, PlayoutPlan
import logging


log = logging.getLogger(__name__)


def create_player(data):
    player = Player(**data)
    db.session.add(player)
    db.session.commit()
    log.info(f"Saved {player}")


def create_playout(data):
    playout = PlayoutPlan(**data)
    if playout.playoutId is None:
        playout.playoutId = str(uuid.uuid4())
    db.session.add(playout)
    db.session.commit()
    log.info(f"Saved Playout Plan with id {playout.playoutId}")
    return playout.playoutId
