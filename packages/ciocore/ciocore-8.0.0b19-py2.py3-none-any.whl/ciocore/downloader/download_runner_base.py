"""
Base Download runner

This module contains the DownloadRunnerBase class. 

The DownloadRunnerBase is responsible for running one of the downloader classes: JobDownloader or DaemonDownloader. If there are no jobids, it runs the DaemonDownloader.

It also sets up a Reporter to report task status back to the server.

By design, derived classes need only be concerned with registering callbacks. See the LoggingDownloadRunner class for an example.

"""

import logging
from ciocore.downloader.job_downloader import JobDownloader
from ciocore.downloader.daemon_downloader import DaemonDownloader
from ciocore.downloader.log import LOGGER_NAME
from ciocore.downloader.reporter import Reporter

logger = logging.getLogger(LOGGER_NAME)

class DownloadRunnerBase(object):
    CLIENT_NAME = "DownloadRunnerBase"

    def __init__(self, jobids=None, location=None, **kwargs):
        """
        Initialize the downloader.
        """

        self.num_reporter_threads = kwargs.get("num_threads", 1)
        if jobids:
            self.downloader = JobDownloader(jobids, **kwargs)
        else:
            self.downloader = DaemonDownloader(location, **kwargs)

    def run(self):
        """
        Run the downloader.

        Start a reporter thread to report task status back to the server.
        """

        with Reporter(self.downloader, num_threads=self.num_reporter_threads):
            self.downloader.run()
