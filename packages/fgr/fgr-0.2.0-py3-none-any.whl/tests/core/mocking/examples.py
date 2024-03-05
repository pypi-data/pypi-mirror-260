import fgr


class Pet(fgr.Object):
    """A pet."""

    id_: fgr.Field[str]
    _alternate_id: fgr.Field[str]

    name: fgr.Field[str]
    type: fgr.Field[str]
    in_: fgr.Field[str]
    is_tail_wagging: fgr.Field[bool] = True
