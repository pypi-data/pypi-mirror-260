from githubapp.events.event import Event


class CreateEvent(Event):
    """This class represents a branch or tag creation event."""

    event_identifier = {"event": "create"}

    def __init__(
        self,
        description,
        master_branch,
        pusher_type,
        ref,
        ref_type,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.description: str = description
        self.master_branch: str = master_branch
        self.pusher_type: str = pusher_type
        self.ref: str = ref
        self.ref_type: str = ref_type


class CreateBranchEvent(CreateEvent):
    """This class represents a branch creation event."""

    event_identifier = {"ref_type": "branch"}


class CreateTagEvent(CreateEvent):
    """This class represents a tag creation event."""

    event_identifier = {"ref_type": "tag"}
