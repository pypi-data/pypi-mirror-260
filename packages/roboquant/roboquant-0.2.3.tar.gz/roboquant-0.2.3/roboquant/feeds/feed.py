import threading
from abc import ABC, abstractmethod

from roboquant.feeds.eventchannel import EventChannel, ChannelClosed
from roboquant.timeframe import Timeframe


class Feed(ABC):
    """A feed (re-)plays events"""

    @abstractmethod
    def play(self, channel: EventChannel):
        """(re-)play the events in the feed and put them on the provided event channel"""
        ...

    def play_background(self, timeframe: Timeframe | None = None, channel_capacity: int = 10) -> EventChannel:
        """Play this feed in the background on its own thread.
        The returned event-channel will be closed after the playing has finished.
        """
        channel = EventChannel(timeframe, channel_capacity)

        def __background():
            try:
                self.play(channel)
            except ChannelClosed:
                # this exception we can expect
                pass
            finally:
                channel.close()

        thread = threading.Thread(None, __background, daemon=True)
        thread.start()
        return channel

    def plot(self, plt, symbol: str, price_type: str = "DEFAULT", timeframe: Timeframe | None = None, **kwargs):
        """Plot the prices of one or more symbols"""
        channel = self.play_background(timeframe)
        times = []
        prices = []
        while evt := channel.get():
            price = evt.get_price(symbol, price_type)
            if price is not None:
                times.append(evt.time)
                prices.append(price)

        plt.plot(times, prices, **kwargs)
        if hasattr(plt, "set_title"):
            # assume we are in a subplot
            plt.set_title(symbol)
        else:
            plt.title(symbol)
