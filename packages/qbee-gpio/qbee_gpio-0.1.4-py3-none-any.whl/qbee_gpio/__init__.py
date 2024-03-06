import asyncio
import sys

from qbee_gpio.config import QbeeConfig
from qbee_gpio.gpio import gpio_setup
from qbee_gpio.orchestrator import QbeeOrchestrator


def run() -> None:
    if "--init-config" in sys.argv:
        QbeeConfig.load().save()
        return
    with gpio_setup():
        asyncio.run(QbeeOrchestrator(debug="-v" in sys.argv).run())
