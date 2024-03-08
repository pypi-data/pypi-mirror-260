# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.utils.functional import cached_property
from educommon.report import AbstractDataProvider


from ..models import FeedBackDetails


class FeedBackDetailProvider(AbstractDataProvider):
    u"""Провайдер данных для ошибок в отчете."""

    def init(self, feedback):
        self._feedback = feedback

    @cached_property
    def details(self):
        for detail in FeedBackDetails.objects.filter(
            feedback_statistic__feedback_id=self._feedback
        ).values(
            "feedback_statistic__model_verbose",
            "record_id",
            "message",
            "processed"
        ):
            yield detail

    @property
    def session(self):
        return self._feedback.session

    @property
    def date_time(self):
        return self._feedback.date_time
