# -*- coding: utf-8 -*-
from __future__ import absolute_import

from educommon.report.reporter import SimpleReporter

from .provider import FeedBackDetailProvider
from .builder import FeedBackReportBuilder


class FeedbackReporter(SimpleReporter):
    u"""Репортер для отчета ошибок."""

    template_file_path = "../templates/report/report.xlsx"
    data_provider_class = FeedBackDetailProvider
    builder_class = FeedBackReportBuilder
