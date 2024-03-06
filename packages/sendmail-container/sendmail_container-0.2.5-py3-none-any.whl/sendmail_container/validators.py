from typing import List, Union


def split_recipients(recipients: Union[List, str]) -> List[str]:
    if isinstance(recipients, str):
        return recipients.split(",")
    return recipients
